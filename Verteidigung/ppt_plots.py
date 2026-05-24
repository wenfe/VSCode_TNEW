"""
PPT.csv — Focused Analysis Plots
=================================
  - Density Plot (HRTEM): Current Density distribution by Stage
  - STEM Violin + Swarm: Au vs WO3

Output: ppt_violin_swarm.png | stem_ppt_violin_swarm.png
"""

import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
from scipy import stats

# #########################
PALETTE_STAGE = {"Melting": "#2166ac", "Synthesis": "#d6604d"}
PALETTE_MODE  = {"HRTEM": "#1b7837",   "LTEM": "#762a83"}
RC = {
    "font.family":       "serif",
    "font.size":         12,
    "axes.titlesize":    13,
    "axes.labelsize":    12,
    "xtick.labelsize":   11,
    "ytick.labelsize":   11,
    "legend.fontsize":   10,
    "figure.dpi":        150,
    "savefig.dpi":       300,
    "savefig.bbox":      "tight",
    "axes.spines.top":   False,
    "axes.spines.right": False,
}
plt.rcParams.update(RC)
sns.set_theme(style="whitegrid", rc=RC)

# ##########################
df = pd.read_csv("PPT.csv")
df.columns = [c.strip().lstrip("\ufeff") for c in df.columns]
if "TEM Mode" in df.columns:
    df = df.rename(columns={"TEM Mode": "Mode"})

CD     = "Current Density"
MODES  = sorted(df["Mode"].unique())
STAGES = sorted(df["Stage"].unique())
rng    = np.random.default_rng(42)

print(f"Loaded {len(df)} rows | Modes: {MODES} | Stages: {STAGES}")
print(df.groupby(["Mode", "Stage"])[CD].agg(["count", "median", "mean", "std"]).round(3))

# #########################
# PLOT KDE Density: Current Density on x-axis, Probability on y-axis
# #########################
fig2, ax2 = plt.subplots(1, 1, figsize=(8, 6))
fig2.suptitle(
    "Density Plot: Current Density Distribution  |  HRTEM only\n"
    "(Surface Smoothing ↑ | NP Synthesis ↓ | dashed = median)",
    fontsize=13, fontweight="bold"
)

df_hrtem = df[df["Mode"] == "HRTEM"]

all_vals = df_hrtem[CD].dropna()
x_grid = np.linspace(all_vals.min(), all_vals.max() + 0.5, 500)

for stage in STAGES:
    sub = df_hrtem[df_hrtem["Stage"] == stage][CD].dropna()
    label = "NP Synthesis" if stage == "Synthesis" else "Surface Smoothing"
    col = PALETTE_STAGE[stage]
    sign = 1 if stage == "Melting" else -1  # Surface Smoothing up, Synthesis down

    kde = stats.gaussian_kde(sub, bw_method=0.6)
    density = kde(x_grid) * sign

    ax2.plot(x_grid, density, color=col, linewidth=1.8, label=label)
    ax2.fill_between(x_grid, density, alpha=0.4, color=col)

    kde_at_data = kde(sub.values) * sign
    ax2.scatter(sub, kde_at_data, color=col, s=25, alpha=0.75,
                edgecolors="white", linewidths=0.5, zorder=4)

    med = sub.median()
    y_peak = density[np.argmax(np.abs(density))]
    if sign == 1:
        ax2.plot([med, med], [0, kde(np.array([med]))[0]],
                 color=col, ls="--", lw=1.5, alpha=0.7)
        ax2.text(med + 1.5, y_peak * 0.85,
                 f"{label}\nMedian Current Density\n= {med:.2f} A/cm²", color=col,
                 fontsize=10, fontweight="bold",
                 ha="left", va="bottom",
                 bbox=dict(boxstyle="round,pad=0.3", fc="white",
                           ec=col, lw=1.2, alpha=0.9))
    else:
        ax2.plot([med, med], [0, -kde(np.array([med]))[0]],
                 color=col, ls="--", lw=1.5, alpha=0.7)
        ax2.annotate(
            f"{label}\nMedian Current Density\n= {med:.2f} A/cm²",
            xy=(med, 0), xytext=(med + 3, abs(y_peak) * 0.5),
            color=col, fontsize=10, fontweight="bold",
            ha="left", va="center",
            bbox=dict(boxstyle="round,pad=0.3", fc="white",
                      ec=col, lw=1.2, alpha=0.9),
            arrowprops=dict(arrowstyle="->" , color=col, lw=1.5),
        )

ax2.axhline(0, color="black", lw=0.8)
x_start = all_vals.min()
ax2.set_xlim(left=x_start)
# Mark the starting x value on the axis
ax2.axvline(x_start, color="black", lw=0.8, ls=":", alpha=0.6)
ticks = list(ax2.get_xticks())
if x_start not in ticks:
    ticks = sorted(set(ticks + [x_start]))
ticks = [t for t in ticks if t != 0]
ax2.set_xticks(ticks)
ax2.set_xlabel("Current Density / A/cm²", fontsize=12)
ax2.set_ylabel("Probability Density", fontsize=12)
ax2.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: f"{abs(y):.2f}"))
ax2.legend(title="Stage", frameon=True, loc="upper right")
ax2.grid(axis="x", alpha=0.35, linestyle="--")
ax2.spines["top"].set_visible(True)
ax2.spines["left"].set_visible(True)
ax2.spines["right"].set_visible(True)
ax2.spines["bottom"].set_visible(True)

plt.tight_layout()
plt.savefig("ppt_violin_swarm.png")
plt.close("all")
print("Saved: ppt_violin_swarm.png")
