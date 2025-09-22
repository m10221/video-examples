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
- Pipeline: adds resource tags to Prometheus metrics and sends them to Splunk Observability Cloud.

What you’ll see
- In Splunk Observability Cloud: request rate (Flask), host load (Node), and NGINX requests/connections

---

# Slide 2 — Key Takeaways

 - The Collector scrapes Prometheus endpoints directly, so you don’t need to run a Prometheus server; it pulls `/metrics` and forwards to Splunk Observability Cloud.
 - The Collector acts as a single ingestion plane, so I can add or remove scrape targets centrally in one configuration file.
 - Common exporters work out of the box, including Node Exporter, the NGINX Prometheus exporter, and custom apps.
 - Consistent resource tags—such as `service.name`, `service.namespace`, and `deployment.environment`—make filtering and grouping straightforward in Splunk Observability Cloud.
 - The setup stays flexible: I can add new scrape targets and make naming/label tweaks in the Collector config instead of changing exporter containers or application code.
