# data/ — Owner: A

Loads StableText2Brick, assigns colors, builds splits, and defines the **brick format** everyone codes against.

## Where the data lives

- Source: StableText2Brick `.arrow` files (~3 GB), in the shared Google Drive folder.
- Local copy: put them in `data/raw/` (gitignored).
- Processed output: `data/processed/` (gitignored).

Read the `.arrow` files with Hugging Face `datasets`:

```python
from datasets import Dataset
ds = Dataset.from_file("data/raw/train/data-00000-of-00001.arrow")
df = ds.to_pandas()
print(df.columns, len(df))
```

## Brick format (DRAFT, freeze by end of week 1)

**Grid**
- 20 × 20 × 20. `x`, `y` are horizontal in studs; `z` is up, in brick layers. All integers, 0–19.
- A brick's position is its **minimum corner** (lowest x, y, z). Verify against a few dataset samples and update this line if the dataset uses something else.

**Brick type**
- Keep the dataset's dimension string (e.g. `2x4`). Orientation is in the order: `2x4` and `4x2` are different types. No rotation flag needed.
- Map each string to an integer `type_id` using the table in `brick_types.csv` (to be generated from the data).

**Color**
- Integer `color_id` from the palette below. We use LDraw color codes so an LDraw export stays possible later.

| color_id | Name |
|---|---|
| 0 | Black |
| 1 | Blue |
| etc | TBD |

(Edit this list as needed, keep it short.)

**Order**
- Bricks sorted bottom-up: by `z`, then `y`, then `x`.

**Storage**
- One Parquet file per split: `data/processed/{train,val,test}.parquet`
- One row per structure: `structure_id`, `caption`, `category` (if available), `bricks` = list of `[type_id, x, y, z, color_id]`.

## Splits

- Use the dataset's existing train/test split.
- **Validation:** carve 5–10% of *train* off with a fixed random seed. Do not take it from test.
- Save the split ID lists to `data/splits/` and commit them so everyone uses the same split.
