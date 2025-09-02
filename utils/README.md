# Utilities

## apply_collector_config.sh

Generic helper to apply a specific OpenTelemetry Collector config to an example without editing docker-compose.

Usage examples (run from repo root):

- Apply OTTL demo config to tail-sampling and restart only the collector:

```
./utils/apply_collector_config.sh \
  --example-dir tail-sampling \
  --config ./ottl-intro/otel-collector-config-ottl-demo.yaml \
  --services "otel-collector"
```

- Switch to the with-sampling config (auto-detects CONFIG_TYPE=with from target name):

```
./utils/apply_collector_config.sh \
  --example-dir tail-sampling \
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
- If your `.env` with Splunk vars lives at repo root, run compose from repo root and pass `-f` with full paths for multiple files.
