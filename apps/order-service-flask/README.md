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
