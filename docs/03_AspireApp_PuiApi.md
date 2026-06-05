# AspireApp PuiApi Detaildokumentation

## Inhaltsverzeichnis
- [Überblick](#überblick)
- [Komponenten und Klassen](#komponenten-und-klassen)
- [Endpunkte und Funktionen](#endpunkte-und-funktionen)
- [Telemetry-Funktionen](#telemetry-funktionen)
- [Szenario- und Simulationslogik](#szenario--und-simulationslogik)
- [Konfiguration](#konfiguration)
- [Beispielabläufe](#beispielabläufe)
- [Troubleshooting](#troubleshooting)

## Überblick
Die PuiApi ist die fachliche Test- und Simulations-API der Lösung. Quellbasis ist [AspireApp/AspireApp.PuiApi/Program.cs](AspireApp/AspireApp.PuiApi/Program.cs).

Ziele:
1. Fachaktionen ausführen.
2. Fehlerszenarien reproduzierbar simulieren.
3. Metriken, Logs und Traces für Observability erzeugen.

## Komponenten und Klassen

### SimulationState
Definiert in [AspireApp/AspireApp.PuiApi/Program.cs](AspireApp/AspireApp.PuiApi/Program.cs).

Verantwortung:
- Hält den aktuellen Simulationszustand der API.

Felder:
- IsDown
- SlowMode
- ErrorBurstRemaining

Funktion:
- Reset() setzt alle Zustände auf Normalbetrieb.

### Observability
Definiert in [AspireApp/AspireApp.PuiApi/Program.cs](AspireApp/AspireApp.PuiApi/Program.cs).

Verantwortung:
- Kapselt ActivitySource und Meter plus konkrete Zähler/Histogramm.

Bereitgestellte Metrikobjekte:
- RequestsTotal (pui.requests.total)
- RequestsFailed (pui.requests.failed)
- ActionsSuccess (pui.actions.success)
- RequestDuration (pui.request.duration)

## Endpunkte und Funktionen

### GET /
Rückgabe eines einfachen Servicezustands mit service, status und timestamp.

### POST /api/pui/actions/{name}
Hauptfunktion für fachliche Aktionen.

Funktionsablauf:
1. Liest Benutzerkontext aus Header x-user-id (Fallback anonymous).
2. Erstellt Logging-Scope mit Action, TraceId und User.
3. Startet Activity pui.action mit Tags.
4. Erhöht pui.requests.total.
5. Prüft Simulationszustände:
   - IsDown => 503
   - SlowMode => Delay 3 Sekunden
   - ErrorBurstRemaining > 0 => dekrementieren und 500 zurückgeben
6. Führt Remote-POST über HttpClient pui-remote aus.
7. Bei Erfolg:
   - pui.actions.success erhöhen
   - pui.request.duration messen
   - 200 mit Payload und elapsedMs zurückgeben
8. Bei Fehler:
   - pui.requests.failed erhöhen
   - 502 oder 500 zurückgeben

### GET /api/pui/report
Liefert einen strukturierten Report über:
- Service
- Timestamp
- bekannte Metriknamen
- TraceSource-Name

### POST /api/pui/simulations/{scenario}
Setzt Szenariomodus anhand Parameter scenario.

Unterstützte Werte:
- error-burst
- slow
- down
- reset

### POST /api/pui/reset
Setzt den Simulationszustand explizit zurück (entspricht reset-Szenario).

### GET /api/pui/simulations/state
Liefert den aktuellen Simulationszustand (isDown, slowMode, errorBurstRemaining).

## Telemetry-Funktionen

### Logging
- Logger-Kategorien PuiApi und PuiSimulation.
- Scope enthält Action, TraceId, User.

### Tracing
- Eigene ActivitySource AspireApp.PuiApi.
- Activity-Name pui.action.
- Tags enthalten action, user, correlation_id.

### Metriken
Erzeugte Metriknamen:
- pui.requests.total
- pui.requests.failed
- pui.actions.success
- pui.request.duration

Diese Metriken werden über die gemeinsame OTel-Pipeline weiterverarbeitet.

## Szenario- und Simulationslogik

### error-burst
- Setzt ErrorBurstRemaining initial auf 20.
- Die nächsten Requests liefern absichtlich Fehler, bis der Zähler 0 ist.

### slow
- Aktiviert SlowMode.
- Requests werden künstlich verzögert.

### down
- Aktiviert IsDown.
- Requests auf Actions liefern 503.

### reset
- Deaktiviert alle Modi und setzt Zähler zurück.

## Konfiguration

Relevante Dateien:
- [AspireApp/AspireApp.PuiApi/appsettings.json](AspireApp/AspireApp.PuiApi/appsettings.json)
- [AspireApp/AspireApp.PuiApi/appsettings.Development.json](AspireApp/AspireApp.PuiApi/appsettings.Development.json)
- [AspireApp/AspireApp.PuiApi/Properties/launchSettings.json](AspireApp/AspireApp.PuiApi/Properties/launchSettings.json)

Wichtige Konfigurationsschlüssel:
- Pui:BaseUrl
- PUI_BASE_URL (Fallback via Environment)

## Beispielabläufe

### Normalfall
1. POST /api/pui/actions/create-report
2. Antwort mit status success.
3. Metriken: total + success + duration steigen.

### Fehlerfall
1. POST /api/pui/simulations/error-burst
2. Danach POST /api/pui/actions/create-report
3. Antwort 500 während Burst aktiv ist.
4. pui.requests.failed steigt.

### Recovery
1. POST /api/pui/reset
2. Aktionen laufen wieder normal.

## Troubleshooting

### Unerwartete 502 bei Action-Aufrufen
Prüfen:
1. Pui:BaseUrl ist erreichbar.
2. Remote-Endpoint akzeptiert POST.

### Keine PUI-Metriken sichtbar
Prüfen:
1. OTEL_EXPORTER_OTLP_ENDPOINT in Laufzeitumgebung gesetzt.
2. OTel-Collector erreichbar.
3. Prometheus Remote-Write aktiv.

### Szenario bleibt aktiv
Abhilfe:
1. POST /api/pui/reset aufrufen.
2. Zustand über GET /api/pui/simulations/state verifizieren.
