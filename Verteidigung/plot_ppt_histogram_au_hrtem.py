"""
Plot current density histograms by stage for Au HRTEM data from PPT.csv.

Output: ppt_histogram_au_hrtem.png
"""

import pathlib

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from style import FACECOLOR, RC


HERE = pathlib.Path(__file__).parent
CSV_PATH = HERE / "PPT.csv"
OUTPUT_PATH = HERE / "ppt_histogram_au_hrtem.png"

CURRENT_DENSITY = "Current Density"
STAGE_ORDER = ["Surface smoothing", "NPs synthesis"]
PALETTE_STAGE = {"Surface smoothing": "#2166ac", "NPs synthesis": "#d6604d"}


def load_au_hrtem_data() -> pd.DataFrame:
    df = pd.read_csv(CSV_PATH)
    df.columns = [column.strip().lstrip("\ufeff") for column in df.columns]

    if "TEM Mode" in df.columns:
        df = df.rename(columns={"TEM Mode": "Mode"})

    required_columns = {CURRENT_DENSITY, "Stage", "Mode", "Material"}
    missing_columns = required_columns.difference(df.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"PPT.csv is missing required columns: {missing}")

    filtered = df[
        df["Material"].eq("Au")
        & df["Mode"].eq("HRTEM")
        & df[CURRENT_DENSITY].notna()
    ].copy()

    if filtered.empty:
        raise ValueError("No Au HRTEM rows found in PPT.csv")

    return filtered


def plot_histogram(df: pd.DataFrame) -> None:
    plt.rcParams.update(RC)
    sns.set_theme(style="whitegrid", rc=RC)

    fig, ax = plt.subplots(figsize=(8, 5))
    fig.patch.set_facecolor(FACECOLOR)
    ax.set_facecolor(FACECOLOR)

    sns.histplot(
        data=df,
        x=CURRENT_DENSITY,
        hue="Stage",
        hue_order=STAGE_ORDER,
        palette=PALETTE_STAGE,
        bins=18,
        multiple="dodge",
        shrink=0.85,
        edgecolor="white",
        linewidth=0.8,
        ax=ax,
    )
    sns.move_legend(ax, "upper right", title="Stage", frameon=True)

    y_top = ax.get_ylim()[1]
    annotation_y = {
        "Surface smoothing": y_top * 0.92,
        "NPs synthesis": y_top * 0.82,
    }
    for stage in STAGE_ORDER:
        stage_values = df.loc[df["Stage"].eq(stage), CURRENT_DENSITY].dropna()
        if stage_values.empty:
            continue

        median_value = stage_values.median()
        ax.axvline(
            median_value,
            color=PALETTE_STAGE[stage],
            linestyle="--",
            linewidth=1.5,
            alpha=0.9,
        )
        ax.text(
            median_value,
            annotation_y.get(stage, y_top * 0.9),
            f"{stage}\nmedian current density = {median_value:.2f} A/cm$^2$",
            color=PALETTE_STAGE[stage],
            rotation=0,
            va="center",
            ha="left",
            fontsize=10,
            fontweight="bold",
        )

    ax.set_title("Au HRTEM Current Density Histogram by Stage", fontweight="bold")
    ax.set_xlabel(r"Current Density / A/cm$^2$")
    ax.set_ylabel("Count")
    ax.set_xlim(left=0)
    ax.grid(axis="y", alpha=0.3, linestyle="--")

    fig.tight_layout()
    fig.savefig(OUTPUT_PATH)
    plt.close(fig)


def main() -> None:
    df = load_au_hrtem_data()
    summary = (
        df.groupby("Stage")[CURRENT_DENSITY]
        .agg(["count", "median", "mean", "std"])
        .round(3)
    )
    print(summary)

    plot_histogram(df)
    print(f"Saved: {OUTPUT_PATH.name}")


if __name__ == "__main__":
    main()