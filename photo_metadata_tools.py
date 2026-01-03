# lib for reading metadata tools from my photos

import pathlib as pl
import os

import numpy as np


def raw_photos_iterator(top_dir: pl.Path, include_dng=True, include_nef=True):
    filetypes = []

    if include_dng:
        filetypes.append("DNG")
        # filetypes.append('dng') # glob is case insensative

    if include_nef:
        filetypes.append("NEF")
        # filetypes.append('nef') # glob is case insensative

    for ext in filetypes:
        yield from top_dir.glob(f"**/*.{ext}")


def collect_raw_file_sizes(
    top_dir: pl.Path, include_dng=True, include_nef=True, assume_sub_4GiB=True
):
    """
    Docstring for collect_raw_file_sizes

    :param top_dir: Description
    :type top_dir: pl.Path
    :param include_dng: Include all DNG files in recursive search of directory
    :param include_nef: Include all NEF files in recursive search of directory
    :param assume_sub_4GiB: Assume that all raw photos are less than 4GiB (size can be correctly described by uint32_t)
    """

    arrtype = np.uint32 if assume_sub_4GiB else np.uint64
    return np.asarray(
        [
            os.path.getsize(photo_file)
            for photo_file in raw_photos_iterator(top_dir, include_dng, include_nef)
        ],
        dtype=arrtype,
    )
