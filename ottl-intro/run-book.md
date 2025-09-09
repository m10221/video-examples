# OTTL Intro Demo — Run Book

A quick reference for starting the shared infra, applying the OTTL config, running the shared Flask app, generating load, and validating results.

## Prereqs
- Root `.env` contains Splunk settings if you plan to export to Splunk:
  - `SPLUNK_REALM`, `SPLUNK_ACCESS_TOKEN`
- Ports free: 16686 (Jaeger UI), 4317/4318 (OTLP), 5000 (Flask app)

## Start infra (Jaeger + Splunk OTel Collector)
```bash
(cd infra && COMPOSE_PROJECT_NAME=ottl-intro docker compose up -d)
```

## Apply the OTTL config (transform processor)
```bash
COMPOSE_PROJECT_NAME=ottl-intro ./utils/apply_collector_config.sh \
  --example-dir infra \
  --config ./ottl-intro/otel-collector-config-ottl-demo.yaml \
  --services "otel-collector" \
  --config-type no
```

## Start the shared Flask app
- Default exporter endpoint in app: `http://host.docker.internal:4317`
- Default service name: `order-service`
```bash
(cd apps/order-service-flask && COMPOSE_PROJECT_NAME=ottl-intro docker compose up -d --build)
```

## Generate load
- Sends requests to `http://localhost:5000/checkout`
```bash
./utils/generate_load.sh 25 0.02
```

## Validate in Jaeger UI
- Open: http://localhost:16686
- Service: `order-service`
- Look for (from OTTL transforms):
  - `demo.ottl = applied`
  - `issue_detected = true` (boolean)
  - `scenario_group = unhappy` (errors/high_latency)
  - Span renamed to `checkout - ERROR` on error
  - Resource attr: `service.namespace = ottl-intro`

## Quick log checks
Collector (confirm transforms, check exporter):
```bash
(cd infra && docker compose -p ottl-intro logs --since 2m otel-collector | tail -n 120)
```
App (Flask):
```bash
(cd apps/order-service-flask && docker compose -p ottl-intro logs --since 2m order-service | tail -n 120)
```

## Common tweaks
- Override service name:
```bash
(cd apps/order-service-flask && OTEL_SERVICE_NAME=my-order-service COMPOSE_PROJECT_NAME=ottl-intro docker compose up -d --build)
```
- Disable Splunk export (local only): remove `otlphttp/splunk` exporter and the `traces/splunk` pipeline from the applied config.

## Video Flow (Presenter Guide)
- Intro: “OTTL transforms telemetry in the Collector—no app redeploy.”
- IDE: show `apps/order-service-flask/app.py` (OTLP endpoint `http://host.docker.internal:4317`, service name `order-service`).
- IDE: show `ottl-intro/otel-collector-config-ottl-demo.yaml` rules:
  - `demo.ottl = applied`
  - `issue_detected` string → boolean
  - `scenario_group = unhappy` on error/high_latency
  - Rename span to `checkout - ERROR` on error
  - Resource: `service.namespace = ottl-intro`
- Generate load:
  ```bash
  ./utils/generate_load.sh 25 0.02
  ```
- Splunk Observability Cloud (or Jaeger):
  - Filters: `service.name=order-service`, `deployment.environment=moss-demo-environment`, `service.namespace=ottl-intro`
  - Open a trace with an error: confirm span name change and attributes above.
  - Jaeger fallback: http://localhost:16686 (Service: order-service)
- Tips: Keep `COMPOSE_PROJECT_NAME=ottl-intro` consistent for start/apply/app.

## Stop everything
- Because both stacks use the same project name, one command stops all containers:
```bash
docker compose -p ottl-intro down
