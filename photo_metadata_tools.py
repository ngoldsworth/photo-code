# lib for reading metadata tools from my photos

import pathlib as pl

def raw_photos_iterator(top_dir:pl.Path, find_dng=True, find_nef=True):
    filetypes = []

    if find_dng:
        filetypes.append('DNG')
        # filetypes.append('dng') # glob is case insensative

    if find_nef:
        filetypes.append('NEF')
        # filetypes.append('nef') # glob is case insensative

    for ext in filetypes:
        yield from top_dir.glob(f'**/*.{ext}')