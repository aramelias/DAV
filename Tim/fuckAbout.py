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


x = []
for i in range(10):
    x.append([])
    for j in range(10):
        x[i].append([])
        for k in range(10):
            x[i][j].append(i * j * k)
print(x)

x_embedded = TSNE(n_components=2).fit_transform(x)

print(x_embedded)
