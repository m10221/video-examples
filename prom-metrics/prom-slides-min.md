# Slide 1 — Prometheus Receiver with the OpenTelemetry Collector

Title: Push Prometheus Metrics to Splunk Observability Cloud (OTel Collector)

What & Why
- The OTel Collector can scrape Prometheus endpoints via the Prometheus receiver (no Prometheus server required)
- Centralizes ingestion, enrichment, and export of metrics to Splunk Observability Cloud
- Works with any Prometheus-compatible target (apps or exporters)

How we’ll demo it
- Sources:
  - Custom Flask app exposing /metrics (via prometheus_flask_exporter)
  - NGINX via nginx-prometheus-exporter (scrapes /stub_status)
  - Node Exporter for host/system metrics
- Collector pipeline (high level):
  Prometheus receiver(s) -> resource tagging (service.name, service.namespace, environment) -> Signalfx exporter -> Splunk Observability Cloud

What you’ll see
- In Splunk Observability Cloud: request rate and latency (Flask), host load (Node), and NGINX requests/connections

---

# Slide 2 — Key Takeaways

- Prometheus scraping without running Prometheus: the Collector pulls /metrics directly
- One ingestion plane: add or remove targets centrally in Collector config
- Familiar exporters work out of the box: Node Exporter, NGINX exporter, custom apps
- Clean resource context: consistent filters via service.name, service.namespace, environment
- Fast validation: curl endpoints locally; confirm in Metric Finder; build a couple of high-signal charts
- Extensible: add more targets or processors later (transforms, aggregation) without changing apps
