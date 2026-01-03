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

def colorwheel(img, N=60, bottom=1):
    image_arr = np.asarray(img)
    hsv_arr = np.asarray(img.convert('HSV'))
    hue = hsv_arr[:,:,0] * np.pi / 180

    theta = np.linspace(0.0,2*np.pi, N, endpoint=True) #bins
    heights, edges = np.histogram(hue, bins = N)

    heights = 10* np.asarray(heights, dtype=np.float64) / float(sum(heights)) 
    width = (2*np.pi) / N

    fig, ax = plt.subplots(1,1)
    ax = plt.subplot(111, polar=True)
    bars = ax.bar(theta, heights, width=width, bottom=bottom)

    # Use custom colors and opacity
    for r, bar in zip(theta, bars):
        bar.set_facecolor(plt.cm.hsv(bar.get_x()/(2*np.pi)))
        bar.set_alpha(1.0)

    return fig, ax