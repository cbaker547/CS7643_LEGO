# models/transformer/ — Owner: C

The main model: image → bricks, one brick at a time.

```
image → encoder (models/encoder.py) → image patch features
                                          ↓ cross-attention
          [START] → transformer decoder → brick, brick, ..., [END]
```

## Tokenization

Each brick is 5 tokens: `type, x, y, z, color`, then `[END]` after the last brick.
- Separate small vocabularies per field (type ids, 0–19 for each coordinate, color ids), or one shared vocab with offsets; pick one and document it here.
- Order: bottom-up raster (z, then y, then x), as in `data/README.md`.
- Cap sequence length from A's brick-count stats.

## Model v1

- Encoder: pretrained (DINOv2 ViT-S or ResNet-50), frozen at first; cache its features to disk to save compute.
- Decoder: ~6 layers, ~256–512 hidden, cross-attends to patch features.
- Loss: cross-entropy per token.

## Constrained decoding (inference only)

Before sampling each brick, mask out choices that would:
- overlap an existing brick, or
- float (no brick under it and not on the ground layer), or
- go outside the 20³ grid.

## Interface

```python
predict(images) -> list[list[[type_id, x, y, z, color_id]]]
```

## Debugging order

1. Tokenize → detokenize round-trips exactly on the whole dataset.
2. Overfit 10 structures to near-zero loss. If it can't, something is wrong in data or masking.
3. Only then train on the full set.

## References

- BrickGPT (next-brick prediction, text-conditioned): https://arxiv.org/abs/2505.05469

## Checklist

- [ ] Week 1: tokenizer + round-trip test
- [ ] Weeks 2–3: v1 on shape only, overfit test passes, first scores
- [ ] Weeks 4–5: color, constrained decoding, encoder ablations (with D)
