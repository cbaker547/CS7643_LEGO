# Image-to-LEGO (CS 7643 Final Project)

Train a model that takes **one image of an object** and outputs **one colored LEGO structure**: a list of bricks, each with a type, a grid position, and a color.

- **Baseline:** image encoder → voxel decoder → greedy brick merge (Image2Lego-style)
- **Main model:** image encoder → transformer that places one brick at a time, with constrained decoding
- **Data:** [StableText2Brick](https://avalovelace1.github.io/BrickGPT/) (47k+ brick structures on a 20×20×20 grid), rendered to images ourselves


---

## Start here

1. Read this file, then the README in the folder you own (table below).
2. Set up the environment (see **Setup**) and run the smoke test.
3. Read the **brick format** in `data/README.md`. Everyone codes against it. Do not change it without telling the team.

## Who owns what

| Folder | Owner | What lives there |
|---|---|---|
| `data/` | A | Loading StableText2Brick, color assignment, splits, brick format spec |
| `render/` | A (B helps in week 1) | Shared renderer: training images *and* output figures |
| `models/voxel_baseline/` | B | Voxel decoder + greedy brick merge |
| `models/transformer/` | C | Tokenizer, brick transformer, constrained decoding |
| `models/encoder.py` | C (shared) | Pretrained image encoder used by both models |
| `eval/` | D | Metrics, visible/hidden IoU split, comparison tables |
| `configs/` | everyone | One YAML per experiment |
| `scripts/` | everyone | Entry points: `render.py`, `train.py`, `evaluate.py` |

## Repo layout

```
data/        loaders, color palette, splits, brick format spec
render/      shared renderer (trimesh + pyrender)
models/      encoder.py, voxel_baseline/, transformer/
eval/        metrics, visualization
configs/     experiment configs (YAML)
src/     command-line entry points
```

Large files (dataset `.arrow`, renders, checkpoints) are **not** committed. They live in the shared Google Drive folder; see `data/README.md` for where to put them locally.

## Setup

```bash
conda create -n lego python=3.11 -y
conda activate lego
pip install -r requirements.txt
python scripts/smoke_test.py   # checks GPU, loads one structure, renders one image
```

On a headless server, pyrender needs an offscreen backend:

```bash
export PYOPENGL_PLATFORM=egl   # or osmesa if EGL is unavailable
```
