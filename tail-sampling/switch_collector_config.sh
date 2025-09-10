#!/bin/bash

set -e

# Define colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Variables to track current state
CURRENT_CONFIG="with"
SPLUNK_ENABLED="false"

# Default to help if no arguments provided
if [ $# -eq 0 ]; then
    echo -e "${YELLOW}Usage:${NC} $0 [tail|no-tail|splunk-tail|splunk-no-tail|status]"
    echo
    echo "Options:"
    echo "  tail           - Switch to configuration with tail sampling"
    echo "  no-tail        - Switch to configuration without tail sampling"
    echo "  splunk-tail    - Switch to configuration with tail sampling and Splunk export"
    echo "  splunk-no-tail - Switch to configuration without tail sampling but with Splunk export"
    echo "  status         - Show current configuration"
    exit 1
fi

# Check for .env file when using Splunk options
check_splunk_env() {
    # Prefer a local .env in tail-sampling/, but fall back to repo root ../.env
    if [ -f ./.env ]; then
        ENV_PATH="./.env"
    elif [ -f ../.env ]; then
        ENV_PATH="../.env"
    else
        echo -e "${YELLOW}Error:${NC} .env file not found"
        echo "Please create a .env file at the repo root with your Splunk credentials:"
        echo "  ./video-examples/.env with:"
        echo "    SPLUNK_ACCESS_TOKEN=your-access-token"
        echo "    SPLUNK_REALM=your-realm (e.g., us1)"
        exit 1
    fi

    # Load environment variables
    # shellcheck source=/dev/null
    source "$ENV_PATH"

    # Check if required variables are set
    if [ -z "$SPLUNK_ACCESS_TOKEN" ] || [ -z "$SPLUNK_REALM" ]; then
        echo -e "${YELLOW}Error:${NC} Missing required environment variables"
        echo "Please make sure SPLUNK_ACCESS_TOKEN and SPLUNK_REALM are set in $ENV_PATH"
        exit 1
    fi
}

# Function to display status
show_status() {
    if [[ "$CURRENT_CONFIG" == "with" ]]; then
        echo -e "${BLUE}Current configuration:${NC} With tail sampling"
    else
        echo -e "${BLUE}Current configuration:${NC} No tail sampling"
    fi
    
    if [[ "$SPLUNK_ENABLED" == "true" ]]; then
        echo -e "${GREEN}Splunk export:${NC} Enabled"
        if [ -n "$SPLUNK_REALM" ]; then
            echo -e "${GREEN}Splunk realm:${NC} $SPLUNK_REALM"
        fi
    else
        echo -e "${GREEN}Splunk export:${NC} Disabled"
    fi
}

case "$1" in
    "tail")
        echo -e "${BLUE}Switching to${NC} tail sampling configuration..."
        # Preserve UX but delegate to the generic applier
        export CONFIG_TYPE=with
        export ENVIRONMENT="tail-sampling-demo"
        SPLUNK_ENABLED="false"
        ./utils/apply_collector_config.sh \
          --example-dir tail-sampling \
          --config ./tail-sampling/otel-collector-config-with-sampling.yaml \
          --target otel-collector-config-with-sampling.yaml \
          --services "otel-collector order-service" \
          --config-type with
        CURRENT_CONFIG="with"
        echo -e "${GREEN}Successfully switched to tail sampling configuration!${NC}"
        echo "Wait a moment for services to fully restart..."
        ;;
        
    "no-tail")
        echo -e "${BLUE}Switching to${NC} no tail sampling configuration..."
        export CONFIG_TYPE=no
        export ENVIRONMENT="tail-sampling-demo"
        SPLUNK_ENABLED="false"
        ./utils/apply_collector_config.sh \
          --example-dir tail-sampling \
          --config ./tail-sampling/otel-collector-config-no-sampling.yaml \
          --target otel-collector-config-no-sampling.yaml \
          --services "otel-collector order-service" \
          --config-type no
        CURRENT_CONFIG="no"
        echo -e "${GREEN}Successfully switched to no tail sampling configuration!${NC}"
        echo "Wait a moment for services to fully restart..."
        ;;
        
    "splunk-tail")
        echo -e "${BLUE}Switching to${NC} tail sampling with Splunk export..."
        # Ensure Splunk credentials then delegate to applier with Splunk config
        check_splunk_env
        export CONFIG_TYPE=with
        export ENVIRONMENT="tail-sampling-demo"
        export SPLUNK_ACCESS_TOKEN="$SPLUNK_ACCESS_TOKEN"
        export SPLUNK_REALM="$SPLUNK_REALM"
        ./utils/apply_collector_config.sh \
          --example-dir tail-sampling \
          --config ./tail-sampling/otel-collector-config-with-sampling-splunk.yaml \
          --target otel-collector-config-with-sampling.yaml \
          --services "otel-collector order-service" \
          --config-type with
        CURRENT_CONFIG="with"
        SPLUNK_ENABLED="true"
        echo -e "${GREEN}Successfully switched to tail sampling with Splunk export!${NC}"
        echo "Wait a moment for services to fully restart..."
        ;;
        
    "splunk-no-tail")
        echo -e "${BLUE}Switching to${NC} no tail sampling with Splunk export..."
        check_splunk_env
        export CONFIG_TYPE=no
        export ENVIRONMENT="tail-sampling-demo"
        export SPLUNK_ACCESS_TOKEN="$SPLUNK_ACCESS_TOKEN"
        export SPLUNK_REALM="$SPLUNK_REALM"
        ./utils/apply_collector_config.sh \
          --example-dir tail-sampling \
          --config ./tail-sampling/otel-collector-config-no-sampling-splunk.yaml \
          --target otel-collector-config-no-sampling.yaml \
          --services "otel-collector order-service" \
          --config-type no
        CURRENT_CONFIG="no"
        SPLUNK_ENABLED="true"
        echo -e "${GREEN}Successfully switched to no tail sampling with Splunk export!${NC}"
        echo "Wait a moment for services to fully restart..."
        ;;
        
    "status")
        show_status
        ;;
        
    *)
        echo -e "${YELLOW}Unknown option:${NC} $1"
        echo -e "${YELLOW}Usage:${NC} $0 [tail|no-tail|splunk-tail|splunk-no-tail|status]"
        exit 1
        ;;
esac

# No backup functionality needed

# Show status if this isn't just a status request
if [ "$1" != "status" ]; then
    echo
    show_status

    echo
    echo -e "${YELLOW}Next steps:${NC}"
    echo "1. Run './utils/generate_load.sh' to generate traces"
    echo "2. Visit Jaeger UI to see results: http://localhost:16686"
fi

# If Splunk is enabled, add Splunk-specific information
if grep -q "^    traces/splunk:" "otel-collector-config-${CONFIG_TYPE}-sampling.yaml" 2>/dev/null; then
    echo "3. View traces in Splunk Observability Cloud:"
    echo "   - Log in to your Splunk account"
    echo "   - Navigate to APM > Traces"
fi
