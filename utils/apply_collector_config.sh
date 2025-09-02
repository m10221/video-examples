#!/usr/bin/env bash
# Generic helper to apply a specific OpenTelemetry Collector config to an example
# without modifying docker-compose.yaml. It copies the provided config file into
# the example directory (default target: otel-collector-config-no-sampling.yaml)
# and restarts the collector and app services.
#
# Usage:
#   utils/apply_collector_config.sh \
#       --example-dir tail-sampling \
#       --config ./ottl-intro/otel-collector-config-ottl-demo.yaml \
#       [--target otel-collector-config-no-sampling.yaml] \
#       [--services "otel-collector order-service"] \
#       [--config-type with|no] \
#       [--no-restart]
#
# Notes:
# - By default this script sets CONFIG_TYPE=no so the volume mapping
#   ./otel-collector-config-${CONFIG_TYPE:-no}-sampling.yaml resolves to the
#   default file name in docker-compose.yaml used by tail-sampling.
# - To support other examples with different service names, use --services.

set -euo pipefail

EXAMPLE_DIR=""
CONFIG_FILE=""
TARGET_NAME="otel-collector-config-no-sampling.yaml"
SERVICES=("otel-collector" "order-service")
RESTART=true
CONFIG_TYPE=""

print_help() {
  sed -n '1,80p' "$0" | sed 's/^# \{0,1\}//'
}

# Simple arg parsing compatible with macOS bash
while [[ $# -gt 0 ]]; do
  case "$1" in
    -e|--example-dir)
      EXAMPLE_DIR="$2"; shift 2 ;;
    -c|--config)
      CONFIG_FILE="$2"; shift 2 ;;
    -t|--target)
      TARGET_NAME="$2"; shift 2 ;;
    -s|--services)
      IFS=' ' read -r -a SERVICES <<< "$2"; shift 2 ;;
    --config-type)
      CONFIG_TYPE="$2"; shift 2 ;;
    --no-restart)
      RESTART=false; shift ;;
    -h|--help)
      print_help; exit 0 ;;
    *)
      echo "Unknown argument: $1" >&2; echo; print_help; exit 1 ;;
  esac
done

if [[ -z "$EXAMPLE_DIR" || -z "$CONFIG_FILE" ]]; then
  echo "Error: --example-dir and --config are required" >&2
  echo
  print_help
  exit 1
fi

if [[ ! -d "$EXAMPLE_DIR" ]]; then
  echo "Error: example dir not found: $EXAMPLE_DIR" >&2
  exit 1
fi

# Require a compose file
if [[ ! -f "$EXAMPLE_DIR/docker-compose.yaml" && ! -f "$EXAMPLE_DIR/docker-compose.yml" ]]; then
  echo "Error: docker-compose file not found in $EXAMPLE_DIR" >&2
  exit 1
fi

if [[ ! -f "$CONFIG_FILE" ]]; then
  echo "Error: config file not found: $CONFIG_FILE" >&2
  exit 1
fi

TARGET_PATH="$EXAMPLE_DIR/$TARGET_NAME"

echo "Applying collector config:" 
echo "  Source: $CONFIG_FILE"
echo "  Target: $TARGET_PATH"

# Determine CONFIG_TYPE if not explicitly provided
CT="$CONFIG_TYPE"
if [[ -z "$CT" ]]; then
  if [[ "$TARGET_NAME" == *"with-sampling.yaml"* ]]; then
    CT="with"
  elif [[ "$TARGET_NAME" == *"no-sampling.yaml"* ]]; then
    CT="no"
  else
    CT="no" # default fallback
  fi
fi
echo "  CONFIG_TYPE (for restart): $CT"

# Copy in place
cp "$CONFIG_FILE" "$TARGET_PATH"

if [[ "$RESTART" == true ]]; then
  echo "Restarting services: ${SERVICES[*]}"
  # Ensure CONFIG_TYPE=no so volume mapping points to the default file
  (
    cd "$EXAMPLE_DIR"
    CONFIG_TYPE="$CT" docker compose stop ${SERVICES[*]} || true
    CONFIG_TYPE="$CT" docker compose up -d ${SERVICES[*]}
  )
  echo "Done. Check logs with: (cd $EXAMPLE_DIR && docker compose logs -f ${SERVICES[0]})"
else
  echo "Config copied. Skipping restart (--no-restart)."
fi
