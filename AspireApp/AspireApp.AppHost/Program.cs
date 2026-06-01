var builder = DistributedApplication.CreateBuilder(args);

// === Observability stack (LGTM + OTel Collector + MailHog + n8n) ===

builder.AddContainer("prometheus", "prom/prometheus", "v2.55.1")
    .WithBindMount("observability/prometheus.yml", "/etc/prometheus/prometheus.yml", isReadOnly: true)
    .WithArgs(
        "--config.file=/etc/prometheus/prometheus.yml",
        "--web.enable-remote-write-receiver",
        "--enable-feature=exemplar-storage",
        "--storage.tsdb.retention.time=6h")
    .WithEndpoint(targetPort: 9090, port: 39090, name: "http", scheme: "http", isProxied: false);

builder.AddContainer("loki", "grafana/loki", "3.2.1")
    .WithBindMount("observability/loki-config.yaml", "/etc/loki/local-config.yaml", isReadOnly: true)
    .WithArgs("-config.file=/etc/loki/local-config.yaml")
    .WithEndpoint(targetPort: 3100, port: 33100, name: "http", scheme: "http", isProxied: false);

builder.AddContainer("tempo", "grafana/tempo", "2.6.1")
    .WithBindMount("observability/tempo-config.yaml", "/etc/tempo.yaml", isReadOnly: true)
    .WithArgs("-config.file=/etc/tempo.yaml")
    .WithEndpoint(targetPort: 3200, port: 33200, name: "http", scheme: "http", isProxied: false);

builder.AddContainer("otel-collector", "otel/opentelemetry-collector-contrib", "0.112.0")
    .WithBindMount("observability/otel-collector-config.yaml", "/etc/otelcol-contrib/config.yaml", isReadOnly: true)
    .WithArgs("--config=/etc/otelcol-contrib/config.yaml")
    .WithEndpoint(targetPort: 4317, port: 34317, name: "otlp-grpc", scheme: "http", isProxied: false)
    .WithEndpoint(targetPort: 4318, port: 34318, name: "otlp-http", scheme: "http", isProxied: false)
    .WithEndpoint(targetPort: 13133, port: 31333, name: "health", scheme: "http", isProxied: false);

builder.AddContainer("mailhog", "mailhog/mailhog", "v1.0.1")
    .WithEndpoint(targetPort: 1025, port: 32525, name: "smtp", isProxied: false)
    .WithEndpoint(targetPort: 8025, port: 38025, name: "http", scheme: "http", isProxied: false);

builder.AddContainer("n8n", "n8nio/n8n", "1.64.0")
    .WithBindMount("observability/n8n/workflows", "/files/workflows", isReadOnly: true)
    .WithBindMount("observability/n8n/mailhog-credential.json", "/files/mailhog-credential.json", isReadOnly: true)
    .WithEnvironment("N8N_HOST", "localhost")
    .WithEnvironment("N8N_PORT", "5678")
    .WithEnvironment("N8N_PROTOCOL", "http")
    .WithEnvironment("N8N_SECURE_COOKIE", "false")
    .WithEnvironment("N8N_EDITOR_BASE_URL", "http://localhost:35678")
    .WithEnvironment("N8N_DEFAULT_BINARY_DATA_MODE", "filesystem")
    .WithEntrypoint("/bin/sh")
    .WithArgs("-lc", "n8n import:credentials --input=/files/mailhog-credential.json || true; n8n import:workflow --separate --input=/files/workflows || true; n8n update:workflow --all --active=true || true; exec n8n start")
    .WithEndpoint(targetPort: 5678, port: 35678, name: "http", scheme: "http", isProxied: false);

builder.AddContainer("grafana", "grafana/grafana", "11.3.0")
    .WithBindMount("observability/grafana/provisioning", "/etc/grafana/provisioning", isReadOnly: true)
    .WithBindMount("observability/grafana/dashboards", "/var/lib/grafana/dashboards", isReadOnly: true)
    .WithEnvironment("GF_AUTH_ANONYMOUS_ENABLED", "true")
    .WithEnvironment("GF_AUTH_ANONYMOUS_ORG_ROLE", "Admin")
    .WithEnvironment("GF_AUTH_DISABLE_LOGIN_FORM", "true")
    .WithEnvironment("GF_FEATURE_TOGGLES_ENABLE", "traceqlEditor")
    .WithEnvironment("GF_SECURITY_ALLOW_EMBEDDING", "true")
    .WithEndpoint(targetPort: 3000, port: 33000, name: "http", scheme: "http", isProxied: false);

const string OtlpEndpoint = "http://localhost:34317";

var apiService = builder.AddProject<Projects.AspireApp_ApiService>("apiservice")
    .WithEnvironment("OTEL_EXPORTER_OTLP_ENDPOINT", OtlpEndpoint)
    .WithEnvironment("OTEL_EXPORTER_OTLP_PROTOCOL", "grpc")
    .WithEnvironment("OTEL_SERVICE_NAME", "apiservice");

var puiApi = builder.AddProject<Projects.AspireApp_PuiApi>("puiapi")
    .WithEnvironment("OTEL_EXPORTER_OTLP_ENDPOINT", OtlpEndpoint)
    .WithEnvironment("OTEL_EXPORTER_OTLP_PROTOCOL", "grpc")
    .WithEnvironment("OTEL_SERVICE_NAME", "puiapi");

builder.AddProject<Projects.AspireApp_Web>("webfrontend")
    .WithExternalHttpEndpoints()
    .WithEnvironment("OTEL_EXPORTER_OTLP_ENDPOINT", OtlpEndpoint)
    .WithEnvironment("OTEL_EXPORTER_OTLP_PROTOCOL", "grpc")
    .WithEnvironment("OTEL_SERVICE_NAME", "webfrontend")
    .WithReference(apiService)
    .WithReference(puiApi);

builder.Build().Run();
