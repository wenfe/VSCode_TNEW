from pathlib import Path

import matplotlib.colors as colors
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


input_csv = Path("Scorer_1_3d_axisymmetric.csv")
output_png = Path("3D_Energy_deposition_ppt_axisymmetric_viridis.png")
percentile = 99.5
max_points = 50000

sns.set_style("white")

df = pd.read_csv(input_csv, usecols=["X", "Y", "Z", "Edep"])
positive = df[df["Edep"] > 0.0].copy()
if positive.empty:
    raise ValueError("No positive Edep values found")

threshold = positive["Edep"].quantile(percentile / 100.0)
plotted = positive[positive["Edep"] >= threshold].copy()
if len(plotted) > max_points:
    plotted = plotted.sample(max_points, random_state=0)

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection="3d")

cw = ax.scatter(
    plotted["X"],
    plotted["Y"],
    plotted["Z"],
    c=plotted["Edep"],
    s=4,
    marker="o",
    alpha=0.65,
    norm=colors.LogNorm(vmin=plotted["Edep"].min(), vmax=plotted["Edep"].max()),
    cmap="viridis",
    edgecolors="none",
)

depth_ticks = [0, 25, 50, 75, 100, 125, 150, 175, 199]
depth_labels = [0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1.0]
transverse_ticks = [0, 25, 50, 75, 100, 125, 150, 175, 199]
transverse_labels = [-0.5, -0.375, -0.25, -0.125, 0.0, 0.125, 0.25, 0.375, 0.5]

ax.set_xlabel("X / µm", fontsize=12)
ax.set_ylabel("Y / µm", fontsize=12)
ax.set_zlabel("Z / µm", fontsize=12)
ax.set_xticks(depth_ticks)
ax.set_xticklabels(depth_labels, fontsize=10)
ax.set_yticks(transverse_ticks)
ax.set_yticklabels(transverse_labels, fontsize=10)
ax.set_zticks(transverse_ticks)
ax.set_zticklabels(transverse_labels, fontsize=10)

ax.set_xlim(0, 199)
ax.set_ylim(0, 199)
ax.set_zlim(0, 199)
ax.view_init(elev=24, azim=-55)

cbar = plt.colorbar(cw, ax=ax, shrink=0.72, pad=0.08)
cbar.set_label("Edep / MeV", fontsize=12)

plt.savefig(output_png, dpi=300, bbox_inches="tight")
plt.close(fig)

print(f"input: {input_csv}")
print(f"output: {output_png}")
print(f"positive voxels: {len(positive):,}")
print(f"plotted voxels: {len(plotted):,}")
print(f"threshold percentile: {percentile}")
print(f"threshold Edep: {threshold:.6g}")