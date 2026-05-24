"""
Plot SE_300_2025.csv — I_EBIC and I_PE vs time.
Output: plot_SE_300_2025.png
"""
import pathlib
import pandas as pd
import matplotlib.pyplot as plt
from style import RC, C_PE, C_SE2 as C_EBIC, FACECOLOR

HERE = pathlib.Path(__file__).parent
plt.rcParams.update(RC)

df = pd.read_csv(HERE / "SE_300_2025.csv")
df.columns = df.columns.str.strip()

T_EBIC = r"$\mathit{I}_\mathrm{EBIC}$"
T_PE   = r"$\mathit{I}_\mathrm{PE}$"

ebic = df[df["Type"] == T_EBIC].sort_values("T/s")
pe   = df[df["Type"] == T_PE  ].sort_values("T/s")

fig, ax = plt.subplots(figsize=(8, 5))
fig.patch.set_facecolor(FACECOLOR)
ax.set_facecolor(FACECOLOR)

ax.plot(pe["T/s"],   pe["I_se/nA"],   color=C_PE,   lw=1.8, ls="--", label=r"$I_\mathrm{PE}$")
ax.plot(ebic["T/s"], ebic["I_se/nA"], color=C_EBIC, lw=1.8,          label=r"$I_\mathrm{EBIC}$")

ax.set_xlim(left=0)
ax.set_xlabel(r"$t$ / s")
ax.set_ylabel(r"$I$ / nA")
ax.set_title("300 kV", fontweight="bold")
ax.legend(framealpha=0.9)
ax.grid(alpha=0.25, linestyle="--")

fig.tight_layout()
fig.savefig(HERE / "plot_SE_300_2025.png")
plt.close(fig)
print("Saved plot_SE_300_2025.png")
