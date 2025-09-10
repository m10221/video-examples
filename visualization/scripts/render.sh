#!/usr/bin/env bash
# Convenience wrapper to render common Manim scenes
# Usage:
#   visualization/scripts/render.sh otel [quality]
#   visualization/scripts/render.sh sampling [quality]
# Quality presets: l (low), m (medium), h (high), k (4k). Default: h

set -euo pipefail

SCENE="${1:-}"
QUALITY_FLAG="-q${2:-h}"

if ! command -v manim >/dev/null 2>&1; then
  echo "Error: manim not found. Activate your venv and install requirements:" >&2
  echo "  python3 -m venv .venv && source .venv/bin/activate && pip install -r visualization/requirements.txt" >&2
  exit 1
fi

case "$SCENE" in
  otel)
    manim -p ${QUALITY_FLAG} visualization/scenes/otel_pipeline.py OTelPipelineScene
    ;;
  sampling)
    echo "TailSamplingComparison scene not yet implemented. Coming soon."
    ;;
  *)
    echo "Usage: $0 {otel|sampling} [l|m|h|k]" >&2
    exit 1
    ;;
fi
