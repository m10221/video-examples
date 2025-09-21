from flask import Flask, jsonify
from prometheus_flask_exporter import PrometheusMetrics
import time
import random

app = Flask(__name__)

# Prometheus metrics exporter attaches to /metrics by default
metrics = PrometheusMetrics(app, path="/metrics")

# App info metric
metrics.info("app_info", "Application info", version="1.0.0", service="prom-flask")

# Default endpoint
@app.route("/")
def index():
    return jsonify({"status": "ok", "service": "prom-flask"})

# Simulate variable latency and outcomes
@app.route("/checkout")
def checkout():
    # Generate a random order ID
    order_id = f"order-{random.randint(10000, 99999)}"

    # Simulate different scenarios similar to the tracing demo
    # 1. High Latency (10% chance, over 1.5 seconds)
    if random.random() < 0.1:
        time.sleep(1.6 + random.random() * 0.5)
        return (
            jsonify({
                "order_id": order_id,
                "status": "completed",
                "scenario": "high_latency",
                "message": "Checkout processed slowly"
            }),
            200,
        )

    # 2. Errors (10% chance)
    if random.random() < 0.1:
        time.sleep(0.1 + random.random() * 0.5)
        return (
            jsonify({
                "order_id": order_id,
                "status": "failed",
                "scenario": "error",
                "message": "Checkout failed: Inventory unavailable"
            }),
            500,
        )

    # 3. Normal operation
    time.sleep(0.1 + random.random() * 0.3)
    return (
        jsonify({
            "order_id": order_id,
            "status": "completed",
            "scenario": "normal",
            "message": "Checkout successful"
        }),
        200,
    )

# Health
@app.route("/healthz")
def health():
    return "ok\n", 200

if __name__ == "__main__":
    # Run on 0.0.0.0:5000 (compatible with existing generate_load.sh)
    app.run(host="0.0.0.0", port=5000)
