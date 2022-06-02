# %%
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.ndimage.filters import gaussian_filter
import ternary
import numpy as np
import pandas as pd
from math import isnan
from ternary.helpers import simplex_iterator

data = pd.read_csv(
    "/Users/aymericvie/Documents/GitHub/evology/evology/research/icml/data/data_test.csv"
)

# data = data[data["Gen"] > 7000]

sns.set(font_scale=1)
fontsize = 18
scale = 25  # from the experiment.py

# %%
# We want a simplex plot of strategy returns.
threshold = 1
data_group = data.groupby(["WS_VI", "WS_TF", "WS_NT"], as_index=False).mean()


def generate_random_heatmap_data(scale):
    nt_ws = dict()
    l = 0
    for (i, j, k) in simplex_iterator(scale):
        nt_ws[(i, j)] = data_group.loc[l, "Test"]

        l += 1
    return nt_ws


nt_r = generate_random_heatmap_data(scale)

figure, tax = ternary.figure(scale=scale)
figure.set_size_inches(10, 8)
tax.heatmap(nt_r, style="triangular")
tax.boundary()
tax.clear_matplotlib_ticks()
ticks = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
tax.ticks(ticks=ticks, axis="blr", linewidth=1, multiple=10)
tax.bottom_axis_label("VI Initial Wealth Share (%)", fontsize=fontsize)
tax.left_axis_label("NT Initial Wealth Share (%)", fontsize=fontsize)
tax.right_axis_label("TF Initial Wealth Share (%)", fontsize=fontsize)
tax.get_axes().axis("off")
tax.set_title("NT returns", fontsize=fontsize)
tax._redraw_labels()
plt.tight_layout()
plt.show()
# %%
