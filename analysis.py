# analyzing photos tools
from functools import singledispatch
import pathlib as pl
import PIL.Image

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from sklearn.cluster import KMeans


# @singledispatch
def get_color_palette(img:PIL.Image, downsample_size: int = -1, clusters: int = 5):
    if downsample_size > 0:
        img = img.resize((downsample_size, downsample_size))
    # convert to RGB, reshape as list of pixels
    pixels = np.array(img).reshape(-1, 3)
    model = KMeans(n_clusters=clusters, n_init='auto')
    model.fit(pixels)

    colors = model.cluster_centers_.astype(int)
    return colors