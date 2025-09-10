# Visualization (Manim)

Presentation-ready animations for tutorials and slide decks, built with Manim.

## Prereqs

- Python 3.10+
- System packages: ffmpeg (required), LaTeX optional (for advanced text rendering)
- Install Python deps:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r visualization/requirements.txt
```

## Quick Start

Render a sample scene (OTel pipeline):

```bash
# From repo root (recommended)
source .venv/bin/activate  # if not already
manim -pqh visualization/scenes/otel_pipeline.py OTelPipelineScene
```

- `-pqh` = preview, high quality, faster. For production: `-p -qk` or `-p -qm`.
- Videos will be saved under `media/videos/scenes/` by default.

## Common Scenes

- `OTelPipelineScene` (`visualization/scenes/otel_pipeline.py`)
  - Animated diagram: Application → Collector → Processors → Exporters → Backend
  - Highlights OTTL and Tail Sampling processors
- `TailSamplingComparison` (`visualization/scenes/tail_sampling.py`)
  - Side-by-side before/after sampling visualization

## Render Scripts

A convenience wrapper is provided:

```bash
# Render OTel Pipeline (preview, high)
visualization/scripts/render.sh otel

# Render Tail Sampling comparison
visualization/scripts/render.sh sampling
```

## Tips

- Customize colors and fonts in the scene files for brand alignment.
- Export a single still frame (thumbnail): add `--format=png --frame 120` to the Manim command.
- For slide decks, embed short loops (3–8s) with `-qk` or `-qm` quality for balance.

## Troubleshooting

- If you see "ffmpeg not found": install ffmpeg via Homebrew on macOS: `brew install ffmpeg`.
- If fonts/text look off, try using Manim's `MarkupText` or set a specific system font in the scenes.
