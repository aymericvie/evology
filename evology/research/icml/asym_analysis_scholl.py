import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.ndimage.filters import gaussian_filter
import ternary
import numpy as np
from ternary.helpers import simplex_iterator
from matplotlib.colors import ListedColormap

sns.set(font_scale=1)
scale = 25
fontsize = 18

data = pd.read_csv(
    "/Users/aymericvie/Documents/GitHub/evology/evology/research/icml/data/asym_dis_scholl.csv"
)

# Removing the sum 0 or sum nan runs does not seem necessary

data_group = data.groupby(
    ["WS_VI_initial", "WS_TF_initial", "WS_NT_initial"], as_index=False
).mean()


def generate_random_heatmap_data(scale):
    tf_ws = dict()
    vi_ws = dict()
    nt_ws = dict()
    attractor = dict()
    l = 0
    for (i, j, k) in simplex_iterator(scale):
        nt_ws[(i, j)] = data_group.loc[l, "WS_NT_final"]
        vi_ws[(i, j)] = data_group.loc[l, "WS_VI_final"]
        tf_ws[(i, j)] = data_group.loc[l, "WS_TF_final"]
        if data_group.loc[l, "WS_TF_final"] >= 90:
            attractor[(i, j)] = 0
        elif data_group.loc[l, "WS_TF_final"] > 10:
            attractor[(i, j)] = 1
        else:
            attractor[(i, j)] = 2
        l += 1
    return nt_ws, vi_ws, tf_ws, attractor


nt_r, vi_r, tf_r, attractor = generate_random_heatmap_data(scale)

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
tax.set_title("NT final wealth share", fontsize=fontsize)
tax._redraw_labels()
plt.tight_layout()
plt.savefig("figures/WS_NT_scholl.png", dpi=300)
# plt.show()

figure, tax = ternary.figure(scale=scale)
figure.set_size_inches(10, 8)
tax.heatmap(vi_r, style="triangular")
tax.boundary()
tax.clear_matplotlib_ticks()
ticks = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
tax.ticks(ticks=ticks, axis="blr", linewidth=1, multiple=10)
tax.bottom_axis_label("VI Initial Wealth Share (%)", fontsize=fontsize)
tax.left_axis_label("NT Initial Wealth Share (%)", fontsize=fontsize)
tax.right_axis_label("TF Initial Wealth Share (%)", fontsize=fontsize)
tax.get_axes().axis("off")
tax.set_title("VI final wealth share", fontsize=fontsize)
tax._redraw_labels()
plt.tight_layout()
plt.savefig("figures/WS_VI_scholl.png", dpi=300)
# plt.show()

figure, tax = ternary.figure(scale=scale)
figure.set_size_inches(10, 8)
tax.heatmap(tf_r, style="triangular")
tax.boundary()
tax.clear_matplotlib_ticks()
ticks = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
tax.ticks(ticks=ticks, axis="blr", linewidth=1, multiple=10)
tax.bottom_axis_label("VI Initial Wealth Share (%)", fontsize=fontsize)
tax.left_axis_label("NT Initial Wealth Share (%)", fontsize=fontsize)
tax.right_axis_label("TF Initial Wealth Share (%)", fontsize=fontsize)
tax.get_axes().axis("off")
tax.set_title("TF final wealth share", fontsize=fontsize)
tax._redraw_labels()
plt.tight_layout()
plt.savefig("figures/WS_TF_scholl.png", dpi=300)
# plt.show()


cmap = plt.get_cmap("inferno", 3)
cmap = ListedColormap(["red", "grey", "blue"])
figure, tax = ternary.figure(scale=scale)
figure.set_size_inches(10, 8)
tax.heatmap(attractor, style="triangular", cmap=cmap, colorbar=False)
tax.boundary()
tax.clear_matplotlib_ticks()
ticks = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
tax.ticks(ticks=ticks, axis="blr", linewidth=1, multiple=10)
tax.bottom_axis_label("VI Initial Wealth Share (%)", fontsize=fontsize)
tax.left_axis_label("NT Initial Wealth Share (%)", fontsize=fontsize)
tax.right_axis_label("TF Initial Wealth Share (%)", fontsize=fontsize)
tax.get_axes().axis("off")
tax.set_title("Basins of attraction", fontsize=fontsize)
tax._redraw_labels()
plt.tight_layout()
plt.savefig("figures/basins_scholl.png", dpi=300)
# plt.show()


def gen_data(scale):
    gens = dict()
    l = 0
    for (i, j, k) in simplex_iterator(scale):
        gens[(i, j)] = data_group.loc[l, "Gen"]
        l += 1
    return gens


""" Density/diffusion plot for generations """

gens = gen_data(scale)
figure, tax = ternary.figure(scale=scale)
figure.set_size_inches(10, 8)
tax.heatmap(gens, style="triangular")
tax.boundary()
tax.clear_matplotlib_ticks()
ticks = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
tax.ticks(ticks=ticks, axis="blr", linewidth=1, multiple=10)
tax.bottom_axis_label("VI Initial Wealth Share (%)", fontsize=fontsize)
tax.left_axis_label("NT Initial Wealth Share (%)", fontsize=fontsize)
tax.right_axis_label("TF Initial Wealth Share (%)", fontsize=fontsize)
tax.get_axes().axis("off")
tax.set_title("Max generations", fontsize=fontsize)
tax._redraw_labels()
plt.tight_layout()
plt.savefig("figures/generations_scholl.png", dpi=300)
# plt.show()


# Difference in returns

# Result: regions with early extinctions correspond to high difference in returns;
# these are regions that are by nature imbalanced and pushing to the boundary.
def gen_data(scale):
    gens = dict()
    l = 0
    for (i, j, k) in simplex_iterator(scale):
        gens[(i, j)] = data_group.loc[l, "AvgDiffReturns"]
        if data_group.loc[l, "AvgDiffReturns"] > 10:
            gens[(i, j)] = 10
        l += 1
    return gens


gens = gen_data(scale)
figure, tax = ternary.figure(scale=scale)
figure.set_size_inches(10, 8)
tax.heatmap(gens, style="triangular")
tax.boundary()
tax.clear_matplotlib_ticks()
ticks = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
tax.ticks(ticks=ticks, axis="blr", linewidth=1, multiple=10)
tax.bottom_axis_label("VI Initial Wealth Share (%)", fontsize=fontsize)
tax.left_axis_label("NT Initial Wealth Share (%)", fontsize=fontsize)
tax.right_axis_label("TF Initial Wealth Share (%)", fontsize=fontsize)
tax.get_axes().axis("off")
tax.set_title("Avg diff returns", fontsize=fontsize)
tax._redraw_labels()
plt.tight_layout()
plt.savefig("figures/diff_returns_scholl.png", dpi=300)
# plt.show()


def gen_data(scale):
    gens = dict()
    l = 0
    for (i, j, k) in simplex_iterator(scale):
        gens[(i, j)] = data_group.loc[l, "AvgDiffReturns"]
        if data_group.loc[l, "AvgDiffReturns"] > 1:
            gens[(i, j)] = 1
        l += 1
    return gens


gens = gen_data(scale)
figure, tax = ternary.figure(scale=scale)
figure.set_size_inches(10, 8)
tax.heatmap(gens, style="triangular")
tax.boundary()
tax.clear_matplotlib_ticks()
ticks = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
tax.ticks(ticks=ticks, axis="blr", linewidth=1, multiple=10)
tax.bottom_axis_label("VI Initial Wealth Share (%)", fontsize=fontsize)
tax.left_axis_label("NT Initial Wealth Share (%)", fontsize=fontsize)
tax.right_axis_label("TF Initial Wealth Share (%)", fontsize=fontsize)
tax.get_axes().axis("off")
tax.set_title("Avg diff returns", fontsize=fontsize)
tax._redraw_labels()
plt.tight_layout()
plt.savefig("figures/diff_returns_scholl2.png", dpi=300)
# plt.show()


def PathPoints(data):
    points = []
    for i in range(len(data["WS_NT_final"])):
        x = (data.loc[i, "WS_VI_final"] / 100) * scale
        y = (data.loc[i, "WS_TF_final"] / 100) * scale
        z = (data.loc[i, "WS_NT_final"] / 100) * scale
        points.append((x, y, z))
    return points


points = PathPoints(data)
# origin = [((100/3, 100/3, 100/3))]
figure, tax = ternary.figure(scale=scale)
figure.set_size_inches(10, 8)
tax.gridlines(color="gray", multiple=10)
tax.boundary()
tax.clear_matplotlib_ticks()
ticks = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
tax.bottom_axis_label("VI Initial Wealth Share (%)", fontsize=fontsize)
tax.left_axis_label("NT Initial Wealth Share (%)", fontsize=fontsize)
tax.right_axis_label("TF Initial Wealth Share (%)", fontsize=fontsize)
tax.scatter(points, marker="D", color="red", label="Simulations")
tax.ticks(ticks=ticks, axis="blr", linewidth=1, multiple=10)
tax.get_axes().axis("off")
tax.set_title("Scatterplot", fontsize=fontsize)
plt.legend(loc="upper right", fontsize=fontsize)
plt.tight_layout()
tax._redraw_labels()
plt.savefig("figures/scatterplot_scholl.png", dpi=300)
# plt.show()


""" density """


def PathPoints(df):
    points = []
    N = len(df)
    for i in range(N):
        x = int((df.loc[i, "WS_VI_final"] / 100) * scale)
        y = int((df.loc[i, "WS_TF_final"] / 100) * scale)
        z = int((df.loc[i, "WS_NT_final"] / 100) * scale)
        points.append((x, y, z))
    return points


points = PathPoints(data)


def DensityData(points, scale):
    density = dict()
    total_count = (scale + 1) * (scale + 2) / 2
    sum_count = 0
    total_enum = 0
    for (i, j, k) in simplex_iterator(scale):
        count = 0
        total_enum += 1
        for point in points:
            if i == point[0] and j == point[1]:
                count += 1
        density[(i, j)] = (count / total_count) / 10
        sum_count += density[(i, j)]
    return density


# scale = 24  # to remove the artifact attractor
scale = 25  # cant set scale more than the experiment setting (25)
density = DensityData(points, scale)

figure, tax = ternary.figure(scale=scale)
figure.set_size_inches(10, 8)
tax.heatmap(density, style="triangular", cmap="Reds", vmin=0, vmax=0.15)
tax.boundary()
tax.clear_matplotlib_ticks()
ticks = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
tax.ticks(ticks=ticks, axis="blr", linewidth=1, multiple=10)
tax.bottom_axis_label("VI Final Wealth Share (%)", fontsize=fontsize)
tax.left_axis_label("NT Final Wealth Share (%)", fontsize=fontsize)
tax.right_axis_label("TF Final Wealth Share (%)", fontsize=fontsize)
tax.get_axes().axis("off")
tax.set_title("Wealth asymptotic distributions density", fontsize=fontsize)
tax._redraw_labels()
plt.tight_layout()
plt.savefig("figures/density_scholl.png", dpi=300)
# plt.show()


#### SUBSTRATEGIES


def gen_data(scale):
    tf = dict()
    vi = dict()
    nt = dict()
    l = 0
    for (i, j, k) in simplex_iterator(scale):
        nt[(i, j)] = data_group.loc[l, "Mean_NT"]
        vi[(i, j)] = data_group.loc[l, "Mean_VI"]
        tf[(i, j)] = data_group.loc[l, "Mean_TF"]

        l += 1
    return nt, vi, tf


nt, vi, tf = gen_data(scale)
figure, tax = ternary.figure(scale=scale)
figure.set_size_inches(10, 8)
tax.heatmap(nt, style="triangular")
tax.boundary()
tax.clear_matplotlib_ticks()
ticks = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
tax.ticks(ticks=ticks, axis="blr", linewidth=1, multiple=10)
tax.bottom_axis_label("NT Initial Wealth Share (%)", fontsize=fontsize)
tax.left_axis_label("VI Initial Wealth Share (%)", fontsize=fontsize)
tax.right_axis_label("TF Initial Wealth Share (%)", fontsize=fontsize)
tax.get_axes().axis("off")
tax.set_title("NT substrategy", fontsize=fontsize)
tax._redraw_labels()
plt.tight_layout()
plt.savefig("figures/nt_substrat_scholl.png", dpi=300)
# plt.show()

figure, tax = ternary.figure(scale=scale)
figure.set_size_inches(10, 8)
tax.heatmap(vi, style="triangular")
tax.boundary()
tax.clear_matplotlib_ticks()
ticks = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
tax.ticks(ticks=ticks, axis="blr", linewidth=1, multiple=10)
tax.bottom_axis_label("NT Initial Wealth Share (%)", fontsize=fontsize)
tax.left_axis_label("VI Initial Wealth Share (%)", fontsize=fontsize)
tax.right_axis_label("TF Initial Wealth Share (%)", fontsize=fontsize)
tax.get_axes().axis("off")
tax.set_title("VI substrategy", fontsize=fontsize)
tax._redraw_labels()
plt.tight_layout()
plt.savefig("figures/vi_substrat_scholl.png", dpi=300)
# plt.show()

figure, tax = ternary.figure(scale=scale)
figure.set_size_inches(10, 8)
tax.heatmap(tf, style="triangular")
tax.boundary()
tax.clear_matplotlib_ticks()
ticks = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
tax.ticks(ticks=ticks, axis="blr", linewidth=1, multiple=10)
tax.bottom_axis_label("NT Initial Wealth Share (%)", fontsize=fontsize)
tax.left_axis_label("VI Initial Wealth Share (%)", fontsize=fontsize)
tax.right_axis_label("TF Initial Wealth Share (%)", fontsize=fontsize)
tax.get_axes().axis("off")
tax.set_title("TF substrategy", fontsize=fontsize)
tax._redraw_labels()
plt.tight_layout()
plt.savefig("figures/tf_substrat_scholl.png", dpi=300)
# plt.show()
