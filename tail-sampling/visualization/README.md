# OpenTelemetry Sampling Visualization

This project provides visualizations to explain Head Sampling and Tail Sampling concepts in an OpenTelemetry architecture.

## Outputs

Running this visualization script will generate three files:

1. `head_sampling.png` - Static visualization of Head Sampling
2. `tail_sampling.png` - Static visualization of Tail Sampling
3. `sampling_demonstration.gif` - Animated demonstration contrasting both sampling methods

## Requirements

- Python 3.7+
- matplotlib
- numpy
- pillow (PIL)

## Running Locally

1. Install the required Python packages:

```
pip install -r requirements.txt
```

2. Run the visualization script:

```
python visualize_sampling.py
```

The output files will be saved in an `output` directory.

## Running with Docker

1. Build the Docker image:

```
docker build -t otel-sampling-viz .
```

2. Run the container:

```
docker run --rm -v $(pwd)/output:/app/output otel-sampling-viz
```

This will mount a volume so that the generated images are available on your host machine in the `output` directory.

## Visualization Concepts

### Head Sampling (Probabilistic Sampling)
- Decision to keep/drop traces is made at the beginning of the trace lifecycle
- Fast and efficient but may miss important traces like errors
- Sampling decision happens before the collector knows the full context

### Tail Sampling (Decision-deferred Sampling)
- Decision to keep/drop traces is made after collecting all spans for a trace
- More intelligent sampling decisions (e.g., keep all error traces)
- Requires more memory and processing resources at the collector level
