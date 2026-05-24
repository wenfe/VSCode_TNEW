"""
Plot I_P and I_se vs t for Linear_80_2025 and Linear_300_2025.
Output: plot_linear_currents.png
"""
import pathlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from style import RC, C_PE, C_SE, C_SE2, FACECOLOR

HERE = pathlib.Path(__file__).parent
plt.rcParams.update(RC)

lin_80  = pd.read_csv(HERE / "Linear_80_2025.csv");  lin_80.columns  = lin_80.columns.str.strip();  lin_80  = lin_80.dropna()
lin_300 = pd.read_csv(HERE / "Linear_300_2025.csv"); lin_300.columns = lin_300.columns.str.strip(); lin_300 = lin_300.dropna()

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5), sharey=False)
fig.patch.set_facecolor(FACECOLOR)

for ax, df, c_se, title in [
    (ax1, lin_80,  C_SE,  "80 kV"),
    (ax2, lin_300, C_SE2, "300 kV"),
]:
    ax.set_facecolor(FACECOLOR)
    ax.plot(df["T/s"], df["I_P/nA"],  color=C_PE, lw=1.8, ls="--", label=r"$I_\mathrm{PE}$")
    ax.plot(df["T/s"], df["I_se/nA"], color=c_se, lw=1.5,           label=r"$I_\mathrm{EBIC}$")
    ax.set_xlim(left=0)
    ax.set_xlabel(r"$t$ / s")
    ax.set_ylabel(r"$I$ / nA")
    ax.set_title(title, fontweight="bold")
    ax.legend(framealpha=0.9)
    ax.grid(alpha=0.25, linestyle="--")

fig.tight_layout(rect=[0, 0, 1, 1])
fig.savefig(HERE / "plot_linear_currents.png")
plt.close(fig)
print("Saved plot_linear_currents.png")
