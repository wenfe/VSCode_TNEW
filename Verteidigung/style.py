"""
Shared matplotlib style — used by plot_linear_*.py, plot_SE_300.py.
Import with:
    from style import RC, C_PE, C_SE, C_SE2, FACECOLOR
    import matplotlib.pyplot as plt; plt.rcParams.update(RC)
"""

RC = {
    "font.family":       "serif",
    "font.size":         13,
    "axes.titlesize":    14,
    "axes.labelsize":    13,
    "xtick.labelsize":   11,
    "ytick.labelsize":   11,
    "legend.fontsize":   11,
    "figure.dpi":        120,
    "savefig.dpi":       150,
    "savefig.bbox":      "tight",
    "axes.spines.top":   True,
    "axes.spines.right": True,
}

FACECOLOR = "#fafafa"

C_PE   = "#e87722"   # orange  — primary / I_PE (dashed)
C_SE   = "#2166ac"   # blue    — I_EBIC  80 kV
C_SE2  = "#4393c3"   # blue    — I_EBIC 300 kV
