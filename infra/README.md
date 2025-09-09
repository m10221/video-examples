# Shared Infra (Collector + Jaeger)

This directory provides a reusable OpenTelemetry Collector and Jaeger stack for all demos.

## What’s included
- `otel-collector` (contrib image) exposing OTLP gRPC (4317) and HTTP (4318)
- `jaeger` all-in-one with UI at http://localhost:16686
- Collector mounts `/etc/otel/config.yaml` from a file in this directory

## Start the infra
```bash
# From repo root or infra/
(cd infra && COMPOSE_PROJECT_NAME=ottl-intro docker compose up -d)
```
Containers will be named like `ottl-intro-otel-collector-1` and `ottl-intro-jaeger-1`.

## Apply or switch collector config
Use the shared utility to copy any config into this directory and restart only the collector.

```bash
# Apply the OTTL demo config
./utils/apply_collector_config.sh \
  --example-dir infra \
  --config ./ottl-intro/otel-collector-config-ottl-demo.yaml \
  --services "otel-collector" \
  --config-type no
```
Notes:
- The compose file mounts `./otel-collector-config-no-sampling.yaml` as `/etc/otel/config.yaml`.
- The utility will copy your provided config to that target filename and restart the collector.

## Use with the shared order service
Run the app standalone so it exports to the infra collector on the host:
```bash
(cd apps/order-service-flask && COMPOSE_PROJECT_NAME=ottl-intro docker compose up -d --build)
```
The app defaults to `OTEL_EXPORTER_OTLP_ENDPOINT=http://host.docker.internal:4317` so it can reach the infra collector.

## Stop the infra
```bash
(cd infra && docker compose down)
```
