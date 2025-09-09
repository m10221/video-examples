Slide 1 — Title
OTTL (OpenTelemetry Transformation Language)
A 5–10 minute intro + live demo

Notes:
- Goal: show how OTTL transforms telemetry in the Collector without app changes.

---

Slide 2 — Why OTTL?
- Unified language to transform/filter/route telemetry in the Collector
- Simple statements + where conditions
- Works across contexts (span, resource, logs, metrics)
- Incremental adoption: no app redeploy

Notes:
- Emphasize “ETL for telemetry” at the Collector.

---

Slide 3 — Where OTTL is used
- transform processor: mutate/enrich/normalize
- filter processor: include/exclude with conditions
- routing processor: conditional fan-out

Notes:
- Today we focus on transform.

---

Slide 4 — Mental model
Application → Receiver → [Transform (OTTL)] → Tail Sampling → Exporter → Backend
(OTTL runs in processors inside the Collector)

Notes:
- Keep pipeline clear; OTTL affects data before export.

---

Slide 5 — Syntax quick hits
- set(attributes["key"], "value")
- set(name, "new span name")
- delete_key(attributes, "old")
- ... where attributes["scenario"] == "error"
- context: resource → attributes[...] targets resource attributes

Notes:
- Keep examples short; show “where”.

---

Slide 6 — Resource vs Span (why two contexts?)
- Resource = who/where produced it (service.name, version, environment)
- Span = what happened this time (request-scoped data)
- Why resource? Consistent cross-signal tags, less duplication, filterable dimensions
- Splunk note: adding service.namespace adds a tag; service identity still comes from service.name

Notes:
- This clarifies why some rules are resource-level.

---

Slide 7 — Demo setup
- Shared Flask service (apps/order-service-flask)
- Emits spans with: scenario, order.id, customer.id, issue_detected ("true")
- Collector applies OTTL transform (ottl-intro/otel-collector-config-ottl-demo.yaml)
- Export to Jaeger (local)

Notes:
- Stress no app code changes to demo OTTL.

---

Slide 8 — What the transform does (span context)
- Marks transformed spans: demo.ottl = "applied"
- Normalizes type: issue_detected "true" → true (boolean)
- Derives label: scenario_group = "unhappy" for error/high_latency
- Improves readability: rename span → "checkout - ERROR" on errors

Notes:
- These are visible in Jaeger/collector logs.

---

Slide 9 — What the transform does (resource context)
- Adds service.namespace = "tail-sampling-demo"
- Propagates env = deployment.environment (if present)

Notes:
- Resource-level = producer identity enrichment.

---

Slide 10 — Running the demo (Compose)
- Start stack: (cd tail-sampling && docker compose up -d)
- Apply config: ./utils/apply_collector_config.sh --example-dir tail-sampling --config ./ottl-intro/otel-collector-config-ottl-demo.yaml --services "otel-collector"
- Optional shared app: (cd tail-sampling && docker compose -f docker-compose.yaml -f docker-compose.order-service-shared.override.yaml up -d --build order-service)
- Generate load: (cd tail-sampling && ./generate_load.sh 100 0.05)

Notes:
- Keep commands copyable from slides.

---

Slide 11 — What to look for
- In Jaeger: service "no-order-service"
- On spans: demo.ottl=applied, issue_detected=true (boolean), scenario_group=unhappy
- Span name becomes "checkout - ERROR" on error
- In collector logs: lines showing these attributes and renamed spans

Notes:
- Show a quick before/after span screenshot if possible.

---

Slide 12 — Key takeaways
- OTTL = conditional, safe, in-flight telemetry transformation
- Normalize, enrich, derive labels without touching app code
- Works across span/resource/log/metric contexts
- Great for hygiene, consistency, and routing decisions

Notes:
- End with how this scales across teams/environments.
