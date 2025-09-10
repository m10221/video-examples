# Shared Order Service (Flask)

A reusable, demo-agnostic Flask app instrumented with OpenTelemetry. Use it across examples without copying app code.

## Run with Docker Compose (standalone)

From `apps/order-service-flask/`:

```bash
docker compose up -d --build
```

Defaults:
- OTLP endpoint: `http://localhost:4317` (assumes a collector running on the host)
- Service name: `no-order-service`
- CONFIG_TYPE: `no`
- ENVIRONMENT: `moss-demo-environment`
- Port: `5000` (exposed on host)

Tip: choose your container name prefix with a project name:
```bash
COMPOSE_PROJECT_NAME=ottl-intro docker compose up -d --build
# container will be: ottl-intro-order-service-1
```

## Pointing to a Collector in Compose

If your collector is running in another Compose project, using host networking is simplest. The default `OTEL_EXPORTER_OTLP_ENDPOINT` is `http://localhost:4317` so the app exports to a collector listening on the host.

Override if needed:
```bash
OTEL_EXPORTER_OTLP_ENDPOINT=http://127.0.0.1:4317 docker compose up -d --build
```

## Environment variables
- `OTEL_EXPORTER_OTLP_ENDPOINT`: OTLP gRPC endpoint (default `http://localhost:4317`)
- `OTEL_SERVICE_NAME`: service name (default `no-order-service`)
- `CONFIG_TYPE`: included in the fallback service name (default `no`)
- `ENVIRONMENT`: deployment environment tag (default `moss-demo-environment`)

## Development
- Source: `apps/order-service-flask/app.py`
- Dockerfile: `apps/order-service-flask/Dockerfile`
- Compose: `apps/order-service-flask/docker-compose.yaml`

## Embedding in a new demo

You can copy this app into any demo directory and run it alongside your own collector or other services.

### Minimal steps
1. Create a demo directory (e.g., `my-demo/`).
2. Copy the app into `my-demo/app/` (preserve the subfolder name `app/`).
3. Create a `my-demo/docker-compose.yaml` like:

```yaml
services:
  order-service:
    build:
      context: ./app
    ports:
      - "5000:5000"
    environment:
      # If your collector runs on the host:
      - OTEL_EXPORTER_OTLP_ENDPOINT=http://host.docker.internal:4317
      # Or, if your collector is another service in this compose file:
      # - OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4317
      - OTEL_SERVICE_NAME=my-demo-order-service
      - CONFIG_TYPE=no
      - ENVIRONMENT=my-demo-env
```

Then run:

```bash
(cd my-demo && docker compose up -d --build)
```

### Things to customize per demo
- Port mapping (`5000:5000`) if you run multiple demos at once
- `OTEL_SERVICE_NAME` so traces are easy to distinguish
- `OTEL_EXPORTER_OTLP_ENDPOINT` depending on where your collector runs

### Optional: apply collector configs
If your demo also includes a collector and you want to swap configs without editing compose files, you can reuse the utility:

```bash
./utils/apply_collector_config.sh \
  --example-dir my-demo \
  --config ./ottl-intro/otel-collector-config-ottl-demo.yaml \
  --services "otel-collector"
```

This copies the config into `my-demo/` under the expected target filename and restarts the selected services.
