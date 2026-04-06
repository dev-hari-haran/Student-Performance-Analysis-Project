# =============================================================================
# 05_correlation.py
# Student Performance Analysis — Correlation Heatmap & Pairplot
# Dataset: student-mat-clean.csv
# Output:  outputs/charts/05_correlation/
# =============================================================================

import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from itertools import combinations

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "student-mat-clean.csv")
OUT_DIR   = os.path.join(BASE_DIR, "outputs", "charts", "05_correlation")
os.makedirs(OUT_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# Load
# ---------------------------------------------------------------------------
df = pd.read_csv(DATA_PATH)

# Core columns for correlation analysis
CORR_COLS = [c for c in ["studytime", "failures", "absences", "G1", "G2", "G3"]
             if c in df.columns]

print("=" * 60)
print("Correlation Analysis")
print(f"Columns : {CORR_COLS}")
print("=" * 60)

corr_df = df[CORR_COLS].dropna()

# ---------------------------------------------------------------------------
# 1. Pearson Correlation Matrix — Print
# ---------------------------------------------------------------------------
corr_matrix = corr_df.corr(method="pearson")
print("\nPearson Correlation Matrix:")
print(corr_matrix.round(3).to_string())

# ---------------------------------------------------------------------------
# 2. Heatmap
# ---------------------------------------------------------------------------
def _annotated_heatmap(matrix, title, filename):
    n = len(matrix)
    fig, ax = plt.subplots(figsize=(8, 6))

    # Custom diverging colormap: blue → white → red
    cmap = plt.cm.RdBu_r
    im = ax.imshow(matrix.values, cmap=cmap, vmin=-1, vmax=1, aspect="auto")

    # Colorbar
    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label("Pearson r", fontsize=10)

    # Ticks
    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.set_xticklabels(matrix.columns, rotation=40, ha="right", fontsize=10)
    ax.set_yticklabels(matrix.index, fontsize=10)

    # Annotate cells
    for i in range(n):
        for j in range(n):
            val = matrix.values[i, j]
            text_color = "white" if abs(val) > 0.6 else "black"
            ax.text(j, i, f"{val:.2f}", ha="center", va="center",
                    fontsize=9, color=text_color, fontweight="bold")

    ax.set_title(title, fontsize=14, fontweight="bold", pad=14)
    plt.tight_layout()
    for ext in ("png", "pdf"):
        fig.savefig(os.path.join(OUT_DIR, f"{filename}.{ext}"),
                    dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  ✔ Saved: {filename}.png / .pdf")


_annotated_heatmap(corr_matrix,
                   "Pearson Correlation Heatmap\n(studytime, failures, absences, G1, G2, G3)",
                   "correlation_heatmap")

# ---------------------------------------------------------------------------
# 3. Manual Pairplot  (scatter grid + histograms on diagonal)
# ---------------------------------------------------------------------------
n = len(CORR_COLS)
fig2, axes = plt.subplots(n, n, figsize=(3.2 * n, 3.0 * n))
fig2.suptitle("Pairplot — Key Performance Variables", fontsize=15,
              fontweight="bold", y=1.01)

SCATTER_COLOR = "#4C72B0"
HIST_COLOR    = "#55A868"

for i, row_col in enumerate(CORR_COLS):
    for j, col_col in enumerate(CORR_COLS):
        ax = axes[i][j]
        if i == j:
            # Diagonal — histogram
            ax.hist(corr_df[row_col], bins=18, color=HIST_COLOR,
                    edgecolor="white", linewidth=0.5)
            ax.set_facecolor("#f7f7f7")
        else:
            # Off-diagonal — scatter
            ax.scatter(corr_df[col_col], corr_df[row_col],
                       alpha=0.25, s=12, color=SCATTER_COLOR, edgecolors="none")
            # Mini regression line
            x_vals = corr_df[col_col].values
            y_vals = corr_df[row_col].values
            if np.std(x_vals) > 0:
                m, b = np.polyfit(x_vals, y_vals, 1)
                x_range = np.linspace(x_vals.min(), x_vals.max(), 50)
                ax.plot(x_range, m * x_range + b, color="#C44E52",
                        linewidth=1.2, alpha=0.85)
            ax.set_facecolor("#fafafa")

        # Labels only on edges
        if i == n - 1:
            ax.set_xlabel(col_col, fontsize=8)
        else:
            ax.set_xticklabels([])
        if j == 0:
            ax.set_ylabel(row_col, fontsize=8)
        else:
            ax.set_yticklabels([])

        ax.tick_params(labelsize=7)

plt.tight_layout()
for ext in ("png", "pdf"):
    fig2.savefig(os.path.join(OUT_DIR, f"pairplot.{ext}"),
                 dpi=130, bbox_inches="tight")
plt.close(fig2)
print("  ✔ Saved: pairplot.png / .pdf")

# ---------------------------------------------------------------------------
# 4. Top Correlations with G3 — Bar Chart
# ---------------------------------------------------------------------------
g3_corr = corr_matrix["G3"].drop("G3").sort_values(key=abs, ascending=False)

fig3, ax3 = plt.subplots(figsize=(8, 4))
bar_colors = ["#C44E52" if v < 0 else "#4C72B0" for v in g3_corr.values]
bars = ax3.barh(g3_corr.index, g3_corr.values, color=bar_colors,
                edgecolor="white", height=0.55)
ax3.bar_label(bars, fmt="%.3f", padding=4, fontsize=9, fontweight="bold")
ax3.axvline(0, color="black", linewidth=0.8)
ax3.set_xlim(-1.1, 1.1)
ax3.set_title("Pearson Correlation with Final Grade (G3)",
              fontsize=13, fontweight="bold")
ax3.set_xlabel("Pearson r")
ax3.invert_yaxis()
plt.tight_layout()
for ext in ("png", "pdf"):
    fig3.savefig(os.path.join(OUT_DIR, f"g3_correlations_bar.{ext}"),
                 dpi=150, bbox_inches="tight")
plt.close(fig3)
print("  ✔ Saved: g3_correlations_bar.png / .pdf")

# ---------------------------------------------------------------------------
# 5. Insight Summary
# ---------------------------------------------------------------------------
print()
print("=" * 60)
print("INSIGHT SUMMARY — Strongest Predictors of G3")
print("=" * 60)
for var, val in g3_corr.items():
    direction = "↑ positive" if val > 0 else "↓ negative"
    strength  = ("strong" if abs(val) >= 0.6
                 else "moderate" if abs(val) >= 0.3
                 else "weak")
    print(f"  {var:>12}  r = {val:+.3f}  ({strength} {direction})")
print(f"\n  All charts saved to: {OUT_DIR}")
print("=" * 60)
