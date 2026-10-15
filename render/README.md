# render/ — Owner: A (B helps in week 1)

One renderer, two jobs:
1. **Training images:** ground-truth brick lists → images.
2. **Output figures:** predicted brick lists → images, drawn the same way so predictions and ground truth compare side by side.

Built on `trimesh` (one box mesh per brick) + `pyrender` (offscreen rendering).

## Interface (other folders call this; keep it stable)

```python
render_structure(
    bricks,            # list of [type_id, x, y, z, color_id]
    camera,            # dict: azimuth, elevation, distance (degrees / grid units)
    size=224,          # output image is size x size
    background=None,   # RGB tuple or None for default
) -> np.ndarray        # H x W x 3 uint8
```

## How bricks become meshes

- Brick footprint from `type_id` (e.g. 2x4 → 2 by 4 studs), height = 1 layer.
- Shrink each box slightly (e.g. 2% per side) so edges between bricks are visible.
- Color from the palette in `data/README.md`.
- Studs (small cylinders on top) are optional; add them only once everything else works.

## Training-image settings (v0)

- 224 × 224 px
- 2 views per structure for hello-world; 4–8 for the full set
- Random azimuth 0–360°, elevation 15–45°
- Mild lighting variation; plain backgrounds first, varied later
- Save the camera parameters with each image (needed for the visible/hidden IoU split in `eval/`)

## Output layout

```
renders/{split}/{structure_id}_{view}.png
renders/{split}/cameras.parquet     # structure_id, view, azimuth, elevation, distance
```

`renders/` is gitignored and lives on the shared Drive.

