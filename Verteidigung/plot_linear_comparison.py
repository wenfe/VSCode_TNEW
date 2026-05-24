"""
Side-by-side scatter comparison: I_EBIC vs I_PE for 80 kV and 300 kV.
Output: plot_linear_comparison.png
"""
import pathlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from style import RC, C_PE, C_SE, C_SE2, FACECOLOR

HERE = pathlib.Path(__file__).parent
plt.rcParams.update(RC)


def load_and_fit(path):
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip()
    df = df.dropna()
    x = df["I_P/nA"].values
    y = df["I_se/nA"].values
    eta = np.dot(x, y) / np.dot(x, x)
    residuals = y - eta * x
    n = len(x)
    sigma_eta = np.sqrt((residuals**2).sum() / (n - 1)) / np.sqrt(np.dot(x, x))
    return df, x, y, eta, sigma_eta


df80,  x80,  y80,  eta80,  sig80  = load_and_fit(HERE / "Linear_80_2025.csv")
df300, x300, y300, eta300, sig300 = load_and_fit(HERE / "Linear_300_2025.csv")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 6))
fig.patch.set_facecolor(FACECOLOR)

datasets = [
    (ax1, df80,  x80,  y80,  eta80,  sig80,  C_SE,  "80 kV,  32 nA"),
    (ax2, df300, x300, y300, eta300, sig300, C_SE2, "300 kV,  50 nA"),
]

for ax, df, x, y, eta, sigma_eta, c_ebic, title in datasets:
    ax.set_facecolor(FACECOLOR)
    sc = ax.scatter(x, y, c=df["T/s"].values, cmap="viridis",
                    s=6, alpha=0.6, label="data")
    fig.colorbar(sc, ax=ax, label=r"$t$ / s")
    x_fit = np.array([0, x.max()])
    ax.plot(x_fit, eta * x_fit, color=C_PE, lw=2,
            label=rf"$I_\mathrm{{EBIC}} = ({eta:.4f} \pm {sigma_eta:.4f})\, I_\mathrm{{PE}}$")
    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)
    ax.set_xlabel(r"$I_\mathrm{PE}$ / nA")
    ax.set_ylabel(r"$I_\mathrm{EBIC}$ / nA")
    ax.set_title(title, fontweight="bold")
    ax.legend(framealpha=0.9)
    ax.grid(alpha=0.25, linestyle="--")

fig.suptitle(r"$I_\mathrm{EBIC}$ vs $I_\mathrm{PE}$ — linear regime",
             fontsize=15, fontweight="bold")
fig.tight_layout()
fig.savefig(HERE / "plot_linear_comparison.png")
plt.close(fig)
print("Saved plot_linear_comparison.png")
