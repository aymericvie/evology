import sys
import pandas as pd

sys.path.insert(0, "/Users/aymericvie/Documents/GitHub/evology/evology/code/")
import ternary
import numpy as np
import matplotlib.pyplot as plt
import platform

if platform.system() != "Linux":
    raise ValueError("Incorrect OS.")

MCNT1 = pd.read_csv(
    "/home/vie/Documents/GitHub/evology/evology/research/MCarloLongRuns/data_config1/MC_NT.csv"
)
MCVI1 = pd.read_csv(
    "/home/vie/Documents/GitHub/evology/evology/research/MCarloLongRuns/data_config1/MC_VI.csv"
)
MCTF1 = pd.read_csv(
    "/home/vie/Documents/GitHub/evology/evology/research/MCarloLongRuns/data_config1/MC_TF.csv"
)

MCNT2 = pd.read_csv(
    "/home/vie/Documents/GitHub/evology/evology/research/MCarloLongRuns/data_config2/MC_NT.csv"
)
MCVI2 = pd.read_csv(
    "/home/vie/Documents/GitHub/evology/evology/research/MCarloLongRuns/data_config2/MC_VI.csv"
)
MCTF2 = pd.read_csv(
    "/home/vie/Documents/GitHub/evology/evology/research/MCarloLongRuns/data_config2/MC_TF.csv"
)

MCNT3 = pd.read_csv(
    "/home/vie/Documents/GitHub/evology/evology/research/MCarloLongRuns/data_config3/MC_NT.csv"
)
MCVI3 = pd.read_csv(
    "/home/vie/Documents/GitHub/evology/evology/research/MCarloLongRuns/data_config3/MC_VI.csv"
)
MCTF3 = pd.read_csv(
    "/home/vie/Documents/GitHub/evology/evology/research/MCarloLongRuns/data_config3/MC_TF.csv"
)

MCNT4 = pd.read_csv(
    "/home/vie/Documents/GitHub/evology/evology/research/MCarloLongRuns/data_config4/MC_NT.csv"
)
MCVI4 = pd.read_csv(
    "/home/vie/Documents/GitHub/evology/evology/research/MCarloLongRuns/data_config4/MC_VI.csv"
)
MCTF4 = pd.read_csv(
    "/home/vie/Documents/GitHub/evology/evology/research/MCarloLongRuns/data_config4/MC_TF.csv"
)

MCNT5 = pd.read_csv(
    "/home/vie/Documents/GitHub/evology/evology/research/MCarloLongRuns/data_config5/MC_NT.csv"
)
MCVI5 = pd.read_csv(
    "/home/vie/Documents/GitHub/evology/evology/research/MCarloLongRuns/data_config5/MC_VI.csv"
)
MCTF5 = pd.read_csv(
    "/home/vie/Documents/GitHub/evology/evology/research/MCarloLongRuns/data_config5/MC_TF.csv"
)

MCNT6 = pd.read_csv(
    "/home/vie/Documents/GitHub/evology/evology/research/MCarloLongRuns/data_config6/MC_NT.csv"
)
MCVI6 = pd.read_csv(
    "/home/vie/Documents/GitHub/evology/evology/research/MCarloLongRuns/data_config6/MC_VI.csv"
)
MCTF6 = pd.read_csv(
    "/home/vie/Documents/GitHub/evology/evology/research/MCarloLongRuns/data_config6/MC_TF.csv"
)

MCNT7 = pd.read_csv(
    "/home/vie/Documents/GitHub/evology/evology/research/MCarloLongRuns/data_config7/MC_NT.csv"
)
MCVI7 = pd.read_csv(
    "/home/vie/Documents/GitHub/evology/evology/research/MCarloLongRuns/data_config7/MC_VI.csv"
)
MCTF7 = pd.read_csv(
    "/home/vie/Documents/GitHub/evology/evology/research/MCarloLongRuns/data_config7/MC_TF.csv"
)

MCNT8 = pd.read_csv(
    "/home/vie/Documents/GitHub/evology/evology/research/MCarloLongRuns/data_config8/MC_NT.csv"
)
MCVI8 = pd.read_csv(
    "/home/vie/Documents/GitHub/evology/evology/research/MCarloLongRuns/data_config8/MC_VI.csv"
)
MCTF8 = pd.read_csv(
    "/home/vie/Documents/GitHub/evology/evology/research/MCarloLongRuns/data_config8/MC_TF.csv"
)

MCNT9 = pd.read_csv(
    "/home/vie/Documents/GitHub/evology/evology/research/MCarloLongRuns/data_config9/MC_NT.csv"
)
MCVI9 = pd.read_csv(
    "/home/vie/Documents/GitHub/evology/evology/research/MCarloLongRuns/data_config9/MC_VI.csv"
)
MCTF9 = pd.read_csv(
    "/home/vie/Documents/GitHub/evology/evology/research/MCarloLongRuns/data_config9/MC_TF.csv"
)

MCNT10 = pd.read_csv(
    "/home/vie/Documents/GitHub/evology/evology/research/MCarloLongRuns/data_config10/MC_NT.csv"
)
MCVI10 = pd.read_csv(
    "/home/vie/Documents/GitHub/evology/evology/research/MCarloLongRuns/data_config10/MC_VI.csv"
)
MCTF10 = pd.read_csv(
    "/home/vie/Documents/GitHub/evology/evology/research/MCarloLongRuns/data_config10/MC_TF.csv"
)


def PathPoints(MCNT, MCVI, MCTF):
    points = []
    for i in range(len(MCNT.columns) - 1):
        x = MCNT["Rep%s" % i].mean()
        y = MCVI["Rep%s" % i].mean()
        z = MCTF["Rep%s" % i].mean()
        points.append((x, y, z))
    return points


def FinalPoints(MCNT, MCVI, MCTF):
    points = []
    for i in range(len(MCNT.columns) - 1):
        x = MCNT["Rep%s" % i].iloc[-1]
        y = MCVI["Rep%s" % i].iloc[-1]
        z = MCTF["Rep%s" % i].iloc[-1]
        points.append((x, y, z))
    return points


points1 = PathPoints(MCNT1, MCVI1, MCTF1)
points2 = PathPoints(MCNT2, MCVI2, MCTF2)
points3 = PathPoints(MCNT3, MCVI3, MCTF3)
points4 = PathPoints(MCNT4, MCVI4, MCTF4)
points5 = PathPoints(MCNT5, MCVI5, MCTF5)
points6 = PathPoints(MCNT6, MCVI6, MCTF6)
points7 = PathPoints(MCNT7, MCVI7, MCTF7)
points8 = PathPoints(MCNT8, MCVI8, MCTF8)
points9 = PathPoints(MCNT9, MCVI9, MCTF9)
points10 = PathPoints(MCNT10, MCVI10, MCTF10)

finals1 = FinalPoints(MCNT1, MCVI1, MCTF1)
finals2 = FinalPoints(MCNT2, MCVI2, MCTF2)
finals3 = FinalPoints(MCNT3, MCVI3, MCTF3)
finals4 = FinalPoints(MCNT4, MCVI4, MCTF4)
finals5 = FinalPoints(MCNT5, MCVI5, MCTF5)
finals6 = FinalPoints(MCNT6, MCVI6, MCTF6)
finals7 = FinalPoints(MCNT7, MCVI7, MCTF7)
finals8 = FinalPoints(MCNT8, MCVI8, MCTF8)

scale = 100
fontsize = 20


def TernaryPlot(scale, points, fontsize, title):
    origin = [((100 / 3, 100 / 3, 100 / 3))]
    # origin = [((40, 40, 20))]
    # origin = [((20,40,40))]
    figure, tax = ternary.figure(scale=scale)
    figure.set_size_inches(10, 8)
    tax.gridlines(color="gray", multiple=10)
    tax.boundary()
    tax.left_axis_label("TF (%)", fontsize=fontsize)
    tax.right_axis_label("VI (%)", fontsize=fontsize)
    tax.bottom_axis_label("NT (%)", fontsize=fontsize)
    tax.scatter(points, marker="D", color="red", label="Simulations")
    tax.scatter(origin, marker="D", color="black", label="Initial condition")
    ticks = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    tax.ticks(ticks=ticks, axis="lbr", linewidth=1, multiple=10)
    tax.get_axes().axis("off")
    # tax.clear_matplotlib_ticks()
    tax.set_title(title, fontsize=fontsize)
    plt.legend(loc="upper right", fontsize=fontsize)
    plt.tight_layout()
    tax._redraw_labels()
    return figure, tax


figure, tax = TernaryPlot(scale, points1, fontsize, "Config1")
if platform.system() == "Linux":
    path = "/home/vie/Documents/GitHub/evology/evology/research/MCarloLongRuns/path_figs/Path1.png"
    plt.savefig(path, dpi=300)
if platform.system() == "Darwin":
    path = "/Users/aymericvie/Documents/GitHub/evology/evology/research/MCarloLongRuns/path_figs/Path1.png"
    plt.savefig(path, dpi=300)

figure, tax = TernaryPlot(scale, finals1, fontsize, "Config1")
if platform.system() == "Linux":
    path = "/home/vie/Documents/GitHub/evology/evology/research/MCarloLongRuns/path_figs/Final1.png"
    plt.savefig(path, dpi=300)
if platform.system() == "Darwin":
    path = "/Users/aymericvie/Documents/GitHub/evology/evology/research/MCarloLongRuns/path_figs/Final1.png"
    plt.savefig(path, dpi=300)

figure, tax = TernaryPlot(scale, points2, fontsize, "Config2")
if platform.system() == "Linux":
    path = "/home/vie/Documents/GitHub/evology/evology/research/MCarloLongRuns/path_figs/Path2.png"
    plt.savefig(path, dpi=300)
if platform.system() == "Darwin":
    path = "/Users/aymericvie/Documents/GitHub/evology/evology/research/MCarloLongRuns/path_figs/Path2.png"
    plt.savefig(path, dpi=300)

figure, tax = TernaryPlot(scale, finals2, fontsize, "Config2")
if platform.system() == "Linux":
    path = "/home/vie/Documents/GitHub/evology/evology/research/MCarloLongRuns/path_figs/Final2.png"
    plt.savefig(path, dpi=300)
if platform.system() == "Darwin":
    path = "/Users/aymericvie/Documents/GitHub/evology/evology/research/MCarloLongRuns/path_figs/Final2.png"
    plt.savefig(path, dpi=300)

figure, tax = TernaryPlot(scale, points3, fontsize, "Config3")
if platform.system() == "Linux":
    path = "/home/vie/Documents/GitHub/evology/evology/research/MCarloLongRuns/path_figs/Path3.png"
    plt.savefig(path, dpi=300)
if platform.system() == "Darwin":
    path = "/Users/aymericvie/Documents/GitHub/evology/evology/research/MCarloLongRuns/path_figs/Path3.png"
    plt.savefig(path, dpi=300)

figure, tax = TernaryPlot(scale, finals3, fontsize, "Config3")
if platform.system() == "Linux":
    path = "/home/vie/Documents/GitHub/evology/evology/research/MCarloLongRuns/path_figs/Final3.png"
    plt.savefig(path, dpi=300)
if platform.system() == "Darwin":
    path = "/Users/aymericvie/Documents/GitHub/evology/evology/research/MCarloLongRuns/path_figs/Final3.png"
    plt.savefig(path, dpi=300)

figure, tax = TernaryPlot(scale, points4, fontsize, "Config4")
if platform.system() == "Linux":
    path = "/home/vie/Documents/GitHub/evology/evology/research/MCarloLongRuns/path_figs/Path4.png"
    plt.savefig(path, dpi=300)
if platform.system() == "Darwin":
    path = "/Users/aymericvie/Documents/GitHub/evology/evology/research/MCarloLongRuns/path_figs/Path4.png"
    plt.savefig(path, dpi=300)

figure, tax = TernaryPlot(scale, finals4, fontsize, "Config4")
if platform.system() == "Linux":
    path = "/home/vie/Documents/GitHub/evology/evology/research/MCarloLongRuns/path_figs/Final4.png"
    plt.savefig(path, dpi=300)
if platform.system() == "Darwin":
    path = "/Users/aymericvie/Documents/GitHub/evology/evology/research/MCarloLongRuns/path_figs/Final4.png"
    plt.savefig(path, dpi=300)

figure, tax = TernaryPlot(scale, points5, fontsize, "Config5")
if platform.system() == "Linux":
    path = "/home/vie/Documents/GitHub/evology/evology/research/MCarloLongRuns/path_figs/Path5.png"
    plt.savefig(path, dpi=300)
if platform.system() == "Darwin":
    path = "/Users/aymericvie/Documents/GitHub/evology/evology/research/MCarloLongRuns/path_figs/Path5.png"
    plt.savefig(path, dpi=300)

figure, tax = TernaryPlot(scale, finals5, fontsize, "Config5")
if platform.system() == "Linux":
    path = "/home/vie/Documents/GitHub/evology/evology/research/MCarloLongRuns/path_figs/Final5.png"
    plt.savefig(path, dpi=300)
if platform.system() == "Darwin":
    path = "/Users/aymericvie/Documents/GitHub/evology/evology/research/MCarloLongRuns/path_figs/Final5.png"
    plt.savefig(path, dpi=300)

figure, tax = TernaryPlot(scale, points6, fontsize, "Config6")
if platform.system() == "Linux":
    path = "/home/vie/Documents/GitHub/evology/evology/research/MCarloLongRuns/path_figs/Path6.png"
    plt.savefig(path, dpi=300)
if platform.system() == "Darwin":
    path = "/Users/aymericvie/Documents/GitHub/evology/evology/research/MCarloLongRuns/path_figs/Path6.png"
    plt.savefig(path, dpi=300)

figure, tax = TernaryPlot(scale, finals6, fontsize, "Config6")
if platform.system() == "Linux":
    path = "/home/vie/Documents/GitHub/evology/evology/research/MCarloLongRuns/path_figs/Final6.png"
    plt.savefig(path, dpi=300)
if platform.system() == "Darwin":
    path = "/Users/aymericvie/Documents/GitHub/evology/evology/research/MCarloLongRuns/path_figs/Final6.png"
    plt.savefig(path, dpi=300)

figure, tax = TernaryPlot(scale, points7, fontsize, "Config7")
if platform.system() == "Linux":
    path = "/home/vie/Documents/GitHub/evology/evology/research/MCarloLongRuns/path_figs/Path7.png"
    plt.savefig(path, dpi=300)
if platform.system() == "Darwin":
    path = "/Users/aymericvie/Documents/GitHub/evology/evology/research/MCarloLongRuns/path_figs/Path7.png"
    plt.savefig(path, dpi=300)

figure, tax = TernaryPlot(scale, finals7, fontsize, "Config7")
if platform.system() == "Linux":
    path = "/home/vie/Documents/GitHub/evology/evology/research/MCarloLongRuns/path_figs/Final7.png"
    plt.savefig(path, dpi=300)
if platform.system() == "Darwin":
    path = "/Users/aymericvie/Documents/GitHub/evology/evology/research/MCarloLongRuns/path_figs/Final7.png"
    plt.savefig(path, dpi=300)

figure, tax = TernaryPlot(scale, points8, fontsize, "Config8")
if platform.system() == "Linux":
    path = "/home/vie/Documents/GitHub/evology/evology/research/MCarloLongRuns/path_figs/Path8.png"
    plt.savefig(path, dpi=300)
if platform.system() == "Darwin":
    path = "/Users/aymericvie/Documents/GitHub/evology/evology/research/MCarloLongRuns/path_figs/Path8.png"
    plt.savefig(path, dpi=300)

figure, tax = TernaryPlot(scale, finals8, fontsize, "Config8")
if platform.system() == "Linux":
    path = "/home/vie/Documents/GitHub/evology/evology/research/MCarloLongRuns/path_figs/Final8.png"
    plt.savefig(path, dpi=300)
if platform.system() == "Darwin":
    path = "/Users/aymericvie/Documents/GitHub/evology/evology/research/MCarloLongRuns/path_figs/Final8.png"
    plt.savefig(path, dpi=300)

figure, tax = TernaryPlot(scale, points9, fontsize, "Config9")
if platform.system() == "Linux":
    path = "/home/vie/Documents/GitHub/evology/evology/research/MCarloLongRuns/path_figs/Path9.png"
    plt.savefig(path, dpi=300)
if platform.system() == "Darwin":
    path = "/Users/aymericvie/Documents/GitHub/evology/evology/research/MCarloLongRuns/path_figs/Path9.png"
    plt.savefig(path, dpi=300)

figure, tax = TernaryPlot(scale, points10, fontsize, "Config10")
if platform.system() == "Linux":
    path = "/home/vie/Documents/GitHub/evology/evology/research/MCarloLongRuns/path_figs/Path10.png"
    plt.savefig(path, dpi=300)
if platform.system() == "Darwin":
    path = "/Users/aymericvie/Documents/GitHub/evology/evology/research/MCarloLongRuns/path_figs/Path10.png"
    plt.savefig(path, dpi=300)
