"""
PPT.csv — Current Density Analysis
Doctoral Disputation Quality Visualizations
============================================
Columns: Current Density | Stage | Mode | Material
"""

import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")          # non-interactive backend — prevents plt.show() blocking GIF save
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.colors import LogNorm
from matplotlib.patches import FancyArrowPatch
import seaborn as sns
from scipy import stats
from scipy.stats import mannwhitneyu, kruskal
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ── Global style ────────────────────────────────────────────────────────────
PALETTE   = {"Melting": "#2166ac", "Synthesis": "#d6604d"}
MODE_PAL  = {"HRTEM": "#4dac26", "LTEM": "#7b3294", "STEM": "#d01c8b"}
MAT_PAL   = {"Au": "#f4a700", "WO": "#636363"}
RC = {
    "font.family": "serif",
    "font.size": 12,
    "axes.titlesize": 13,
    "axes.labelsize": 12,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 10,
    "figure.dpi": 150,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
}
plt.rcParams.update(RC)
sns.set_theme(style="whitegrid", rc=RC)

# ── Load data ────────────────────────────────────────────────────────────────
df = pd.read_csv("PPT.csv")
df.columns = df.columns.str.strip()
if "TEM Mode" in df.columns:
    df = df.rename(columns={"TEM Mode": "Mode"})
df["log10_CD"] = np.log10(df["Current Density"])
print(df.head())
print("\nShape:", df.shape)
print("\nGroup counts:")
print(df.groupby(["Stage", "Mode", "Material"]).size().to_string())

# ============================================================
# PLOT 1 — Raincloud Plot  (half-violin + strip + box)
# ============================================================
def raincloud(ax, data, x_col, y_col, hue_col, palette, log=True):
    """Minimal raincloud: half-violin left, box center, jitter right."""
    categories = data[x_col].unique()
    hue_levels = data[hue_col].unique()
    n_hue = len(hue_levels)
    width = 0.35
    offsets = np.linspace(-width / 2, width / 2, n_hue)

    for i, cat in enumerate(categories):
        for j, hue in enumerate(hue_levels):
            sub = data[(data[x_col] == cat) & (data[hue_col] == hue)][y_col].dropna()
            if sub.empty:
                continue
            pos = i + offsets[j]
            vals = np.log10(sub) if log else sub.values

            # Half violin (left side)
            kde = stats.gaussian_kde(vals, bw_method=0.4)
            y_range = np.linspace(vals.min(), vals.max(), 200)
            density = kde(y_range)
            density = density / density.max() * 0.28
            ax.fill_betweenx(y_range, pos, pos - density,
                             alpha=0.55, color=palette[hue], linewidth=0)

            # Box (IQR)
            q1, med, q3 = np.percentile(vals, [25, 50, 75])
            ax.plot([pos + 0.03, pos + 0.03], [q1, q3],
                    color="black", lw=3, solid_capstyle="round", zorder=3)
            ax.plot(pos + 0.03, med, "o", color="white",
                    markersize=5, zorder=4, markeredgecolor="black", markeredgewidth=0.8)

            # Jitter strip (right)
            jitter = np.random.uniform(-0.06, 0.06, size=len(vals))
            ax.scatter(pos + 0.18 + jitter, vals,
                       color=palette[hue], alpha=0.55, s=14, linewidths=0, zorder=2)

    ax.set_xticks(range(len(categories)))
    ax.set_xticklabels(categories)
    if log:
        ax.set_ylabel("Current Density (A/cm²) — log₁₀ scale")
        fmt = ticker.FuncFormatter(lambda x, _: f"$10^{{{x:.0f}}}$" if x == int(x) else f"$10^{{{x:.1f}}}$")
        ax.yaxis.set_major_formatter(fmt)

    # Legend
    from matplotlib.patches import Patch
    handles = [Patch(color=palette[h], alpha=0.7, label=h) for h in hue_levels]
    ax.legend(handles=handles, title=hue_col, frameon=True, loc="upper right")


fig1, axes1 = plt.subplots(1, 2, figsize=(13, 6), sharey=False)
fig1.suptitle("Raincloud Plot of Current Density\nby Microscopy Mode and Stage",
              fontsize=14, fontweight="bold", y=1.01)

for ax, mat, color_pal in zip(axes1, ["Au", "WO"], [PALETTE, PALETTE]):
    sub = df[df["Material"] == mat]
    if sub.empty:
        ax.set_visible(False)
        continue
    raincloud(ax, sub, x_col="Mode", y_col="Current Density",
              hue_col="Stage", palette=PALETTE, log=True)
    ax.set_title(f"Material: {mat}", fontweight="bold")
    ax.set_xlabel("Microscopy Mode")
    ax.grid(axis="y", alpha=0.4)

plt.tight_layout()
plt.savefig("plot1_raincloud.png")
plt.close('all')
print("✔ Plot 1 saved: plot1_raincloud.png")

# ============================================================
# PLOT 2 — Split Violin + Swarm (log scale)
# ============================================================
fig2, axes2 = plt.subplots(1, 2, figsize=(13, 6), sharey=False)
fig2.suptitle("Split Violin + Data Points\nCurrent Density by Mode and Stage",
              fontsize=14, fontweight="bold")

for ax, mat in zip(axes2, ["Au", "WO"]):
    sub = df[df["Material"] == mat].copy()
    if sub.empty:
        ax.set_visible(False)
        continue
    sub["log10_CD"] = np.log10(sub["Current Density"])

    sns.violinplot(data=sub, x="Mode", y="log10_CD", hue="Stage",
                   split=True, inner=None, palette=PALETTE,
                   scale="count", linewidth=0.8, ax=ax)
    sns.stripplot(data=sub, x="Mode", y="log10_CD", hue="Stage",
                  dodge=True, alpha=0.55, size=4, palette=PALETTE,
                  jitter=True, ax=ax, legend=False)

    ax.set_title(f"Material: {mat}", fontweight="bold")
    ax.set_ylabel("log₁₀(Current Density)")
    ax.set_xlabel("Microscopy Mode")
    ax.grid(axis="y", alpha=0.4)

    # Fix duplicate legend
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[:2], labels[:2], title="Stage", frameon=True)

plt.tight_layout()
plt.savefig("plot2_violin_swarm.png")
plt.close('all')
print("✔ Plot 2 saved: plot2_violin_swarm.png")

# ============================================================
# PLOT 3 — ECDF Plot (faceted by Mode)
# ============================================================
modes = df["Mode"].unique()
fig3, axes3 = plt.subplots(1, len(modes), figsize=(5 * len(modes), 5), sharey=True)
fig3.suptitle("Empirical Cumulative Distribution Functions\nby Microscopy Mode and Stage",
              fontsize=14, fontweight="bold")

if len(modes) == 1:
    axes3 = [axes3]

for ax, mode in zip(axes3, modes):
    sub = df[df["Mode"] == mode]
    for stage, color in PALETTE.items():
        vals = sub[sub["Stage"] == stage]["Current Density"].dropna().sort_values()
        if vals.empty:
            continue
        ecdf_y = np.arange(1, len(vals) + 1) / len(vals)
        ax.step(vals, ecdf_y, color=color, lw=2, label=stage, where="post")
        ax.scatter(vals, ecdf_y, color=color, s=20, alpha=0.4, zorder=3)

    ax.set_xscale("log")
    ax.set_title(f"Mode: {mode}", fontweight="bold")
    ax.set_xlabel("Current Density (A/cm²)")
    ax.set_ylabel("Cumulative Probability" if ax == axes3[0] else "")
    ax.legend(title="Stage", frameon=True)
    ax.grid(alpha=0.3, which="both")
    ax.xaxis.set_major_formatter(ticker.LogFormatterSciNotation())

plt.tight_layout()
plt.savefig("plot3_ecdf.png")
plt.close('all')
print("✔ Plot 3 saved: plot3_ecdf.png")

# ============================================================
# PLOT 4 — Heatmap of Median Current Densities (log scale)
# ============================================================
pivot = (df.groupby(["Mode", "Stage"])["Current Density"]
           .median()
           .unstack("Stage"))

fig4, ax4 = plt.subplots(figsize=(7, 4))
log_pivot = np.log10(pivot)
sns.heatmap(log_pivot, annot=pivot.map(lambda v: f"{v:.2f}"),
            fmt="", cmap="YlOrRd", linewidths=0.5,
            cbar_kws={"label": "Median Current Density log₁₀(A/cm²)"},
            ax=ax4)
ax4.set_title("Median Current Density Heatmap\n(annotated values in A/cm², color = log₁₀)",
              fontweight="bold")
ax4.set_xlabel("Stage")
ax4.set_ylabel("Microscopy Mode")
plt.tight_layout()
plt.savefig("plot4_heatmap.png")
plt.close('all')
print("✔ Plot 4 saved: plot4_heatmap.png")

# ============================================================
# PLOT 5 — Faceted Box + Strip (per Mode × Material)
# ============================================================
g = sns.FacetGrid(df, col="Mode", row="Material",
                  height=4, aspect=1.1, sharey=False,
                  margin_titles=True)
g.map_dataframe(sns.boxplot, x="Stage", y="Current Density",
                palette=PALETTE, width=0.5, fliersize=3,
                linewidth=0.9, order=["Melting", "Synthesis"])
g.map_dataframe(sns.stripplot, x="Stage", y="Current Density",
                palette=PALETTE, size=4, alpha=0.5, jitter=True,
                order=["Melting", "Synthesis"])
g.set(yscale="log")
g.set_axis_labels("Stage", "Current Density (A/cm²)")
g.set_titles(col_template="Mode: {col_name}", row_template="Material: {row_name}")
g.figure.suptitle("Box + Strip Plot Faceted by Mode and Material",
                  fontsize=14, fontweight="bold", y=1.01)
g.tight_layout()
g.savefig("plot5_faceted_box.png")
plt.close('all')
print("✔ Plot 5 saved: plot5_faceted_box.png")

# ============================================================
# PLOT 6 — Log-Normal Probability Plot (Q-Q per group)
# ============================================================
groups = df.groupby(["Stage", "Mode"])
n_groups = len(groups)
ncols = 3
nrows = int(np.ceil(n_groups / ncols))

fig6, axes6 = plt.subplots(nrows, ncols, figsize=(5 * ncols, 4 * nrows))
axes6 = axes6.flatten()
fig6.suptitle("Log-Normal Q-Q Probability Plots\nper Stage × Mode",
              fontsize=14, fontweight="bold")

for idx, ((stage, mode), grp) in enumerate(groups):
    ax = axes6[idx]
    log_vals = np.log10(grp["Current Density"].dropna())
    if len(log_vals) < 3:
        ax.set_visible(False)
        continue
    (osm, osr), (slope, intercept, r) = stats.probplot(log_vals, dist="norm")
    ax.scatter(osm, osr, color=PALETTE.get(stage, "#333"), alpha=0.7, s=30, label="Data")
    fit_line = slope * np.array(osm) + intercept
    ax.plot(osm, fit_line, "k--", lw=1.5, label=f"R²={r**2:.3f}")
    ax.set_title(f"{stage} | {mode}", fontweight="bold", fontsize=10)
    ax.set_xlabel("Theoretical Quantiles")
    ax.set_ylabel("log₁₀(Current Density)")
    ax.legend(fontsize=8, frameon=True)
    ax.grid(alpha=0.3)

for idx in range(n_groups, len(axes6)):
    axes6[idx].set_visible(False)

plt.tight_layout()
plt.savefig("plot6_qqplots.png")
plt.close('all')
print("✔ Plot 6 saved: plot6_qqplots.png")

# ============================================================
# PLOT 7 — Animated Bootstrap of Group Medians
# ============================================================
N_BOOT = 400
STAGES = ["Melting", "Synthesis"]
MODES_BOOT = sorted(df["Mode"].unique().tolist())  # derived from data

boot_results = {(s, m): [] for s in STAGES for m in MODES_BOOT}
rng = np.random.default_rng(42)

for s in STAGES:
    for m in MODES_BOOT:
        sub = df[(df["Stage"] == s) & (df["Mode"] == m)]["Current Density"].dropna().values
        if len(sub) < 2:
            continue
        medians = [np.median(rng.choice(sub, size=len(sub), replace=True))
                   for _ in range(N_BOOT)]
        boot_results[(s, m)] = np.log10(medians)

fig7, axes7 = plt.subplots(1, len(MODES_BOOT), figsize=(12, 5), sharey=False)
fig7.suptitle("Bootstrap Distribution of Median Current Density\n(Animated — 400 iterations)",
              fontsize=13, fontweight="bold")

bin_edges = {(s, m): np.linspace(boot_results[(s, m)].min() - 0.2,
                                  boot_results[(s, m)].max() + 0.2, 35)
             for s in STAGES for m in MODES_BOOT if len(boot_results[(s, m)]) > 0}

bars_dict = {}
for ax, mode in zip(axes7, MODES_BOOT):
    ax.set_title(f"Mode: {mode}", fontweight="bold")
    ax.set_xlabel("log₁₀(Median Current Density)")
    ax.set_ylabel("Count")
    ax.grid(alpha=0.3)
    bars_dict[mode] = {}
    for stage in STAGES:
        key = (stage, mode)
        if not len(boot_results[key]):
            continue
        counts, edges = np.histogram([], bins=bin_edges[key])
        widths = np.diff(edges)
        bars = ax.bar(edges[:-1], counts, width=widths, align="edge",
                      color=PALETTE[stage], alpha=0.6, label=stage, edgecolor="white")
        bars_dict[mode][stage] = (bars, bin_edges[key])
    ax.legend(title="Stage", frameon=True)

def update(frame):
    n = frame + 1
    for mode in MODES_BOOT:
        ax = axes7[MODES_BOOT.index(mode)]
        y_max = 0
        for stage in STAGES:
            key = (stage, mode)
            if key not in bars_dict[mode] or not len(boot_results[key]):
                continue
            bars, edges = bars_dict[mode][stage]
            counts, _ = np.histogram(boot_results[key][:n], bins=edges)
            for bar, h in zip(bars, counts):
                bar.set_height(h)
            y_max = max(y_max, counts.max() if counts.max() > 0 else 1)
        ax.set_ylim(0, y_max * 1.25)
    return []

ani = FuncAnimation(fig7, update, frames=N_BOOT, interval=15, blit=False)
ani.save("plot7_bootstrap_animation.gif", writer=PillowWriter(fps=30))
plt.close(fig7)
print("✔ Plot 7 saved: plot7_bootstrap_animation.gif")

# ============================================================
# PLOT 8 — Interactive Plotly Violin (HTML export)
# ============================================================
df_plot = df.copy()
df_plot["hover"] = (df_plot["Stage"] + " | " + df_plot["Mode"] +
                    " | " + df_plot["Material"])

fig8 = px.violin(
    df_plot,
    y="Current Density",
    x="Mode",
    color="Stage",
    facet_col="Material",
    log_y=True,
    box=True,
    points="all",
    color_discrete_map=PALETTE,
    hover_data=["Current Density", "Stage", "Mode", "Material"],
    title="Interactive Violin: Current Density by Mode, Stage and Material",
    labels={"Current Density": "Current Density (A/cm²)", "Mode": "Microscopy Mode"},
    template="plotly_white",
)
fig8.update_traces(meanline_visible=True, jitter=0.4, pointpos=-0.9)
fig8.update_layout(
    font_family="serif",
    title_font_size=15,
    legend_title_text="Stage",
    violingap=0.3,
    violingroupgap=0.1,
)
fig8.write_html("plot8_interactive_violin.html")
fig8.show()
print("✔ Plot 8 saved: plot8_interactive_violin.html")

# ============================================================
# PLOT 9 — Pairwise Statistical Summary (publication table figure)
# ============================================================
from itertools import combinations

pairs = list(combinations(STAGES, 2))
rows = []
for mode in df["Mode"].unique():
    for mat in df["Material"].unique():
        sub = df[(df["Mode"] == mode) & (df["Material"] == mat)]
        if sub.empty:
            continue
        for s1, s2 in pairs:
            g1 = sub[sub["Stage"] == s1]["Current Density"].dropna()
            g2 = sub[sub["Stage"] == s2]["Current Density"].dropna()
            if len(g1) < 2 or len(g2) < 2:
                continue
            stat, p = mannwhitneyu(g1, g2, alternative="two-sided")
            # Log-scale Cohen's d
            d = ((np.log10(g1).mean() - np.log10(g2).mean()) /
                 np.sqrt((np.log10(g1).std()**2 + np.log10(g2).std()**2) / 2))
            rows.append({"Mode": mode, "Material": mat,
                         "Comparison": f"{s1} vs {s2}",
                         "n₁": len(g1), "n₂": len(g2),
                         "U-stat": round(stat, 1), "p-value": round(p, 4),
                         "Cohen d (log)": round(d, 3)})

stats_df = pd.DataFrame(rows)
print("\n── Statistical Tests ──────────────────────────────")
print(stats_df.to_string(index=False))

# Render as a figure
fig9, ax9 = plt.subplots(figsize=(13, 0.5 * len(stats_df) + 1.5))
ax9.axis("off")
tbl = ax9.table(
    cellText=stats_df.values,
    colLabels=stats_df.columns,
    cellLoc="center",
    loc="center",
    bbox=[0, 0, 1, 1],
)
tbl.auto_set_font_size(False)
tbl.set_fontsize(9)
# Style header
for j in range(len(stats_df.columns)):
    tbl[0, j].set_facecolor("#2c3e50")
    tbl[0, j].set_text_props(color="white", fontweight="bold")
# Color rows by significance
for i, row in enumerate(stats_df.itertuples(), start=1):
    color = "#fde8e8" if row._7 < 0.05 else "#e8f4fd"
    for j in range(len(stats_df.columns)):
        tbl[i, j].set_facecolor(color)

fig9.suptitle("Mann-Whitney U Tests: Melting vs Synthesis\n(red = significant p < 0.05)",
              fontsize=13, fontweight="bold")
plt.savefig("plot9_statistics_table.png")
plt.close('all')
print("✔ Plot 9 saved: plot9_statistics_table.png")

# ============================================================
# PLOT 10 — Kruskal-Wallis across Modes + Effect Size Heatmap
# ============================================================
kw_rows = []
for stage in STAGES:
    groups_kw = [df[(df["Stage"] == stage) & (df["Mode"] == m)]["Current Density"].dropna()
                 for m in df["Mode"].unique()]
    groups_kw = [g for g in groups_kw if len(g) >= 2]
    if len(groups_kw) < 2:
        continue
    H, p = kruskal(*groups_kw)
    kw_rows.append({"Stage": stage, "H-statistic": round(H, 3), "p-value": round(p, 6)})

print("\n── Kruskal-Wallis (across Modes) ───────────────────")
print(pd.DataFrame(kw_rows).to_string(index=False))

# Effect size matrix (log Cohen's d) between all Mode pairs
mode_pairs = list(combinations(df["Mode"].unique(), 2))
effect_data = []
for stage in STAGES:
    row = {}
    for m1, m2 in mode_pairs:
        g1 = np.log10(df[(df["Stage"] == stage) & (df["Mode"] == m1)]["Current Density"].dropna())
        g2 = np.log10(df[(df["Stage"] == stage) & (df["Mode"] == m2)]["Current Density"].dropna())
        if len(g1) < 2 or len(g2) < 2:
            row[f"{m1}↔{m2}"] = np.nan
            continue
        d = abs((g1.mean() - g2.mean()) /
                np.sqrt((g1.std()**2 + g2.std()**2) / 2))
        row[f"{m1}↔{m2}"] = round(d, 3)
    effect_data.append({"Stage": stage, **row})

effect_df = pd.DataFrame(effect_data).set_index("Stage")

fig10, ax10 = plt.subplots(figsize=(8, 3))
sns.heatmap(effect_df.astype(float), annot=True, fmt=".2f",
            cmap="RdYlGn_r", linewidths=0.5, vmin=0, vmax=5,
            cbar_kws={"label": "|Cohen's d| (log scale)"},
            ax=ax10)
ax10.set_title("Effect Size between Microscopy Modes\n(|Cohen's d| on log₁₀ scale)",
               fontweight="bold")
ax10.set_xlabel("Mode Pair")
ax10.set_ylabel("Stage")
plt.tight_layout()
plt.savefig("plot10_effect_size_heatmap.png")
plt.close('all')
print("✔ Plot 10 saved: plot10_effect_size_heatmap.png")

# ============================================================
print("\n" + "="*55)
print(" All 10 plots generated successfully.")
print("="*55)
print("\nOutput files:")
for f in [
    "plot1_raincloud.png",
    "plot2_violin_swarm.png",
    "plot3_ecdf.png",
    "plot4_heatmap.png",
    "plot5_faceted_box.png",
    "plot6_qqplots.png",
    "plot7_bootstrap_animation.gif",
    "plot8_interactive_violin.html",
    "plot9_statistics_table.png",
    "plot10_effect_size_heatmap.png",
]:
    print(f"  {f}")
