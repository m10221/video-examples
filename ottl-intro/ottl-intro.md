# OpenTelemetry Transformation Language (OTTL) — 5–10 min Intro + Demo

## 1) Why OTTL?

- __Unified language__ to transform, filter, and route telemetry inside the Collector
- __Simple, expressive statements__ with a `where` clause for conditions
- __Works across contexts__: resource, scope, span, log, metric datapoint
- __Incremental adoption__: add a `transform` or `filter` processor without changing the app

---

## 2) Where OTTL is used

- __transform processor__: mutate data (rename spans, add/convert attributes, normalize)
- __filter processor__: include/exclude using OTTL boolean expressions
- __routing processor__: route by conditions

Think: “ETL for telemetry” directly in the Collector’s pipelines.

---

## 3) Mental model

```
Application           OTel Collector                                   Backend
  (Traces)  --->  [receiver] -> [processors: transform(+tail_sampling)] -> [exporter]
                              ^ OTTL lives here
```

- You write small statements that run on each span/resource/etc.
- `where` applies the statement only if the condition matches.
- `error_mode: ignore` means a single failed statement won’t break the pipeline.

---

## 4) OTTL syntax at a glance

- __Set new or existing attribute__
  - `set(attributes["key"], "value")`
- __Rename or reshape__
  - `set(name, "new span name")`
  - `set(attributes["new"], attributes["old"])`
  - `delete_key(attributes, "old")`
- __Conditional__
  - `... where attributes["scenario"] == "error"`
- __Resource context__
  - With `context: resource`, `attributes[...]` targets resource attrs
  - Resource = identity of the producer (who/where): stable tags like `service.name`, `service.version`, `deployment.environment`, `service.namespace`
  - Span = a single operation (what happened this time): request-scoped attrs like `scenario`, `order.id`
  - Why resource? Consistent cross-signal tags (traces/metrics/logs), less duplication, and filterable dimensions in backends
  - Splunk note: adding `service.namespace` at resource level adds a filterable tag; it does not rename/split the APM service unless you change `service.name`

---

## 5) Demo scenario (using your Flask app)

- App emits spans with attributes like `scenario`, `order.id`, `customer.id`, `issue_detected` (string "true"). See `tail-sampling/app/app.py`.
- We’ll use OTTL to:
  - Convert `issue_detected` from string to boolean
  - Derive `scenario_group` for quick filtering
  - Rename span when an error occurs (easy visual in Jaeger)
  - Add resource attributes to tag the environment

---

## 6) OTTL config snippet (transform processor)

```yaml
processors:
  transform/ottl_demo:
    error_mode: ignore
    trace_statements:
      - context: span
        statements:
          - set(attributes["demo.ottl"], "applied")
          - set(attributes["issue_detected"], true) where attributes["issue_detected"] == "true"
          - set(attributes["scenario_group"], "unhappy") where attributes["scenario"] == "error" or attributes["scenario"] == "high_latency"
          - set(name, "checkout - ERROR") where attributes["scenario"] == "error"
      - context: resource
        statements:
          - set(attributes["service.namespace"], "tail-sampling-demo")
          - set(attributes["env"], attributes["deployment.environment"]) where attributes["deployment.environment"] != nil
```

Full, runnable config placed at `ottl-intro/otel-collector-config-ottl-demo.yaml`.

---

## 7) How to run the demo (5 min)

1. __Start the stack__
   - `(cd tail-sampling && docker compose up -d)`
2. __Apply the OTTL config__ (using the reusable utility script)
   - `./utils/apply_collector_config.sh --example-dir tail-sampling --config ./ottl-intro/otel-collector-config-ottl-demo.yaml`
3. __Generate load__
   - `./utils/generate_load.sh 100 0.05`
4. __Open Jaeger__
   - http://localhost:16686
   - Service: `no-order-service`
   - Inspect spans; look for:
     - `demo.ottl: applied`
     - `issue_detected: true` (boolean)
     - `scenario_group: unhappy` on error/high_latency
     - Span name changed to `checkout - ERROR` for error scenarios

Tip: Switch back anytime with your existing script (tail/no-tail) to compare before/after transforms.

### Optional: run the shared app via Compose override

- Build and run `order-service` from `apps/order-service-flask/` in the tail-sampling project:
  - `(cd tail-sampling && docker compose -f docker-compose.yaml -f docker-compose.order-service-shared.override.yaml up -d --build order-service)`

---

## 8) Diagram ideas (for slides)

- __Pipeline view__
  - Boxes for Receiver -> Transform(OTTL) -> Tail Sampling -> Exporter
  - Callouts on Transform: "normalize types", "derive labels", "PII cleanup"
- __Before/After span__
  - Left JSON: span with `issue_detected: "true"`
  - Right JSON: span with `issue_detected: true`, `scenario_group: unhappy`, renamed `name`
- __Decision flow__
  - Diamond: `scenario == error?` -> Set attr, rename -> Export

---

## 9) Good practices

- __Keep rules small and readable__; group related statements
- __Prefer additive changes__ (set new attrs) before destructive ones (deletes)
- __Guard with `where`__ to avoid accidental broad effects
- __Stage in one pipeline__ before enabling everywhere

---

## 10) References

- Collector processors: transform, filter, routing (OTTL powered)
- OTTL guide and examples: OpenTelemetry Collector docs

```
Time check
- 1–2 min: What/Why
- 2–3 min: Syntax + mental model
- 2–3 min: Demo walk-through
- 1–2 min: Q&A
```
