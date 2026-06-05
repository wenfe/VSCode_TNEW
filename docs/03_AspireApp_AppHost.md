# AspireApp AppHost Detaildokumentation

## Inhaltsverzeichnis
- [Überblick](#überblick)
- [Verantwortung des AppHost](#verantwortung-des-apphost)
- [Container und Funktionen](#container-und-funktionen)
- [Projekt-Workloads und Verdrahtung](#projekt-workloads-und-verdrahtung)
- [Konfiguration und Startverhalten](#konfiguration-und-startverhalten)
- [Betriebsrelevante Punkte](#betriebsrelevante-punkte)
- [Troubleshooting](#troubleshooting)

## Überblick
Der AppHost ist der zentrale Orchestrator der verteilten Lösung. Die technische Implementierung liegt in [AspireApp/AspireApp.AppHost/Program.cs](AspireApp/AspireApp.AppHost/Program.cs) und die Projektdefinition in [AspireApp/AspireApp.AppHost/AspireApp.AppHost.csproj](AspireApp/AspireApp.AppHost/AspireApp.AppHost.csproj).

## Verantwortung des AppHost
Der AppHost übernimmt folgende Kernfunktionen:
1. Aufbau des lokalen Observability-Stacks (LGTM + OTel Collector).
2. Aufbau unterstützender Integrationsdienste (MailHog, n8n).
3. Start und Verbindung der .NET-Workloads apiservice, puiapi und webfrontend.
4. Übergabe zentraler OTLP-Umgebungsvariablen an alle Workloads.

## Container und Funktionen

### Prometheus
Definition in [AspireApp/AspireApp.AppHost/Program.cs](AspireApp/AspireApp.AppHost/Program.cs).

Funktion:
- Metrik-Speicher und Query-Backend für Grafana.
- Nimmt Remote-Write-Daten an.

Konfigurationsquellen:
- [AspireApp/AspireApp.AppHost/observability/prometheus.yml](AspireApp/AspireApp.AppHost/observability/prometheus.yml)
- [AspireApp/AspireApp.AppHost/observability/prometheus-enable-remote-write.txt](AspireApp/AspireApp.AppHost/observability/prometheus-enable-remote-write.txt)

### Loki
Definition in [AspireApp/AspireApp.AppHost/Program.cs](AspireApp/AspireApp.AppHost/Program.cs).

Funktion:
- Log-Speicher für strukturierte und unstrukturierte Anwendungslogs.

Konfiguration:
- [AspireApp/AspireApp.AppHost/observability/loki-config.yaml](AspireApp/AspireApp.AppHost/observability/loki-config.yaml)

### Tempo
Definition in [AspireApp/AspireApp.AppHost/Program.cs](AspireApp/AspireApp.AppHost/Program.cs).

Funktion:
- Trace-Speicher für verteiltes Tracing.
- Generiert zusätzliche Metriken über den Metrics Generator.

Konfiguration:
- [AspireApp/AspireApp.AppHost/observability/tempo-config.yaml](AspireApp/AspireApp.AppHost/observability/tempo-config.yaml)

### OTel Collector
Definition in [AspireApp/AspireApp.AppHost/Program.cs](AspireApp/AspireApp.AppHost/Program.cs).

Funktion:
- Zentraler Telemetrie-Eingang (OTLP gRPC/HTTP).
- Routing der Daten zu Prometheus, Loki und Tempo.

Konfiguration:
- [AspireApp/AspireApp.AppHost/observability/otel-collector-config.yaml](AspireApp/AspireApp.AppHost/observability/otel-collector-config.yaml)

### MailHog
Definition in [AspireApp/AspireApp.AppHost/Program.cs](AspireApp/AspireApp.AppHost/Program.cs).

Funktion:
- Lokales SMTP-Testziel.
- UI zur Verifikation ausgehender Mails.

### n8n
Definition in [AspireApp/AspireApp.AppHost/Program.cs](AspireApp/AspireApp.AppHost/Program.cs).

Funktion:
- Verarbeitung von Grafana-Alerts über Webhooks.
- Workflow-basierte Weiterleitung (Teams/Slack/Mail/GitHub je Konfiguration).

Gemountete Dateien:
- [AspireApp/AspireApp.AppHost/observability/n8n/workflows/pui-alert-router.workflow.json](AspireApp/AspireApp.AppHost/observability/n8n/workflows/pui-alert-router.workflow.json)
- [AspireApp/AspireApp.AppHost/observability/n8n/workflows/pui-incident-automation.workflow.json](AspireApp/AspireApp.AppHost/observability/n8n/workflows/pui-incident-automation.workflow.json)
- [AspireApp/AspireApp.AppHost/observability/n8n/mailhog-credential.json](AspireApp/AspireApp.AppHost/observability/n8n/mailhog-credential.json)

### Grafana
Definition in [AspireApp/AspireApp.AppHost/Program.cs](AspireApp/AspireApp.AppHost/Program.cs).

Funktion:
- Visualisierung von Metriken, Logs, Traces.
- Alert-Regelauswertung und Notification Routing.

Provisioning-Dateien:
- [AspireApp/AspireApp.AppHost/observability/grafana/provisioning/datasources/datasources.yaml](AspireApp/AspireApp.AppHost/observability/grafana/provisioning/datasources/datasources.yaml)
- [AspireApp/AspireApp.AppHost/observability/grafana/provisioning/dashboards/dashboards.yaml](AspireApp/AspireApp.AppHost/observability/grafana/provisioning/dashboards/dashboards.yaml)
- [AspireApp/AspireApp.AppHost/observability/grafana/provisioning/alerting/rules.yaml](AspireApp/AspireApp.AppHost/observability/grafana/provisioning/alerting/rules.yaml)
- [AspireApp/AspireApp.AppHost/observability/grafana/provisioning/alerting/contact-points.yaml](AspireApp/AspireApp.AppHost/observability/grafana/provisioning/alerting/contact-points.yaml)
- [AspireApp/AspireApp.AppHost/observability/grafana/provisioning/alerting/notification-policies.yaml](AspireApp/AspireApp.AppHost/observability/grafana/provisioning/alerting/notification-policies.yaml)

## Projekt-Workloads und Verdrahtung
Der AppHost startet folgende Projekte aus der Solution:
- apiservice
- puiapi
- webfrontend

Definition in:
- [AspireApp/AspireApp.sln](AspireApp/AspireApp.sln)
- [AspireApp/AspireApp.AppHost/Program.cs](AspireApp/AspireApp.AppHost/Program.cs)

Verdrahtung:
1. OTLP Endpoint wird an alle drei Workloads übergeben.
2. webfrontend referenziert apiservice und puiapi für Service Discovery.
3. Externe HTTP-Endpunkte werden für webfrontend freigegeben.

## Konfiguration und Startverhalten

### Laufzeitkonfiguration
- [AspireApp/AspireApp.AppHost/appsettings.json](AspireApp/AspireApp.AppHost/appsettings.json)
- [AspireApp/AspireApp.AppHost/appsettings.Development.json](AspireApp/AspireApp.AppHost/appsettings.Development.json)
- [AspireApp/AspireApp.AppHost/Properties/launchSettings.json](AspireApp/AspireApp.AppHost/Properties/launchSettings.json)

### n8n-Initialisierung im Startkommando
Beim Start werden Credentials und Workflows importiert und Workflows aktiviert. Das reduziert manuelle Setup-Schritte für lokale Demos.

## Betriebsrelevante Punkte
1. Der AppHost verwendet feste Host-Ports für reproduzierbare lokale URL-Zugriffe.
2. n8n und Grafana laufen in Containern, greifen aber über host.docker.internal auf Host-Ports zu.
3. Der AppHost ist als net8.0-Anwendung definiert, das CLI aspire start erfordert in der aktuellen Toolchain dennoch .NET SDK 10 für C# AppHost-Unterstützung.

## Troubleshooting

### Problem: aspire start findet keinen unterstützten AppHost
Ursache:
- .NET SDK ist kleiner als 10.0.100.

Abhilfe:
1. AppHost direkt per dotnet run auf [AspireApp/AspireApp.AppHost/AspireApp.AppHost.csproj](AspireApp/AspireApp.AppHost/AspireApp.AppHost.csproj) starten.
2. Oder SDK auf 10.0.100+ aktualisieren.

### Problem: Alerts kommen nicht in n8n an
Prüfen:
1. Contact Point in [AspireApp/AspireApp.AppHost/observability/grafana/provisioning/alerting/contact-points.yaml](AspireApp/AspireApp.AppHost/observability/grafana/provisioning/alerting/contact-points.yaml).
2. Workflow-Webhook-Pfade in den Workflowdateien.
3. Workflow-Aktivierungsstatus in n8n.
