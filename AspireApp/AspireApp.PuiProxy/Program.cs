using System.Diagnostics;
using System.Diagnostics.Metrics;
using System.Net.Http.Json;

var builder = WebApplication.CreateBuilder(args);

builder.AddServiceDefaults();

builder.Services.AddProblemDetails();

builder.Services.AddHttpClient("pui-remote", client =>
{
	var configuredBaseUrl = builder.Configuration["Pui:BaseUrl"];
	var fallbackBaseUrl = builder.Configuration["PUI_BASE_URL"];
	var baseUrl = configuredBaseUrl ?? fallbackBaseUrl ?? "https://postman-echo.com";
	client.BaseAddress = new Uri(baseUrl);
	client.Timeout = TimeSpan.FromSeconds(8);
});

builder.Services.AddSingleton(Observability.Instance);

var app = builder.Build();

app.UseExceptionHandler();

var scenarios = new SimulationState();

app.MapPost("/pui/action/{name}", async (string name, HttpContext httpContext, IHttpClientFactory httpClientFactory, Observability observability, ILoggerFactory loggerFactory) =>
{
	var logger = loggerFactory.CreateLogger("PuiProxy");
	var traceId = Activity.Current?.TraceId.ToString() ?? Guid.NewGuid().ToString("N");
	var user = httpContext.Request.Headers["x-user-id"].ToString();
	var userValue = string.IsNullOrWhiteSpace(user) ? "anonymous" : user;

	using var scope = logger.BeginScope(new Dictionary<string, object>
	{
		["PuiAction"] = name,
		["TraceId"] = traceId,
		["User"] = userValue
	});

	using var activity = observability.ActivitySource.StartActivity("pui.action", ActivityKind.Server);
	activity?.SetTag("pui.action", name);
	activity?.SetTag("pui.user", userValue);
	activity?.SetTag("pui.correlation_id", traceId);

	var start = Stopwatch.GetTimestamp();
	observability.RequestsTotal.Add(1, new KeyValuePair<string, object?>("pui.action", name));

	if (scenarios.IsDown)
	{
		observability.RequestsFailed.Add(1, new KeyValuePair<string, object?>("pui.action", name));
		logger.LogError("PUI action rejected because service is marked as down.");
		return Results.Problem("PUI proxy is currently unavailable.", statusCode: StatusCodes.Status503ServiceUnavailable);
	}

	if (scenarios.SlowMode)
	{
		await Task.Delay(TimeSpan.FromSeconds(3));
	}

	if (scenarios.ErrorBurstRemaining > 0)
	{
		scenarios.ErrorBurstRemaining--;
		observability.RequestsFailed.Add(1, new KeyValuePair<string, object?>("pui.action", name));
		logger.LogError("Simulated error burst for action {Action}", name);
		return Results.Problem("Simulated error burst.", statusCode: StatusCodes.Status500InternalServerError);
	}

	try
	{
		var client = httpClientFactory.CreateClient("pui-remote");

		// Use a permissive fallback endpoint so local demos work while keeping remote mode semantics.
		var remotePath = client.BaseAddress?.AbsolutePath == "/" ? "/post" : string.Empty;
		var payload = new { action = name, at = DateTimeOffset.UtcNow, user = userValue, traceId };

		using var response = await client.PostAsJsonAsync(remotePath, payload);
		var success = response.IsSuccessStatusCode;

		if (!success)
		{
			observability.RequestsFailed.Add(1, new KeyValuePair<string, object?>("pui.action", name));
			logger.LogError("Remote PUI call failed with status {StatusCode}", (int)response.StatusCode);
			return Results.Problem($"Remote PUI call failed with status {(int)response.StatusCode}.", statusCode: StatusCodes.Status502BadGateway);
		}

		observability.ActionsSuccess.Add(1, new KeyValuePair<string, object?>("pui.action", name));
		logger.LogInformation("PUI action {Action} completed successfully.", name);

		var elapsedMs = Stopwatch.GetElapsedTime(start).TotalMilliseconds;
		observability.RequestDuration.Record(elapsedMs, new KeyValuePair<string, object?>("pui.action", name));

		return Results.Ok(new
		{
			action = name,
			status = "success",
			traceId,
			elapsedMs,
			source = "puiproxy"
		});
	}
	catch (Exception ex)
	{
		observability.RequestsFailed.Add(1, new KeyValuePair<string, object?>("pui.action", name));
		logger.LogError(ex, "Unexpected error while executing PUI action {Action}", name);
		return Results.Problem("Unexpected proxy error.", statusCode: StatusCodes.Status500InternalServerError);
	}
})
.WithName("RunPuiAction");

app.MapGet("/pui/report", (Observability observability) =>
{
	return Results.Ok(new
	{
		service = "puiproxy",
		generatedAt = DateTimeOffset.UtcNow,
		metrics = new[]
		{
			"pui.requests.total",
			"pui.requests.failed",
			"pui.actions.success",
			"pui.request.duration"
		},
		traceSource = observability.ActivitySource.Name
	});
})
.WithName("GetPuiReport");

app.MapPost("/pui/simulate/{scenario}", (string scenario, ILoggerFactory loggerFactory) =>
{
	var logger = loggerFactory.CreateLogger("PuiSimulation");
	switch (scenario.ToLowerInvariant())
	{
		case "error-burst":
			scenarios.ErrorBurstRemaining = 20;
			logger.LogWarning("Enabled error burst simulation with {Remaining} failures", scenarios.ErrorBurstRemaining);
			return Results.Ok(new { scenario, enabled = true, failures = scenarios.ErrorBurstRemaining });
		case "slow":
			scenarios.SlowMode = true;
			logger.LogWarning("Enabled slow mode simulation");
			return Results.Ok(new { scenario, enabled = true });
		case "down":
			scenarios.IsDown = true;
			logger.LogWarning("Enabled down mode simulation");
			return Results.Ok(new { scenario, enabled = true });
		case "reset":
			scenarios.Reset();
			logger.LogInformation("Reset all simulation modes");
			return Results.Ok(new { scenario, enabled = false });
		default:
			return Results.BadRequest(new { error = "Unknown scenario. Use error-burst, slow, down, reset." });
	}
})
.WithName("SetSimulationScenario");

app.MapGet("/pui/simulate/state", () => Results.Ok(new
{
	isDown = scenarios.IsDown,
	slowMode = scenarios.SlowMode,
	errorBurstRemaining = scenarios.ErrorBurstRemaining
}));

app.MapDefaultEndpoints();

app.Run();

public sealed class SimulationState
{
	public bool IsDown { get; set; }
	public bool SlowMode { get; set; }
	public int ErrorBurstRemaining { get; set; }

	public void Reset()
	{
		IsDown = false;
		SlowMode = false;
		ErrorBurstRemaining = 0;
	}
}

public sealed class Observability
{
	private const string MeterName = "Pui.Proxy";
	private const string ActivitySourceName = "Pui.Proxy";

	public static Observability Instance { get; } = new();

	public ActivitySource ActivitySource { get; } = new(ActivitySourceName);
	public Meter Meter { get; } = new(MeterName);

	public Counter<long> RequestsTotal { get; }
	public Counter<long> RequestsFailed { get; }
	public Counter<long> ActionsSuccess { get; }
	public Histogram<double> RequestDuration { get; }

	private Observability()
	{
		RequestsTotal = Meter.CreateCounter<long>("pui.requests.total", description: "Total count of proxied PUI requests");
		RequestsFailed = Meter.CreateCounter<long>("pui.requests.failed", description: "Total count of failed proxied PUI requests");
		ActionsSuccess = Meter.CreateCounter<long>("pui.actions.success", description: "Total count of successful PUI actions");
		RequestDuration = Meter.CreateHistogram<double>("pui.request.duration", unit: "ms", description: "Duration of PUI requests in milliseconds");
	}
}
