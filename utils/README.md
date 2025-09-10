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
./utils/generate_load.sh 25 0.02
```

## scaffold_demo.sh

Scaffold a new demo directory pre-wired with the shared order service app.

### Usage
```
utils/scaffold_demo.sh --name <demo-name> [--port 5000] [--service-name my-demo-order-service] \
  [--collector host|service] [--collector-service-name otel-collector]
```

- `--name` (required): target demo directory to create
- `--port` (optional, default 5000): host port to map to the Flask app's 5000
- `--service-name` (optional): OTEL service name to set inside the app
- `--collector` (optional, default host): whether to point to a collector on the `host` or a `service` in the same compose
- `--collector-service-name` (optional, default otel-collector): service name to use when `--collector service`

Creates:
- `<name>/app/` copied from `apps/order-service-flask/`
- `<name>/docker-compose.yaml`
- `<name>/README.md`

### End-to-end test flow

1) Spin down any existing stacks (avoid port/name conflicts):
```
(cd tail-sampling && docker compose down)
(cd infra && docker compose -p ottl-intro down || true)
(cd infra && docker compose down || true)
(cd apps/order-service-flask && docker compose -p ottl-intro down || true)
(cd apps/order-service-flask && docker compose down || true)
```

2) Scaffold a demo:
```
utils/scaffold_demo.sh --name demo-scaffold
```

3) Start infra (Jaeger + OTel Collector) with a unique project name:
```
(cd infra && COMPOSE_PROJECT_NAME=ottl-scaffold docker compose up -d)
```

4) Build and start the scaffolded app:
```
(cd demo-scaffold && docker compose build && docker compose up -d)
```

5) Verify logs (last 2 minutes):
```
(cd infra && docker compose -p ottl-scaffold logs --since 2m otel-collector | tail -n 120)
(cd demo-scaffold && docker compose logs --since 2m order-service | tail -n 120)
```

6) Generate load:
```
./utils/generate_load.sh 25 0.02
```

7) Optional teardown when finished:
```
(cd demo-scaffold && docker compose down)
(cd infra && docker compose -p ottl-scaffold down)
```
