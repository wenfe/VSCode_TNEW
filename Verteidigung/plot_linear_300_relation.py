"""
Plot I_se vs I_P (linear relation) from Linear_300_2025.csv.
Output: plot_linear_300_relation.png
"""
import pathlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from style import RC, C_PE, C_SE2 as C_EBIC, FACECOLOR

HERE = pathlib.Path(__file__).parent
plt.rcParams.update(RC)

df = pd.read_csv(HERE / "Linear_300_2025.csv")
df.columns = df.columns.str.strip()
df = df.dropna()

x = df["I_P/nA"].values
y = df["I_se/nA"].values

# fit through origin
eta = np.dot(x, y) / np.dot(x, x)
x_fit = np.array([0, x.max()])

# residual std deviation and uncertainty on slope
residuals = y - eta * x
delta = residuals.std()
n = len(x)
sigma_eta = np.sqrt((residuals**2).sum() / (n - 1)) / np.sqrt(np.dot(x, x))
r2 = 1 - np.sum(residuals**2) / np.sum((y - y.mean())**2)

fig, (ax, ax_res) = plt.subplots(2, 1, figsize=(6, 7),
                                  gridspec_kw={"height_ratios": [3, 1]})
fig.patch.set_facecolor(FACECOLOR)
ax.set_facecolor(FACECOLOR)
ax_res.set_facecolor(FACECOLOR)

sc = ax.scatter(x, y, c=df["T/s"].values, cmap="viridis",
                s=6, alpha=0.6, label="data")
fig.colorbar(sc, ax=ax, label=r"$t$ / s")
ax.plot(x_fit, eta * x_fit, color=C_PE, lw=2,
        label=rf"$I_\mathrm{{EBIC}} = ({eta:.4f} \pm {sigma_eta:.4f})\, I_\mathrm{{PE}}$")

ax.set_xlim(left=0)
ax.set_ylim(bottom=0)
ax.set_xlabel(r"$I_\mathrm{PE}$ / nA")
ax.set_ylabel(r"$I_\mathrm{EBIC}$ / nA")
ax.set_title("300 kV,  50 nA — linear regime", fontweight="bold")
ax.legend(framealpha=0.9)
ax.grid(alpha=0.25, linestyle="--")

# ── Residuals vs time panel ───────────────────────────────────────────────
ax_res.scatter(df["T/s"].values, residuals, c=df["T/s"].values,
               cmap="viridis", s=5, alpha=0.6)
ax_res.axhline(0, color=C_PE, lw=1.5, ls="--")
ax_res.set_xlabel(r"$t$ / s")
ax_res.set_ylabel(r"Residual / nA")
ax_res.set_title("Residuals vs time", fontweight="bold")
ax_res.grid(alpha=0.25, linestyle="--")

fig.tight_layout()
fig.savefig(HERE / "plot_linear_300_relation.png")
plt.close(fig)
print("Saved plot_linear_300_relation.png")
