# Slide 1 — Prometheus Receiver with the OpenTelemetry Collector

Title: Push Prometheus Metrics to Splunk Observability Cloud (OTel Collector)

What & Why
 - The OpenTelemetry Collector can scrape Prometheus endpoints via the Prometheus receiver (no Prometheus server required).
 - It centralizes ingestion, enrichment, and export of metrics to Splunk Observability Cloud.
 - It works with any Prometheus-compatible target (apps or exporters).

How we’ll demo it
 - Data sources:
  - Custom Flask app exposing /metrics (via prometheus_flask_exporter)
  - NGINX via nginx-prometheus-exporter (scrapes /stub_status)
  - Node Exporter for host/system metrics
 - The Collector adds resource tags to Prometheus metrics and sends them to Splunk Observability Cloud.

What you’ll see
- In Splunk Observability Cloud, you’ll see quick charts for request rate (Flask), active connections (NGINX), and average node load (Node Exporter).

---

# Slide 2 — Key Takeaways

 - You can use the Collector to scrape Prometheus endpoints directly, eliminating the need to run a Prometheus server; it pulls `/metrics` and forwards to Splunk Observability Cloud.
 - The Collector acts as a single ingestion plane, allowing you to add or remove scrape targets centrally in one configuration file.
 - Common exporters work out of the box, including Node Exporter, the NGINX Prometheus exporter, and custom apps.
 - Consistent resource tags—such as `service.name`, `service.namespace`, and `deployment.environment`—make filtering and grouping straightforward in Splunk Observability Cloud.
 - The setup stays flexible: you can add new scrape targets and make naming/label tweaks in the Collector config instead of changing exporter containers or application code.
