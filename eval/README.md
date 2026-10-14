# eval/ — Owner: D (also leads the report)

Scores any model that outputs brick lists, the same way for every model.

## Interface

```python
evaluate(pred_bricks, gt_bricks, cameras=None) -> dict   # one structure
evaluate_split(model_name, split="val") -> pandas.DataFrame   # whole split, one row per structure
```

Input: brick lists in the format from `data/README.md`.

## Metrics

| Metric | How |
|---|---|
| Voxel IoU | Voxelize both (`voxelize.py`), intersection / union of filled cells |
| Visible / hidden IoU | Split cells by whether they face the camera (needs camera params from `render/`) |
| Color accuracy | Of cells filled in both, share with the same color |
| Brick F1 | Exact match on (type, x, y, z) |
| Validity | No overlapping bricks |
| Connectivity | All bricks form one connected structure |

## Visualization

Use the shared renderer in `render/` for side-by-side figures: input image | ground truth | baseline | transformer.

## Report

- Start the report skeleton (Overleaf) in week 1, one section per owner.
- Keep a `results/` table updated as runs land so week 7 is writing, not hunting for numbers.

## Checklist

- [ ] Week 1: metric functions + unit tests on hand-made tiny structures
- [ ] Weeks 2–3: `evaluate_split` runs on both models; visible/hidden split
- [ ] Weeks 4–5: ablation tables, error analysis with C
- [ ] Weeks 6–7: figures, report
