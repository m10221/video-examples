FROM python:3.9-slim

WORKDIR /app

# Install required dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libfreetype6-dev \
    pkg-config \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the visualization script
COPY visualize_sampling.py .

# Create output directory
RUN mkdir -p /app/output

# Run the script
CMD ["python", "visualize_sampling.py"]
