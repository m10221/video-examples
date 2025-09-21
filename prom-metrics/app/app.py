from flask import Flask, jsonify, request
from prometheus_flask_exporter import PrometheusMetrics
import time
import random

app = Flask(__name__)

# Prometheus metrics exporter attaches to /metrics by default
metrics = PrometheusMetrics(app, path="/metrics")

# Custom metrics
metrics.info("app_info", "Application info", version="1.0.0", service="prom-flask")

# Default endpoint
@app.route("/")
def index():
    return jsonify({"status": "ok", "service": "prom-flask"})

# Simulate variable latency and outcomes
@app.route("/work")
def work():
    mode = request.args.get("mode", "normal")

    # Randomize a bit even in normal
    base = 0.05
    extra = 0.0
    status = 200

    if mode == "slow":
        extra = 1.2
    elif mode == "error":
        status = 500
    elif mode == "spiky":
        extra = random.choice([0.0, 0.4, 0.8, 1.0])

    time.sleep(base + extra)

    payload = {
        "mode": mode,
        "status": status,
        "latency_ms": int((base + extra) * 1000),
    }
    return (jsonify(payload), status)

# Health
@app.route("/healthz")
def health():
    return "ok\n", 200

if __name__ == "__main__":
    # Run on 0.0.0.0:8000
    app.run(host="0.0.0.0", port=8000)
