# Video Examples

A collection of runnable OpenTelemetry demo scenarios and utilities.

## Quick Start: Scaffold a New Demo with the Shared App

Use the shared Flask order service as a starting point for new demos.

1) Shut down any existing stacks (avoid port or name conflicts):

```
(cd tail-sampling && docker compose down)
(cd infra && docker compose -p ottl-intro down || true)
(cd infra && docker compose down || true)
(cd apps/order-service-flask && docker compose -p ottl-intro down || true)
(cd apps/order-service-flask && docker compose down || true)
```

2) Scaffold a new demo directory (creates `demo-scaffold/` with `app/`, compose, and README):

```
./utils/scaffold_demo.sh --name demo-scaffold
```

3) Start the shared infra (Jaeger + OTel Collector) with a unique project name:

```
(cd infra && COMPOSE_PROJECT_NAME=ottl-scaffold docker compose up -d)
```

4) Build and start the scaffolded app:

```
(cd demo-scaffold && docker compose build && docker compose up -d)
```

5) Generate load and view traces:

```
./utils/generate_load.sh 25 0.02
# Jaeger UI: http://localhost:16686
```

## Utilities

- `./utils/scaffold_demo.sh` — scaffold a new demo directory using the shared app
- `./utils/apply_collector_config.sh` — apply a collector config to an example and restart selected services
- `./utils/generate_load.sh` — generate HTTP traffic against the app (defaults to http://localhost:5000/checkout)

## Shared App

- `apps/order-service-flask/` — reusable Flask app instrumented with OpenTelemetry
  - See its README for how to embed it in a demo and customize endpoint, service name, and ports.
