"""
Plot SE_20240807.csv and BSE_20240806.csv - single-panel raw energy spectra.
Left axis : SE counts (full range).
Right axis: Reflected ("Primary") + Transmitted/100 ("Primary x100"), both >149 keV.
Output: plot_SE_20240807.png
"""
import pathlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from style import RC, C_SE, C_SE2, C_PE, FACECOLOR

HERE = pathlib.Path(__file__).parent
plt.rcParams.update(RC)

se  = pd.read_csv(HERE / "SE_20240807.csv");  se.columns  = se.columns.str.strip()
bse = pd.read_csv(HERE / "BSE_20240806.csv"); bse.columns = bse.columns.str.strip()

E_se  = se["Energy/keV"].values
E_bse = bse["Energy/keV"].values
y_se  = se["SE/counts"].values
y_ref = bse["Reflected/counts"].values
y_tra = bse["Transmitted/counts"].values / 100   # Primary100

# Cut BSE curves at Energy > 149 keV
mask = E_bse > 149
E_bse_cut = E_bse[mask]
y_ref_cut = y_ref[mask]
y_tra_cut = y_tra[mask]

C_TRA = "#1b7837"

fig, ax1 = plt.subplots(figsize=(9, 5))
ax2 = ax1.twinx()
fig.patch.set_facecolor(FACECOLOR)
ax1.set_facecolor(FACECOLOR)

# Left axis: SE
l1, = ax1.plot(E_se, y_se, color=C_SE, lw=1.8, label=r"SE (2024-08-07)")
ax1.fill_between(E_se, y_se, alpha=0.10, color=C_SE)

# Right axis: Reflected + Transmitted/100
l2, = ax2.plot(E_bse_cut, y_ref_cut, color="royalblue", lw=1.6,
               label=r"Deflected Primary Electrons")
l3, = ax2.plot(E_bse_cut, y_tra_cut, color=C_TRA, lw=1.6,
               label=r"Deflected Primary Electrons x100")
ax2.fill_between(E_bse_cut, y_ref_cut, alpha=0.12, color="royalblue")
ax2.fill_between(E_bse_cut, y_tra_cut, alpha=0.12, color=C_TRA)

# Annotate SE peak
i_peak = np.argmax(y_se)
ax1.annotate(
    rf"SE peak at {E_se[i_peak]:.1f} keV",
    xy=(E_se[i_peak], y_se[i_peak]),
    xytext=(8, y_se[i_peak] * 0.75),
    arrowprops=dict(arrowstyle="->", color=C_SE, lw=1.2),
    color=C_SE, fontsize=10,
)

ax1.set_xlim(-1, 301)
ax1.set_ylim(bottom=0)
ax2.set_ylim(0, 50000)
ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x/1e3:.0f}"))

ax1.set_xlabel(r"Energy / keV")
ax1.set_ylabel("SE counts", color=C_SE)
ax2.set_ylabel(r"Primary electron counts (x10^3)", color="royalblue")
ax1.tick_params(axis="y", labelcolor=C_SE)
ax2.tick_params(axis="y", labelcolor="royalblue")

ax1.set_title("Electron spectra - 2024-08-06/07", fontsize=13, fontweight="bold")
lines = [l1, l2, l3]
ax1.legend(lines, [l.get_label() for l in lines], framealpha=0.9, fontsize=10, loc="upper left")
ax1.grid(alpha=0.25, linestyle="--")

fig.tight_layout()
fig.savefig(HERE / "plot_SE_20240807.png", dpi=150)
plt.close(fig)
print("Saved plot_SE_20240807.png")
