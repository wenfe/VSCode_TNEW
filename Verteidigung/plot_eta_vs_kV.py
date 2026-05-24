"""
Secondary-electron yield η vs accelerating voltage.
Derives η and σ_η from Linear_80_2025.csv and Linear_300_2025.csv via
origin-forced linear fit, then plots a 2-point summary with error bars.
Output: plot_eta_vs_kV.png
"""
import pathlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from style import RC, C_PE, C_SE, C_SE2, FACECOLOR

HERE = pathlib.Path(__file__).parent
plt.rcParams.update(RC)


def fit_eta(path):
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip()
    df = df.dropna()
    x = df["I_P/nA"].values
    y = df["I_se/nA"].values
    eta = np.dot(x, y) / np.dot(x, x)
    residuals = y - eta * x
    n = len(x)
    sigma_eta = np.sqrt((residuals**2).sum() / (n - 1)) / np.sqrt(np.dot(x, x))
    return eta, sigma_eta


eta80,  sig80  = fit_eta(HERE / "Linear_80_2025.csv")
eta300, sig300 = fit_eta(HERE / "Linear_300_2025.csv")

voltages = [80, 300]
etas     = [eta80,  eta300]
sigmas   = [sig80,  sig300]
colors   = [C_SE,   C_SE2]

fig, ax = plt.subplots(figsize=(6, 5))
fig.patch.set_facecolor(FACECOLOR)
ax.set_facecolor(FACECOLOR)

for v, eta, sigma, c in zip(voltages, etas, sigmas, colors):
    ax.errorbar(v, eta, yerr=sigma,
                fmt="o", color=c, markersize=9, capsize=6, capthick=2,
                elinewidth=2, zorder=3,
                label=rf"$\eta_{{{v}\,\mathrm{{kV}}}} = {eta:.4f} \pm {sigma:.4f}$")

# guide line connecting the two points
ax.plot(voltages, etas, color="#aaaaaa", lw=1.2, ls="--", zorder=2)

ax.set_xlim(0, 380)
ax.set_ylim(bottom=0)
ax.set_xlabel(r"Accelerating voltage / kV")
ax.set_ylabel(r"SE yield $\eta = I_\mathrm{EBIC} / I_\mathrm{PE}$")
ax.set_title(r"SE yield vs accelerating voltage", fontweight="bold")
ax.set_xticks(voltages)
ax.legend(framealpha=0.9)
ax.grid(alpha=0.25, linestyle="--")

fig.tight_layout()
fig.savefig(HERE / "plot_eta_vs_kV.png")
plt.close(fig)
print("Saved plot_eta_vs_kV.png")
