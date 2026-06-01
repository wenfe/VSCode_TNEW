namespace AspireApp.Web;

public class PuiApiClient(HttpClient httpClient)
{
    public async Task<PuiActionResult> RunActionAsync(string actionName, CancellationToken cancellationToken = default)
    {
        using var response = await httpClient.PostAsync($"/api/pui/actions/{Uri.EscapeDataString(actionName)}", content: null, cancellationToken);
        var payload = await response.Content.ReadAsStringAsync(cancellationToken);

        return new PuiActionResult
        {
            IsSuccess = response.IsSuccessStatusCode,
            StatusCode = (int)response.StatusCode,
            Payload = payload
        };
    }

    public async Task<PuiActionResult> SetScenarioAsync(string scenario, CancellationToken cancellationToken = default)
    {
        var path = scenario.Equals("reset", StringComparison.OrdinalIgnoreCase)
            ? "/api/pui/reset"
            : $"/api/pui/simulations/{Uri.EscapeDataString(scenario)}";
        using var response = await httpClient.PostAsync(path, content: null, cancellationToken);
        var payload = await response.Content.ReadAsStringAsync(cancellationToken);

        return new PuiActionResult
        {
            IsSuccess = response.IsSuccessStatusCode,
            StatusCode = (int)response.StatusCode,
            Payload = payload
        };
    }
}

public sealed class PuiActionResult
{
    public bool IsSuccess { get; init; }
    public int StatusCode { get; init; }
    public string Payload { get; init; } = string.Empty;
}
