import pathlib as pl
import os
import time
import datetime as dt

from collections import Counter
from itertools import chain

from PIL import Image
import PIL.ExifTags

import matplotlib.pyplot as plt

hist = Counter()

photo_raw_gericault = pl.Path(r"D:\PHOTOGRAPHY_RAW")
photo_raw_ssd = pl.Path(r"W:\NELSON\Photog_raw_CURRENT")

testdir = pl.Path(r'W:\NELSON\Photog_raw_CURRENT\2025\2025_03')
testchain = chain(
    testdir.glob('**/*.nef'),
    testdir.glob('**/*.NEF'),
    testdir.glob('**/*.dng'),
    testdir.glob('**/*.DNG'),
)
print(sum(1 for p in testchain))

gen_chain = chain(
    # photo_raw_gericault.glob('**/*.nef'),
    photo_raw_gericault.glob('**/*.NEF'),
    # photo_raw_gericault.glob('**/*.dng'),
    photo_raw_gericault.glob('**/*.DNG'),
    # photo_raw_ssd.glob('**/*.nef'),
    photo_raw_ssd.glob('**/*.NEF'),
    # photo_raw_ssd.glob('**/*.dng'),
    photo_raw_ssd.glob('**/*.DNG'),

)

nef_count = 0
dng_count = 0
for photo in gen_chain:
    t = os.path.getctime(photo)
    st = time.localtime(t)
    hist[(st.tm_year, st.tm_mon)] += 1
    # hist[mnth] += 1

    exif_raw = Image.open(photo).getexif()
    exif = {
            PIL.ExifTags.TAGS[k]: v
            for k, v in exif_raw.items()
            if k in PIL.ExifTags.TAGS
    }
    ts = dt.datetime.strptime(exif['DateTime'], '%Y:%m:%d %H:%M:%S')

    # if photo.suffix.upper() == 'NEF':
    #     print(photo)

    if photo.suffix.upper() == '.NEF':
        nef_count += 1
        # print(photo.parent)
        # print(photo.stem)
    elif photo.suffix.upper() == '.DNG':
        dng_count += 1


    # hist[(ts.year, ts.month)] += 1
tot = dng_count + nef_count
print(tot)
print(f'dng: {dng_count:>8} ({dng_count/tot:6>.2%})')
print(f'nef: {nef_count:>8} ({nef_count/tot:6>.2%})')

fix, ax = plt.subplots(1)

months = sorted(hist.keys())
labels = [f'{yr}-{mn}' for yr, mn in months]
counts = [hist[m] for m in months]

p = ax.bar(labels, counts)
ax.set_xlabel('Month')
ax.set_ylabel('Pictures Taken')
ax.bar_label(p, label_type='edge')
plt.show()

