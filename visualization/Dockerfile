# Container for rendering Manim scenes without a local venv
# Usage via docker-compose.yml in this directory

FROM python:3.10-slim

# Install system dependencies (ffmpeg required by Manim)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps
RUN pip install --no-cache-dir manim==0.18.1

# Default workdir where the repository will be mounted
WORKDIR /workspace

# Default entrypoint is manim; args provided by compose wrapper
ENTRYPOINT ["manim"]
