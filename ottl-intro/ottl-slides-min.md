Slide 1 — What is OTTL? (and what it can do)
OpenTelemetry Transformation Language (OTTL) lets you transform, filter, and route telemetry inside the Collector—without changing application code.

What it can do (examples):
* Add intent markers for QA and canary rollouts, such as setting transform.applied = true, so you can instantly filter and verify rollouts.
* Normalize types and names so filters, policies, and sampling rules evaluate correctly; for example, convert the strings "true" and "false" to booleans and unify attribute keys.
* Derive categorical labels that simplify queries and SLOs, such as outcome_group or latency_bucket, so dashboards and alerts rely on stable buckets.
* Make spans easier to scan and search by including outcome or operation category in the span name to speed triage.
* Enrich producer identity with stable resource tags such as namespace, environment, team, and region to enable consistent filtering and routing across signals.

Key points:
* OTTL runs in Collector processors, such as transform, filter, and routing.
* It uses small, readable statements with where conditions.
* It works across contexts including span, resource, logs, and metrics.

Notes:
Think “ETL for telemetry” in the pipeline before export.

---

Slide 2 — Why use OTTL? (vs. alternatives)
Why OTTL:
* Centralize hygiene and enrichment in the Collector and enforce standards across teams, so you can ship versioned, reversible changes instantly.
* Exercise control before export so you can influence routing, sampling, PII scrubbing, and costs, not just dashboards.
* Make changes safer and more deterministic by guarding with where conditions, and use error_mode: ignore for resilience.

Without OTTL, you would:
* Touch many services to fix types and names, coordinate redeploys across teams, and risk configuration drift.
* Build and maintain custom processors or sidecars, which adds operational burden and inconsistency.
* Depend on backend mapping rules that run after ingestion, which is too late for tail sampling or routing and can create vendor lock‑in.
* Run ad‑hoc cleanup scripts that are after the fact, inconsistently applied, and invisible to operators.

Notes:
Emphasize time-to-fix and consistency across teams.

---

Slide 3 — Demo plan (what we will show)
Using the shared Flask app (apps/order-service-flask):
* Apply the OTTL config via utils/apply_collector_config.sh.
* Generate load and view spans in Jaeger (service: no-order-service).
Observe:
* A marker attribute that confirms transforms are active and lets you filter affected traffic.
* A string‑to‑boolean normalization so filters, policies, and sampling rules are reliable across services.
* A derived label that groups problematic requests to accelerate triage and KPI reporting.
* A span name that surfaces critical context, such as an error state, for faster visual scanning and search.
* Resource‑level tags such as environment, namespace, or team for consistent filtering and policy scoping across traces, metrics, and logs.

Demo steps (Compose):
* Start the stack and apply the OTTL config via utils/apply_collector_config.sh.
* Generate load and view spans in Jaeger (no-order-service).
* Observe the attributes and any renamed spans in the UI and the collector logs.

Notes:
Emphasize: no app code changes needed.

---

Slide 4 — Key takeaways
* OTTL provides safe, conditional, in‑flight telemetry transformation in the Collector.
* It standardizes telemetry semantics centrally without requiring application redeploys.
* It works across span, resource, log, and metric contexts to keep signals consistent.
* It improves queryability, accelerates incident response, and enables precise routing, sampling, and redaction before export.

Notes:
Invite next steps: adopt a transform stage in your standard pipelines.
