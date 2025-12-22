
import pathlib as pl
import os
import time
import datetime as dt

from collections import Counter
from itertools import chain

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np

hist = Counter()

photo_raw_gericault = pl.Path(r"D:\photo-archive")
photo_raw_ssd = pl.Path(r"W:\NELSON\photo-current") / '2025'

gen_chain = [k for k in chain(
    # photo_raw_gericault.glob('**/*.nef'),
    # photo_raw_gericault.glob('**/*.NEF'),
    # photo_raw_gericault.glob('**/*.dng'),
    # photo_raw_gericault.glob('**/*.DNG'),
    photo_raw_ssd.glob('**/*.nef'),
    photo_raw_ssd.glob('**/*.NEF'),
    photo_raw_ssd.glob('**/*.dng'),
    photo_raw_ssd.glob('**/*.DNG'),
)]
    
sizes = np.asarray([os.path.getsize(photo) for photo in gen_chain], dtype=np.uint64)
ct = len(sizes)

print(f'{ct} photos found')

## folders with most NEFs vs DNGs
nef_counter = Counter()
dng_counter = Counter()

for photo in gen_chain:
    if photo.suffix.upper() == '.NEF':
        for d in photo.parents:
            nef_counter[d] += 1
    
    if photo.suffix.upper() == '.DNG':
        for d in photo.parents:
            dng_counter[d] += 1

print('----NEF----')
for k,v in nef_counter.items():
    print(f'{v}: {k}')

print('----DNG----')
for k,v in dng_counter.items():
    print(f'{v}: {k}')

print(f'total dng: {dng_counter.total()}')
print(f'total nef: {nef_counter.total()}')

tot_mib = sum(sizes) / 1024**2
print(f'{int(tot_mib+1):,}MiB total')
print(f'{tot_mib/ct:.2f}MiB on average')

h, e = np.histogram(sizes, bins=10000, range=(0,1e8))
h_norm = h.astype(float)/ h.sum()
e /= 1024**2

fig, ax = plt.subplots(1,1)
centers = e[:-1] + (0.5)*(e[4]-e[3])
ax.plot(centers, h_norm.cumsum())

fig2, ax2 = plt.subplots(1,1)
ax2.bar(centers, h_norm)

avg_size = tot_mib/len(sizes)
ax.set_title(f'{avg_size:.3f}')
# ax.set_yscale('log')
plt.show()

d750px = 4000 * 6000
dz7ii = 8256 * 5504

print(avg_size * dz7ii / d750px)