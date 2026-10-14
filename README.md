# Image-to-LEGO (CS 7643 Final Project)

Train a model that takes **one image of an object** and outputs **one colored LEGO structure**: a list of bricks, each with a type, a grid position, and a color.

- **Baseline:** image encoder → voxel decoder → greedy brick merge (Image2Lego-style)
- **Main model:** image encoder → transformer that places one brick at a time, with constrained decoding
- **Data:** [StableText2Brick](https://avalovelace1.github.io/BrickGPT/) (47k+ brick structures on a 20×20×20 grid), rendered to images ourselves

Project plan, timeline, and task flow live in the shared plan doc.

---

## Start here

1. Read this file, then the README in the folder you own (table below).
2. Set up the environment (see **Setup**) and run the smoke test.
3. Read the **brick format** in `data/README.md`. Everyone codes against it. Do not change it without telling the team.
4. Pick up your week-1 tasks from the GitHub Projects board.

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
scripts/     command-line entry points
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

## Working rules

- **Branches:** one branch per task (`a/render-v0`, `c/tokenizer`). Merge to `main` through small pull requests; one teammate glances at each.
- **`main` always runs.** If you break the smoke test, fix it before anything else.
- **Interfaces over internals.** Your folder can change freely; the brick format and the function signatures other folders call should not change without a heads-up in the group chat.
- **Experiments are configs.** Every training run has a YAML in `configs/` and is logged to the shared Weights & Biases project. A result without a config is not reported.
- **Weekly sync:** 30 minutes, same time each week. Bring: what's done, what's blocked, what you need from someone else.

## Week-1 goal: hello-world end to end

Push 10 structures through the whole pipeline: load → render → dummy model (outputs a random brick) → metrics → rendered output. It's useless as a model, but it proves every handoff works.
