import os
from datasets import Dataset
from pathlib import Path
import pandas as pd
import re
import numpy as np
BRICK_RE = re.compile(r"(\d+)x(\d+)\s*\((\d+),\s*(\d+),\s*(\d+)\)")
ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = Path(os.environ.get("LEGO_DATA_DIR", ROOT / "data"))
def parse_bricks(text:str)->list[tuple[int,int,int,int,int]]:
    x= re.findall(BRICK_RE,text)
    return [tuple(int(v) for v in i) for i in x]

    
def check_convention(bricks, swap_axes=False):
    """bricks: list of (H, W, x, y, z).
    Hypothesis A (swap_axes=False): (x,y,z) is the min corner, H runs along x, W along y.
    Hypothesis B (swap_axes=True):  same, but H runs along y, W along x.
    Returns (n_out_of_bounds, n_overlap_cells)."""
    grid = np.zeros((20, 20, 20), dtype=np.int16)
    n_oob = 0
    n_overlap = 0
    for H, W, x, y, z in bricks:
        if swap_axes:
            H,W=W,H
        if (x+H)>20 or (y+W)>20 or x<0 or y<0 or z<0 or z>=20:
            n_oob+=1
            continue

        if np.all(grid[x:x+H,y:y+W,z]==0) :
            grid[x:x+H,y:y+W,z]=1
        else:
            n_overlap+=1


    return n_oob, n_overlap

def is_ascending(tuple,idx):
    values=[tup[idx] for tup in tuple]
    return all(x<=y for x,y in zip(values,values[1:]))
def min_z(tuple,idx):
    values=[tup[idx] for tup in tuple]
    return min(values)

def inspect(file_path):

    ds = Dataset.from_file(str(file_path))
    if "stability_scores" in ds.column_names:
        ds = ds.remove_columns("stability_scores")
    df=ds.to_pandas()
    # assert parse_bricks("2x6 (13,12,0)\n1x1 (15,17,0)\n") == [(2, 6, 13, 12, 0), (1, 1, 15, 17, 0)]
    # ("2x6 (13,12,0)== [(2, 6, 13, 12, 0)]
    df['bricks']=df['bricks'].apply(parse_bricks)

    #H and W check aligning with x and y
    res_a = df['bricks'].apply(lambda b: check_convention(b, swap_axes=False))
    a=pd.DataFrame(res_a.to_list(),columns=['n_oob','n_overlap'])
    res_b = df['bricks'].apply(lambda b: check_convention(b, swap_axes=True))
    b=pd.DataFrame(res_b.to_list(),columns=['n_oob','n_overlap'])

    #Confirmed that bricks min corner is first number HXW runs along
    #For arrow Train_0
    # n_oob        0
    # n_overlap    0
    # dtype: int64
    # n_oob        7075
    # n_overlap    6939

    #Checking whether z's are ascending
    is_asc=(df['bricks']).apply(lambda lst: is_ascending(lst,4)).all()
    out=f'Default Axis:\n{(a>0).sum()}'
    outFlip=f'Flipped Axis:\n{(b>0).sum()}'
    tot=f'total items: {len(df)}'
    z=f'Z values ascending?: {is_asc}'
    ground=(df['bricks']).apply(lambda lst: min_z(lst,4))
    print(tot)
    print(out)
    print(outFlip)
    print(z)

    order={'z, y, x ascending':df['bricks'].apply(lambda b: b == sorted(b, key=lambda t: (t[4], t[3], t[2]))).mean() 
    ,'z, x, y ascending':df['bricks'].apply(lambda b: b == sorted(b, key=lambda t: (t[4], t[2], t[3]))).mean() 
    ,'z ascending, then x and y descending':df['bricks'].apply(lambda b: b == sorted(b, key=lambda t: (t[4], -t[2], -t[3]))).mean()}
    print(f'Ordering of dimensions :{max(order,key=order.get)}')

    
    print(f'Minimum Value z=0? {(ground==0).all()}')
    return df

def main():
    # ROOT = Path(__file__).resolve().parents[1]  
    # file_path = ROOT / "data" / "raw" / "StableText2Brick" / "train"/"data-00000-of-00006.arrow"
    # BRICK_RE = re.compile(r"(\d+)x(\d+)\s*\((\d+),\s*(\d+),\s*(\d+)\)")

    train_path=DATA_DIR / 'raw'/'StableText2Brick'/'train'
    test_path=DATA_DIR / 'raw'/'StableText2Brick'/'test'
    train_paths = sorted([(str(file.resolve()),file.stem) for file in train_path.glob("*.arrow")])
    test_paths = sorted([(str(file.resolve()),file.stem) for file in test_path.glob("*.arrow")])
    assert train_paths, f'No.arrow files found in {train_path}'
    assert test_paths, f'No.arrow files found in {test_path}'
    print(f'Found {len(train_paths)} train and {len(test_paths)} test items')

    for file,name in (train_paths):
        print(name)
        df=inspect(file)
        out = DATA_DIR  / "raw_shrunk" / 'train'/ f"{name}.parquet"
        out.parent.mkdir(parents=True, exist_ok=True)
        df.to_parquet(out)   

    for file,name in (test_paths):
        print(name)
        df=inspect(file)
        out = DATA_DIR  / "raw_shrunk" / 'test' /f"{name}.parquet"
        out.parent.mkdir(parents=True, exist_ok=True)
        df.to_parquet(out)   



if __name__ == '__main__':
    main()