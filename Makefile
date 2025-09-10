# Make targets for visualization rendering (Manim)
# Usage examples:
#   make viz-build           # Build the Manim container
#   make viz                 # Render OTel pipeline in container (high quality)
#   make viz Q=m             # Render OTel pipeline in container (medium quality)
#   make viz-sampling        # Render TailSampling (placeholder)
#   make viz-local           # Render locally using host manim (venv)
#   make viz-clean           # Remove visualization outputs

Q ?= h

.PHONY: help
help:
	@echo "Available targets:"
	@echo "  viz-build        Build container for Manim rendering"
	@echo "  viz              Render OTel pipeline in container (quality via Q=l|m|h|k, default h)"
	@echo "  viz-sampling     Render TailSampling scene in container (placeholder)"
	@echo "  viz-local        Render locally (requires manim installed on host)"
	@echo "  viz-clean        Remove visualization output artifacts"

.PHONY: viz-build
viz-build:
	cd visualization && docker compose build

.PHONY: viz
viz:
	visualization/scripts/render_docker.sh otel $(Q)

.PHONY: viz-sampling
viz-sampling:
	visualization/scripts/render_docker.sh sampling $(Q)

.PHONY: viz-local
viz-local:
	visualization/scripts/render.sh otel $(Q)

.PHONY: viz-clean
viz-clean:
	rm -rf visualization/output || true
	rm -rf media || true
