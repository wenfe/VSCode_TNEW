import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.colors as colors


sns.set_style("white")

df = pd.read_csv("Scorer_1_3d_axisymmetric.csv", usecols=["X", "Y", "Z", "Edep"])

center_index = 100
color_floor = 0.0001


def format_depth_axis(axis):
    axis.set_ticks([-4.5, 25, 50, 75, 100, 125, 150, 175, 200])
    axis.set_ticklabels([0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1.0], fontsize=12)


def format_transverse_axis(axis):
    axis.set_ticks([0, 25, 50, 75, 100, 125, 150, 175, 200])
    axis.set_ticklabels([-0.5, -0.375, -0.25, -0.125, 0.0, 0.125, 0.25, 0.375, 0.5], fontsize=12)


def plot_plane(data, x_column, y_column, xlabel, ylabel, title, output_png, x_axis_type, y_axis_type):
    fig, ax = plt.subplots(figsize=(8, 6))
    cw = ax.scatter(
        data[x_column],
        data[y_column],
        c=data["Edep"] + color_floor,
        s=200,
        marker="s",
        norm=colors.LogNorm(),
        cmap="viridis",
        edgecolors="none",
    )

    ax.set_title(title, fontsize=12)
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)

    if x_axis_type == "depth":
        format_depth_axis(ax.xaxis)
        ax.set_xlim(-4.5, 200)
    else:
        format_transverse_axis(ax.xaxis)
        ax.set_xlim(0, 200)

    if y_axis_type == "depth":
        format_depth_axis(ax.yaxis)
        ax.set_ylim(-4.5, 200)
    else:
        format_transverse_axis(ax.yaxis)
        ax.set_ylim(0, 200)

    cbar = plt.colorbar(cw)
    cbar.set_label("Edep / MeV", fontsize=12)
    plt.savefig(output_png, dpi=300, bbox_inches="tight")
    plt.close(fig)


plane_x0 = df[df["X"] == 0]
plane_y0 = df[df["Y"] == center_index]
plane_z0 = df[df["Z"] == center_index]

plot_plane(
    plane_x0,
    "Y",
    "Z",
    "Y / µm",
    "Z / µm",
    "Plane 1: X = 0",
    "Scorer_1_3d_axisymmetric_plane_x0_yz.png",
    "transverse",
    "transverse",
)

plot_plane(
    plane_y0,
    "X",
    "Z",
    "X / µm",
    "Z / µm",
    "Plane 2: Y = 0",
    "Scorer_1_3d_axisymmetric_plane_y0_xz.png",
    "depth",
    "transverse",
)

plot_plane(
    plane_z0,
    "X",
    "Y",
    "X / µm",
    "Y / µm",
    "Plane 3: Z = 0",
    "Scorer_1_3d_axisymmetric_plane_z0_xy.png",
    "depth",
    "transverse",
)

print("output: Scorer_1_3d_axisymmetric_plane_x0_yz.png")
print("output: Scorer_1_3d_axisymmetric_plane_y0_xz.png")
print("output: Scorer_1_3d_axisymmetric_plane_z0_xy.png")
print(f"plane X=0 points: {len(plane_x0)}")
print(f"plane Y=0 points: {len(plane_y0)}")
print(f"plane Z=0 points: {len(plane_z0)}")