#!/usr/bin/env bash
# Render Manim scenes inside the visualization container
# Examples:
#   visualization/scripts/render_docker.sh otel h
#   visualization/scripts/render_docker.sh sampling m
#   visualization/scripts/render_docker.sh otel h frame   # export a PNG (uses FRAME=N if set, else last frame)
# Quality presets: l,m,h,k -> mapped to -ql,-qm,-qh,-qk

set -euo pipefail
cd "$(dirname "$0")/.."

SCENE_KEY="${1:-otel}"
QUALITY="${2:-h}"
MODE="${3:-video}"

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

# If requesting a single frame PNG export
if [[ "$MODE" == "frame" ]]; then
  # Prefer a specific frame if FRAME env is provided; else save last frame (-s)
  if [[ -n "${FRAME:-}" ]]; then
    CMD+=("--format=png" "--frame" "${FRAME}")
  else
    CMD+=("-s")
  fi
fi

# Use compose to run the command with repo mounted; outputs go to visualization/output
exec docker compose -f visualization/docker-compose.yaml run --rm manim "${CMD[@]}"
