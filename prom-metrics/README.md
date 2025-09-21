# Prometheus Metrics Demo (OTel Collector -> Splunk Observability)

This example shows the OpenTelemetry Collector scraping a Prometheus `/metrics` endpoint from a small Flask app and exporting those metrics to Splunk Observability Cloud.

## Layout
- `prom-metrics/docker-compose.yaml` — starts `demo-app` and `otel-collector`
- `prom-metrics/app/` — Flask app exposing `/metrics` via `prometheus_flask_exporter`
- `prom-metrics/otel-collector-config-prom-demo.yaml` — Collector config with Prometheus receiver and Signalfx exporter

## Prerequisites
- Docker / Docker Compose
- `.env` at repo root with Splunk credentials (if exporting to Splunk):
  - `SPLUNK_REALM=...`
  - `SPLUNK_ACCESS_TOKEN=...`

## Quick start
Start the stack (Collector scrapes the app directly; no Prometheus server required):
```bash
(cd prom-metrics && COMPOSE_PROJECT_NAME=prom-demo docker compose up -d --build)
```

Hit the app to generate metrics (compatible with your existing load generator that calls /checkout on port 5000):
```bash
# Normal
curl -s http://localhost:5000/checkout > /dev/null
# Error path occurs randomly; to force a quick mix, just loop

# Quick loop to generate a mix
for i in {1..10}; do
  curl -s http://localhost:5000/checkout > /dev/null
  sleep 0.2
done
```

Validate locally:
```bash
# App metrics endpoint
curl -s http://localhost:5000/metrics | head -n 40

# Collector logs
(cd prom-metrics && docker compose -p prom-demo logs --since 2m otel-collector | tail -n 120)
```

See metrics in Splunk Observability Cloud:
- Metric Finder: search for `flask_http_request_*`, `process_*`, `python_*`
- Build a chart with request rate by `status`/`method`/`endpoint`
- If you want system-level metrics as well, add a node-exporter service and scrape it in the same Collector config

## Stop
```bash
docker compose -p prom-demo -f prom-metrics/docker-compose.yaml down
```

## Notes
- This demo uses the Collector’s `prometheus` receiver with `scrape_configs` (Prometheus-compatible). No Prometheus server is required.
- The Collector converts Prometheus exposition to OTLP metrics and exports to Splunk via the `signalfx` exporter.
- You can add more targets to `receivers.prometheus.config.scrape_configs` to scrape multiple apps/exporters.
