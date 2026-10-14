# models/voxel_baseline/ — Owner: B

The Image2Lego-style baseline: image → voxel grid → bricks.

```
image → encoder (models/encoder.py) → 3D conv decoder → 20³ occupancy + color → greedy brick merge → brick list
```

## Pieces

1. **Voxelizer** (week 1, shared with `eval/`): brick list → 20³ occupancy grid + 20³ color grid. Put it in `eval/voxelize.py` so both folders import the same function.
2. **Decoder:** image features → 20³ logits for occupancy, plus a color class per cell.
   - Loss: binary cross-entropy on occupancy + cross-entropy on color (filled cells only).
3. **Greedy brick merge:** filled voxels → bricks. Layer by layer from the bottom, place the largest brick from our type list that fits in filled, unclaimed cells; repeat until the layer is covered.

## Interface

```python
predict(images) -> list[list[[type_id, x, y, z, color_id]]]
```

Same output format as the transformer, so `eval/` treats both models the same.

## References

- Image2Lego: https://arxiv.org/html/2108.08477v1 (Sections 2.2–2.4)

## Checklist

- [ ] Week 1: voxelizer in `eval/voxelize.py`, help A get the renderer running
- [ ] Weeks 2–3: decoder trains on shape; greedy merge works; first scores from `eval/`
- [ ] Weeks 4–5: add color head; freeze results
