import pandas as pd

data = pd.read_csv(
    "/Users/aymericvie/Documents/GitHub/evology/evology/research/MCarloLongRuns/data/data1.csv"
)
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.ndimage.filters import gaussian_filter
import ternary
import numpy as np
from ternary.helpers import simplex_iterator

sns.set(font_scale=1)
fontsize = 18

"""
data_group = data.groupby(['WS_VI', 'WS_TF', 'WS_NT'], as_index=False).mean()

def generate_random_heatmap_data(scale):
    tf_ws = dict()
    vi_ws = dict()
    nt_ws = dict()
    l = 0
    for (i,j,k) in simplex_iterator(scale):
        nt_ws[(i,j)] = data_group.loc[l,"NT_returns_mean"] 
        vi_ws[(i,j)] = data_group.loc[l,"VI_returns_mean"] 
        tf_ws[(i,j)] = data_group.loc[l,"TF_returns_mean"] 
        l += 1
    return nt_ws, vi_ws, tf_ws
    
scale = 50
nt_r, vi_r, tf_r = generate_random_heatmap_data(scale)

figure, tax = ternary.figure(scale=scale)
figure.set_size_inches(10, 8)
tax.heatmap(nt_r, style='triangular')
tax.boundary()
tax.clear_matplotlib_ticks()
ticks = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
tax.ticks(ticks = ticks, axis='blr', linewidth=1, multiple=10)
tax.bottom_axis_label("NT Initial Wealth Share (%)", fontsize = fontsize) 
tax.left_axis_label("VI Initial Wealth Share (%)", fontsize = fontsize) 
tax.right_axis_label("TF Initial Wealth Share (%)", fontsize = fontsize)
tax.get_axes().axis('off')
tax.set_title('NT returns', fontsize = fontsize)
tax._redraw_labels()
plt.tight_layout()
plt.savefig('Experiment1_NT_ternary.png',dpi=300)
plt.show()

figure, tax = ternary.figure(scale=scale)
figure.set_size_inches(10, 8)
tax.heatmap(vi_r, style='triangular')
tax.boundary()
tax.clear_matplotlib_ticks()
ticks = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
tax.ticks(ticks = ticks, axis='blr', linewidth=1, multiple=10)
tax.bottom_axis_label("NT Initial Wealth Share (%)", fontsize = fontsize) 
tax.left_axis_label("VI Initial Wealth Share (%)", fontsize = fontsize) 
tax.right_axis_label("TF Initial Wealth Share (%)", fontsize = fontsize)
tax.get_axes().axis('off')
tax.set_title('VI returns', fontsize = fontsize)
tax._redraw_labels()
plt.tight_layout()
plt.savefig('Experiment1_VI_ternary.png',dpi=300)
plt.show()

figure, tax = ternary.figure(scale=scale)
figure.set_size_inches(10, 8)
tax.heatmap(tf_r, style='triangular')
tax.boundary()
tax.clear_matplotlib_ticks()
ticks = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
tax.ticks(ticks = ticks, axis='blr', linewidth=1, multiple=10)
tax.bottom_axis_label("NT Initial Wealth Share (%)", fontsize = fontsize) 
tax.left_axis_label("VI Initial Wealth Share (%)", fontsize = fontsize) 
tax.right_axis_label("TF Initial Wealth Share (%)", fontsize = fontsize)
tax.get_axes().axis('off')
tax.set_title('TF returns', fontsize = fontsize)
tax._redraw_labels()
plt.tight_layout()
plt.savefig('Experiment1_TF_ternary.png',dpi=300)
plt.show()

"""

""" return to size ratios """

data = pd.read_csv(
    "/Users/aymericvie/Documents/GitHub/evology/evology/research/MCarloLongRuns/data/data1.csv"
)
data_group = data.groupby(["WS_VI", "WS_TF", "WS_NT"], as_index=False).mean()
# print('here')
# print(data_group['WS_VI'])


data_group["NT_weighted_returns"] = data_group["NT_returns_mean"] / np.sqrt(
    data_group["WS_NT"]
)
data_group["VI_weighted_returns"] = data_group["VI_returns_mean"] / np.sqrt(
    data_group["WS_VI"]
)
data_group["TF_weighted_returns"] = data_group["TF_returns_mean"] / np.sqrt(
    data_group["WS_TF"]
)
# data_group['NT_weighted_returns'] = data_group['NT_returns_mean'] / data_group['WS_NT']
# data_group['VI_weighted_returns'] = data_group['VI_returns_mean'] / data_group['WS_VI']
# data_group['TF_weighted_returns'] = data_group['TF_returns_mean'] / data_group['WS_TF']

# print(data_group['VI_returns_mean'])
# print(data_group['WS_VI'])

from math import isnan


def generate_random_heatmap_data2(scale):
    tf_ws = dict()
    vi_ws = dict()
    nt_ws = dict()
    l = 0
    for (i, j, k) in simplex_iterator(scale):
        nt_ws[(i, j)] = data_group.loc[l, "NT_weighted_returns"]
        vi_ws[(i, j)] = data_group.loc[l, "VI_weighted_returns"]
        tf_ws[(i, j)] = data_group.loc[l, "TF_weighted_returns"]
        if isnan(nt_ws[(i, j)]) == True:
            nt_ws[(i, j)] = 0.0
        if isnan(vi_ws[(i, j)]) == True:
            vi_ws[(i, j)] = 0.0
        if isnan(tf_ws[(i, j)]) == True:
            tf_ws[(i, j)] = 0.0
        # NOTE: this isnan is important to add. Because if the first value that ternary heatmap
        # encounters is NAN, then it will turn the figure ALL to Nan.
        # When the NAN is a row of data (ex for WS = 0) but it is not the first row to be plotted,
        # then the program simply displays a black line.
        # Porbably a bug to be noted when using ternary.
        l += 1
    return nt_ws, vi_ws, tf_ws


scale = 50
nt_r2, vi_r2, tf_r2 = generate_random_heatmap_data2(scale)


# print(vi_r2)

figure, tax = ternary.figure(scale=scale)
figure.set_size_inches(10, 8)
tax.heatmap(nt_r2, style="triangular")
tax.boundary()
tax.clear_matplotlib_ticks()
ticks = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
tax.ticks(ticks=ticks, axis="blr", linewidth=1, multiple=10)
tax.bottom_axis_label("NT Initial Wealth Share (%)", fontsize=fontsize)
tax.left_axis_label("VI Initial Wealth Share (%)", fontsize=fontsize)
tax.right_axis_label("TF Initial Wealth Share (%)", fontsize=fontsize)
tax.get_axes().axis("off")
tax.set_title("NT weighted returns", fontsize=fontsize)
tax._redraw_labels()
plt.tight_layout()
plt.savefig("Experiment1b_NT_ternary.png", dpi=300)
plt.show()

figure, tax = ternary.figure(scale=scale)
figure.set_size_inches(10, 8)
tax.heatmap(vi_r2, style="triangular")
tax.boundary()
tax.clear_matplotlib_ticks()
ticks = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
tax.ticks(ticks=ticks, axis="blr", linewidth=1, multiple=10)
tax.bottom_axis_label("NT Initial Wealth Share (%)", fontsize=fontsize)
tax.left_axis_label("VI Initial Wealth Share (%)", fontsize=fontsize)
tax.right_axis_label("TF Initial Wealth Share (%)", fontsize=fontsize)
tax.get_axes().axis("off")
tax.set_title("VI weighted returns", fontsize=fontsize)
tax._redraw_labels()
plt.tight_layout()
plt.savefig("Experiment1b_VI_ternary.png", dpi=300)
plt.show()

figure, tax = ternary.figure(scale=scale)
figure.set_size_inches(10, 8)
tax.heatmap(tf_r2, style="triangular")
tax.boundary()
tax.clear_matplotlib_ticks()
ticks = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
tax.ticks(ticks=ticks, axis="blr", linewidth=1, multiple=10)
tax.bottom_axis_label("NT Initial Wealth Share (%)", fontsize=fontsize)
tax.left_axis_label("VI Initial Wealth Share (%)", fontsize=fontsize)
tax.right_axis_label("TF Initial Wealth Share (%)", fontsize=fontsize)
tax.get_axes().axis("off")
tax.set_title("TF weighted returns", fontsize=fontsize)
tax._redraw_labels()
plt.tight_layout()
plt.savefig("Experiment1b_TF_ternary.png", dpi=300)
plt.show()
