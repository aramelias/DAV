# TRY THIS AT HOME:
# Welcome to the test file for Tim! Do here whatever your heart desires.

import argparse
import pandas as pd
import sys
import os
import time
import bokeh.plotting as plt
import bokeh.models as bkm
import bokeh.layouts as bkl
import bokeh
import datetime
import random
import numpy as np
from sklearn import datasets
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
import sklearn.metrics as sm

from TimsStuff.progressBar import ProgressBar
import scatter_plot

# Test for t-SNE
id_to_color = {
    1:bokeh.colors.RGB(255, 0, 0),
    2:bokeh.colors.RGB(0, 255, 0),
    3:bokeh.colors.RGB(0, 0, 255),
    4:bokeh.colors.RGB(0, 127, 127),
    5:bokeh.colors.RGB(127, 0, 127),
    6:bokeh.colors.RGB(127, 127, 0),
    7:bokeh.colors.RGB(127, 0, 0),
    8:bokeh.colors.RGB(0, 127, 0)
}

x = pd.DataFrame()
x["x"] = [1, 2, 3, 4, 5, 6, 7, 8]
x["y"] = [1, 2, 3, 4, 5, 6, 7, 8]
x["z"] = [1, 2, 3, 4, 5, 6, 7, 8]
x["lbl"] = [1, 2, 3, 4, 5, 6, 7, 8]
x["to_drop"] = [1, 2, 3, 4, 5, 6, 7, 8]
x["drop_this_too"] = [1, 2, 3, 4, 5, 6, 7, 8]

x = x.drop(["to_drop", "drop_this_too"], axis=1)

model = KMeans(n_clusters=8)
model.fit(x)
x["color"] = model.labels_

print(x)

rndperm = np.random.permutation(x.shape[0])

print(rndperm)

x_embedded = TSNE(n_components=2).fit_transform(x.values)

print(x_embedded)

new_color = []
for i in range(len(x["color"])):
    new_color.append(id_to_color[x["color"][i] + 1])

x["color"] = new_color

# Create hover tool
hover = bkm.HoverTool(tooltips=[("Label", "@lbl"), ("xy", "@xyz")])

xyz = []
for i in range(len(x["x"])):
    xyz.append(str(x["x"][i]) + "," + str(x["y"][i]) + "," + str(x["z"][i]))

data = {"x":x_embedded[:, 0], "y":x_embedded[:, 1], "color":x["color"], "xyz":xyz, "lbl":x["lbl"]}

# Create figure
f = plt.figure(title="A", x_axis_label = "B", y_axis_label = "C", tools=[hover, bkm.WheelZoomTool(), bkm.BoxZoomTool(), bkm.PanTool(), bkm.SaveTool(), bkm.ResetTool()], width=900)
f.scatter("x", "y", source=bokeh.models.ColumnDataSource(data=data), color="color", size=10)
plt.show(f)
