import pathlib as pl

from collections import Counter
from itertools import chain

photo_raw_gericault = pl.Path(r"D:\PHOTOGRAPHY_RAW")
photo_raw_ssd = pl.Path(r"W:\NELSON\Photog_raw_CURRENT")

counting_dir = photo_raw_gericault #/ '2022'
# counting_dir = photo_raw_ssd / '2025'

dirchain = chain(
    counting_dir.glob('**/*.nef'),
    counting_dir.glob('**/*.dng'),
    counting_dir.glob('**/*.NEF'),
    counting_dir.glob('**/*.DNG'),
)

ctr = Counter()
for p in dirchain:
    ctr[p.suffix.upper()] += 1

print(f' in folder {counting_dir}:')
tot = sum(v for v in ctr.values())
for k, v in ctr.items():
    print(f'{k:>5}: {v:>6} ({v/tot:.1%})')