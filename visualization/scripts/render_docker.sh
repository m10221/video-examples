#!/usr/bin/env bash
# Render Manim scenes inside the visualization container
# Examples:
#   visualization/scripts/render_docker.sh otel h
#   visualization/scripts/render_docker.sh sampling m
# Quality presets: l,m,h,k -> mapped to -ql,-qm,-qh,-qk

set -euo pipefail
cd "$(dirname "$0")/.."

SCENE_KEY="${1:-otel}"
QUALITY="${2:-h}"

case "$QUALITY" in
  l|m|h|k) : ;; 
  *) echo "Invalid quality: $QUALITY (use l|m|h|k)" >&2; exit 1;;
esac

# Map scene key to file and class
case "$SCENE_KEY" in
  otel)
    FILE="visualization/scenes/otel_pipeline.py"
    CLASS="OTelPipelineScene"
    ;;
  sampling)
    FILE="visualization/scenes/tail_sampling.py"
    CLASS="TailSamplingComparison"
    ;;
  *)
    echo "Unknown scene key: $SCENE_KEY (use otel|sampling)" >&2
    exit 1
    ;;
fi

CMD=("manim" "-p" "-q${QUALITY}" "$FILE" "$CLASS")

# Use compose to run the command with repo mounted; outputs go to visualization/output
exec docker compose -f visualization/docker-compose.yaml run --rm manim "${CMD[@]}"
