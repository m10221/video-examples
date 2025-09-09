# Utilities

## apply_collector_config.sh

Generic helper to apply a specific OpenTelemetry Collector config to an example without editing docker-compose.

Usage examples (run from repo root):

- Apply OTTL demo config to the shared infra collector and restart only the collector:

```
./utils/apply_collector_config.sh \
  --example-dir infra \
  --config ./ottl-intro/otel-collector-config-ottl-demo.yaml \
  --services "otel-collector"
```

- Switch to another config (example: with-sampling) for the infra collector:

```
./utils/apply_collector_config.sh \
  --example-dir infra \
  --config ./tail-sampling/otel-collector-config-with-sampling.yaml \
  --target otel-collector-config-with-sampling.yaml
```

Options:
- `--example-dir` (required): path to example directory containing docker-compose.yaml
- `--config` (required): source collector config to apply
- `--target` (optional): filename to write inside example dir (default: otel-collector-config-no-sampling.yaml)
- `--services` (optional): services to restart (default: "otel-collector order-service")
- `--config-type` (optional): force CONFIG_TYPE (with|no); else auto-detected from `--target`
- `--no-restart` (optional): copy only, skip restarts

Notes:
- If your `.env` with Splunk vars lives at repo root, the infra compose reads it via `env_file: ../.env`.
- To run infra from repo root instead of `infra/`, you can use: `docker compose -p ottl-intro -f infra/docker-compose.yaml up -d`.

Quick start (infra + shared app):
```
(cd infra && COMPOSE_PROJECT_NAME=ottl-intro docker compose up -d)
./utils/apply_collector_config.sh --example-dir infra --config ./ottl-intro/otel-collector-config-ottl-demo.yaml --services "otel-collector" --config-type no
(cd apps/order-service-flask && COMPOSE_PROJECT_NAME=ottl-intro docker compose up -d --build)
(cd tail-sampling && ./generate_load.sh 25 0.02)
```
