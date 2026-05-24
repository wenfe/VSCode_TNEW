"""
SE Current Analysis — 2025
==========================
Inputs:
  SE_80_2025.csv, SE_300_2025.csv  — sparse EBIC events + PE current vs time
  Linear_80_2025.csv, Linear_300_2025.csv — dense linear-regime measurements

Outputs:
  plot_T_Ise.png  — time series, 2-panel (80 kV | 300 kV)
  plot_IP_Ise.png — I_P vs I_se scatter with linear fits
"""

import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ── Global style (matches analysis.py) ──────────────────────────────────────
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

# Colours
C_80   = "#2166ac"   # blue   — 80 kV
C_300  = "#d6604d"   # red    — 300 kV
C_PE   = "#636363"   # grey   — primary / PE current
C_LIN  = "#4dac26"   # green  — linear regime overlay


# ── Load data ────────────────────────────────────────────────────────────────
se_80  = pd.read_csv("SE_80_2025.csv")
se_300 = pd.read_csv("SE_300_2025.csv")
lin_80  = pd.read_csv("Linear_80_2025.csv")
lin_300 = pd.read_csv("Linear_300_2025.csv")

# Strip any whitespace from column names
for df in (se_80, se_300, lin_80, lin_300):
    df.columns = df.columns.str.strip()

# ── Split SE files by Type ───────────────────────────────────────────────────
ebic_80 = se_80[se_80["Type"].str.contains("EBIC", na=False)].copy()
pe_80   = se_80[~se_80["Type"].str.contains("EBIC", na=False)].copy()

ebic_300 = se_300[se_300["Type"].str.contains("EBIC", na=False)].copy()
pe_300   = se_300[~se_300["Type"].str.contains("EBIC", na=False)].copy()

print(f"SE_80  — EBIC rows: {len(ebic_80)},  PE rows: {len(pe_80)}")
print(f"SE_300 — EBIC rows: {len(ebic_300)}, PE rows: {len(pe_300)}")
print(f"Linear_80  rows: {len(lin_80)}")
print(f"Linear_300 rows: {len(lin_300)}")


# ════════════════════════════════════════════════════════════════════════════
# PLOT 1 — T/s vs I_se/nA   (2-panel: 80 kV | 300 kV)
# ════════════════════════════════════════════════════════════════════════════
fig, (ax_80, ax_300) = plt.subplots(1, 2, figsize=(13, 5.5))


def _draw_timeseries(ax, ebic, pe, lin, color, color_lin, label_kv):
    """Populate one time-series panel; returns the twinned axis for the legend."""
    ax_b = ax.twinx()

    # Primary y — I_se: EBIC scatter
    ax.scatter(
        ebic["T/s"], ebic["I_se/nA"],
        s=18, color=color, alpha=0.7, zorder=3,
        label=r"$I_\mathrm{EBIC}$ events",
    )
    # Primary y — I_se: Linear-regime line
    ax.plot(
        lin["T/s"], lin["I_se/nA"],
        color=color_lin, lw=1.5, alpha=0.85, zorder=2,
        label=r"$I_\mathrm{se}$ (linear regime)",
    )

    # Secondary y — PE / primary current
    ax_b.plot(
        pe["T/s"], pe["I_se/nA"],
        color=C_PE, lw=1.2, alpha=0.8, ls="--",
        label=r"$I_\mathrm{PE}$",
    )

    ax.set_xlabel(r"$t$ / s")
    ax.set_ylabel(r"$I_\mathrm{se}$ / nA")
    ax_b.set_ylabel(r"$I_\mathrm{PE}$ / nA", color=C_PE)
    ax_b.tick_params(axis="y", labelcolor=C_PE)
    ax.set_title(label_kv)

    return ax_b


ax_80b  = _draw_timeseries(ax_80,  ebic_80,  pe_80,  lin_80,  C_80,  C_LIN, "80 kV")
ax_300b = _draw_timeseries(ax_300, ebic_300, pe_300, lin_300, C_300, C_LIN, "300 kV")

# Combined legend per panel (primary + secondary handles)
for ax_primary, ax_twin in [(ax_80, ax_80b), (ax_300, ax_300b)]:
    handles1, labels1 = ax_primary.get_legend_handles_labels()
    handles2, labels2 = ax_twin.get_legend_handles_labels()
    ax_primary.legend(handles1 + handles2, labels1 + labels2,
                      loc="upper left", framealpha=0.85)

fig.tight_layout()
fig.savefig("plot_T_Ise.png")
plt.close(fig)
print("Saved plot_T_Ise.png")


# ════════════════════════════════════════════════════════════════════════════
# PLOT 2 — I_P/nA vs I_se/nA
# ════════════════════════════════════════════════════════════════════════════

# ── Interpolate I_P for SE EBIC events (using PE T→I_se as I_P proxy) ───────
ip_at_ebic_80 = np.interp(
    ebic_80["T/s"].values,
    pe_80["T/s"].values,
    pe_80["I_se/nA"].values,
    left=np.nan,
    right=np.nan,
)
ip_at_ebic_300 = np.interp(
    ebic_300["T/s"].values,
    pe_300["T/s"].values,
    pe_300["I_se/nA"].values,
    left=np.nan,
    right=np.nan,
)

# Drop out-of-range interpolations (NaN)
mask_80  = ~np.isnan(ip_at_ebic_80)
mask_300 = ~np.isnan(ip_at_ebic_300)

# ── Fit through origin: η = (x·y) / (x·x) ──────────────────────────────────
def fit_origin(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    m = np.isfinite(x) & np.isfinite(y)
    xm, ym = x[m], y[m]
    slope = np.dot(xm, ym) / np.dot(xm, xm)
    return slope

eta_80  = fit_origin(lin_80["I_P/nA"],  lin_80["I_se/nA"])
eta_300 = fit_origin(lin_300["I_P/nA"], lin_300["I_se/nA"])
print(f"η (80 kV)  = {eta_80:.4f}")
print(f"η (300 kV) = {eta_300:.4f}")

fig2, ax = plt.subplots(figsize=(7, 5.5))

# Linear regime — filled scatter
ax.scatter(lin_80["I_P/nA"],  lin_80["I_se/nA"],
           s=12, color=C_80,  alpha=0.5, label="Linear 80 kV")
ax.scatter(lin_300["I_P/nA"], lin_300["I_se/nA"],
           s=12, color=C_300, alpha=0.5, label="Linear 300 kV")

# SE EBIC events — open circles
ax.scatter(ip_at_ebic_80[mask_80],   ebic_80["I_se/nA"].values[mask_80],
           s=40, color=C_80,  marker="o", facecolors="none", lw=1.2,
           label="SE events 80 kV")
ax.scatter(ip_at_ebic_300[mask_300], ebic_300["I_se/nA"].values[mask_300],
           s=40, color=C_300, marker="o", facecolors="none", lw=1.2,
           label="SE events 300 kV")

# Fit lines
x_range_80  = np.array([0, lin_80["I_P/nA"].max()  * 1.05])
x_range_300 = np.array([0, lin_300["I_P/nA"].max() * 1.05])
ax.plot(x_range_80,  eta_80  * x_range_80,  color=C_80,  lw=1.5, ls="--")
ax.plot(x_range_300, eta_300 * x_range_300, color=C_300, lw=1.5, ls="--")

# η annotation box
textstr = (
    rf"$\eta_{{80}} = {eta_80:.3f}$"
    "\n"
    rf"$\eta_{{300}} = {eta_300:.3f}$"
)
ax.text(
    0.05, 0.95, textstr,
    transform=ax.transAxes,
    fontsize=11,
    verticalalignment="top",
    bbox=dict(boxstyle="round,pad=0.4", facecolor="white", alpha=0.8),
)

ax.set_xlabel(r"$I_\mathrm{P}$ / nA")
ax.set_ylabel(r"$I_\mathrm{se}$ / nA")
ax.legend(loc="lower right", framealpha=0.85)
ax.set_xlim(left=0)

fig2.tight_layout()
fig2.savefig("plot_IP_Ise.png")
plt.close(fig2)
print("Saved plot_IP_Ise.png")
