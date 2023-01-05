import matplotlib.style
import matplotlib as mpl
from cycler import cycler
import matplotlib.font_manager

FONT_MONOSPACE = {'fontname':'monospace'}
MARKERS = "o^s*DP1"
COLORS = [
    "cornflowerblue",
    "darkseagreen",
    "salmon",
    "orange",
    "seagreen",
    "dimgray",
    "purple",
]
COLORS_EXTRA = ["#9c2963", "#fb9e07"]

mpl.rcParams['axes.prop_cycle'] = cycler(color=COLORS)
mpl.rcParams['lines.linewidth'] = 2
mpl.rcParams['lines.markersize'] = 7
mpl.rcParams['axes.linewidth'] = 1.5
mpl.rcParams['font.family'] = "cmr10"
mpl.rcParams['axes.formatter.use_mathtext'] = True

# for font in matplotlib.font_manager.fontManager.ttflist:
#     if "modern" in font.name.lower():
#         print(font.name)
# exit()