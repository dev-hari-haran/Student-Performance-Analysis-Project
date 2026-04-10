# =============================================================================
# 06_lifestyle.py
# Student Performance Analysis — Lifestyle Impact on Grades
# Covers: Alcohol consumption (Dalc, Walc) & Social activities (goout)
# Dataset: student-mat-clean.csv
# Output:  outputs/charts/06_lifestyle/
# =============================================================================

import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from scipy import stats

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "student-mat-clean.csv")
OUT_DIR   = os.path.join(BASE_DIR, "outputs", "charts", "06_lifestyle")
os.makedirs(OUT_DIR, exist_ok=True)

# Scale labels (1–5)
SCALE_LABELS = {1: "Very Low", 2: "Low", 3: "Moderate", 4: "High", 5: "Very High"}
GOOUT_LABELS = {1: "Rarely", 2: "Occasionally", 3: "Sometimes", 4: "Often", 5: "Very Often"}

# ---------------------------------------------------------------------------
# Load
# ---------------------------------------------------------------------------
df = pd.read_csv(DATA_PATH)

# Compute combined alcohol score if both columns exist
if "Dalc" in df.columns and "Walc" in df.columns:
    df["alc_total"] = (df["Dalc"] + df["Walc"]) / 2
elif "Walc" in df.columns:
    df["alc_total"] = df["Walc"]
elif "Dalc" in df.columns:
    df["alc_total"] = df["Dalc"]
else:
    df["alc_total"] = None

print("=" * 60)
print("Lifestyle Impact Analysis")
print("=" * 60)

# ============================================================
# SECTION A — ALCOHOL CONSUMPTION vs GRADES
# ============================================================

# ---------------------------------------------------------------------------
# A1. Summary table — Workday & Weekend alcohol vs G3
# ---------------------------------------------------------------------------
for col, label in [("Dalc", "Workday Alcohol"), ("Walc", "Weekend Alcohol")]:
    if col not in df.columns:
        continue
    summ = df.groupby(col)["G3"].agg(["mean", "median", "std", "count"])
    summ.index = [SCALE_LABELS.get(i, i) for i in summ.index]
    print(f"\n{label} (Dalc) → G3 Summary:")
    print(summ.to_string())

# ---------------------------------------------------------------------------
# A2. Side-by-side Bar Chart — Dalc & Walc vs Mean G3
# ---------------------------------------------------------------------------
available_alc = [c for c in ["Dalc", "Walc"] if c in df.columns]
if available_alc:
    levels = sorted(SCALE_LABELS.keys())
    x = np.arange(len(levels))
    width = 0.38
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    colors_alc = {"Dalc": "#C44E52", "Walc": "#DD8452"}
    labels_alc = {"Dalc": "Workday Alcohol (Dalc)", "Walc": "Weekend Alcohol (Walc)"}
    offset = -width / 2
    for col in available_alc:
        means = [df.loc[df[col] == lv, "G3"].mean() for lv in levels]
        bars = ax1.bar(x + offset, means, width, label=labels_alc[col],
                       color=colors_alc[col], edgecolor="white")
        ax1.bar_label(bars, fmt="%.1f", padding=3, fontsize=8)
        offset += width

    ax1.set_xticks(x)
    ax1.set_xticklabels([SCALE_LABELS[lv] for lv in levels], rotation=15, ha="right")
    ax1.set_title("Mean Final Grade (G3) by Alcohol Consumption Level",
                  fontsize=13, fontweight="bold")
    ax1.set_ylabel("Mean G3 (0–20)")
    ax1.set_ylim(0, 22)
    ax1.axhline(df["G3"].mean(), color="grey", linestyle="--", linewidth=1,
                label=f"Overall Mean: {df['G3'].mean():.2f}")
    ax1.legend()
    plt.tight_layout()
    for ext in ("png", "pdf"):
        fig1.savefig(os.path.join(OUT_DIR, f"alcohol_vs_g3_bar.{ext}"),
                     dpi=150, bbox_inches="tight")
    plt.close(fig1)
    print("\n  ✔ Saved: alcohol_vs_g3_bar.png / .pdf")

# ---------------------------------------------------------------------------
# A3. Box Plot — Combined Alcohol Score vs G3
# ---------------------------------------------------------------------------
if "alc_total" in df.columns and df["alc_total"].notnull().any():
    df["alc_bin"] = pd.cut(df["alc_total"], bins=[0, 1.5, 2.5, 3.5, 4.5, 5.1],
                           labels=["Very Low", "Low", "Moderate", "High", "Very High"])
    groups_alc = [df.loc[df["alc_bin"] == lbl, "G3"].dropna().values
                  for lbl in ["Very Low", "Low", "Moderate", "High", "Very High"]
                  if lbl in df["alc_bin"].values]
    group_labels_alc = [lbl for lbl in ["Very Low", "Low", "Moderate", "High", "Very High"]
                        if lbl in df["alc_bin"].values]
    if groups_alc:
        fig2, ax2 = plt.subplots(figsize=(9, 5))
        bp = ax2.boxplot(groups_alc, labels=group_labels_alc, patch_artist=True,
                         medianprops=dict(color="black", linewidth=2))
        alc_colors = ["#4C72B0", "#55A868", "#FFC107", "#DD8452", "#C44E52"]
        for patch, c in zip(bp["boxes"], alc_colors):
            patch.set_facecolor(c)
            patch.set_alpha(0.75)
        ax2.set_title("G3 Distribution by Combined Alcohol Consumption",
                      fontsize=13, fontweight="bold")
        ax2.set_xlabel("Average Alcohol Consumption Level")
        ax2.set_ylabel("Final Grade G3 (0–20)")
        plt.tight_layout()
        for ext in ("png", "pdf"):
            fig2.savefig(os.path.join(OUT_DIR, f"alcohol_boxplot_g3.{ext}"),
                         dpi=150, bbox_inches="tight")
        plt.close(fig2)
        print("  ✔ Saved: alcohol_boxplot_g3.png / .pdf")

# ---------------------------------------------------------------------------
# A4. Scatter — alc_total vs G3 with regression
# ---------------------------------------------------------------------------
if "alc_total" in df.columns and df["alc_total"].notnull().any():
    sub = df[["alc_total", "G3"]].dropna()
    slope_a, intercept_a, r_a, p_a, _ = stats.linregress(sub["alc_total"], sub["G3"])
    fig3, ax3 = plt.subplots(figsize=(8, 5))
    jitter = np.random.uniform(-0.12, 0.12, len(sub))
    ax3.scatter(sub["alc_total"] + jitter, sub["G3"],
                alpha=0.30, s=20, color="#C44E52", edgecolors="none")
    x_fit = np.linspace(sub["alc_total"].min(), sub["alc_total"].max(), 100)
    ax3.plot(x_fit, slope_a * x_fit + intercept_a, color="#333333",
             linewidth=2, label=f"r = {r_a:.3f},  p = {p_a:.4f}")
    ax3.set_title("Alcohol Consumption vs Final Grade G3 (Scatter + Regression)",
                  fontsize=12, fontweight="bold")
    ax3.set_xlabel("Average Alcohol Score (1=Very Low … 5=Very High)")
    ax3.set_ylabel("Final Grade G3")
    ax3.legend()
    plt.tight_layout()
    for ext in ("png", "pdf"):
        fig3.savefig(os.path.join(OUT_DIR, f"scatter_alcohol_g3.{ext}"),
                     dpi=150, bbox_inches="tight")
    plt.close(fig3)
    print("  ✔ Saved: scatter_alcohol_g3.png / .pdf")

# ============================================================
# SECTION B — SOCIAL ACTIVITIES (goout) vs GRADES
# ============================================================

if "goout" in df.columns:
    # ---------------------------------------------------------------------------
    # B1. Summary table
    # ---------------------------------------------------------------------------
    summ_g = df.groupby("goout")["G3"].agg(["mean", "median", "std", "count"])
    summ_g.index = [GOOUT_LABELS.get(i, i) for i in summ_g.index]
    print("\nGoout (Social Activity) → G3 Summary:")
    print(summ_g.to_string())

    # ---------------------------------------------------------------------------
    # B2. Bar Chart — goout vs Mean G3
    # ---------------------------------------------------------------------------
    levels_g = sorted(df["goout"].dropna().unique().astype(int))
    means_g  = [df.loc[df["goout"] == lv, "G3"].mean() for lv in levels_g]
    labels_g = [GOOUT_LABELS.get(lv, str(lv)) for lv in levels_g]

    fig4, ax4 = plt.subplots(figsize=(9, 5))
    palette = cm.Blues(np.linspace(0.4, 0.85, len(levels_g)))
    bars4 = ax4.bar(labels_g, means_g, color=palette, edgecolor="white", width=0.55)
    ax4.bar_label(bars4, fmt="%.2f", padding=4, fontsize=9, fontweight="bold")
    ax4.axhline(df["G3"].mean(), color="grey", linestyle="--", linewidth=1,
                label=f"Overall Mean: {df['G3'].mean():.2f}")
    ax4.set_title("Mean Final Grade (G3) by Social Activity (Go Out) Level",
                  fontsize=13, fontweight="bold")
    ax4.set_xlabel("Social Activity Frequency")
    ax4.set_ylabel("Mean G3 (0–20)")
    ax4.set_ylim(0, 22)
    ax4.legend()
    plt.tight_layout()
    for ext in ("png", "pdf"):
        fig4.savefig(os.path.join(OUT_DIR, f"goout_vs_g3_bar.{ext}"),
                     dpi=150, bbox_inches="tight")
    plt.close(fig4)
    print("  ✔ Saved: goout_vs_g3_bar.png / .pdf")

    # ---------------------------------------------------------------------------
    # B3. Scatter + Regression — goout vs G3
    # ---------------------------------------------------------------------------
    sub_g = df[["goout", "G3"]].dropna()
    slope_g, intercept_g, r_g, p_g, _ = stats.linregress(sub_g["goout"], sub_g["G3"])
    fig5, ax5 = plt.subplots(figsize=(8, 5))
    jitter_g = np.random.uniform(-0.15, 0.15, len(sub_g))
    ax5.scatter(sub_g["goout"] + jitter_g, sub_g["G3"],
                alpha=0.30, s=20, color="#8172B2", edgecolors="none")
    x_fit_g = np.linspace(sub_g["goout"].min(), sub_g["goout"].max(), 100)
    ax5.plot(x_fit_g, slope_g * x_fit_g + intercept_g, color="#333333",
             linewidth=2, label=f"r = {r_g:.3f},  p = {p_g:.4f}")
    ax5.set_xticks(levels_g)
    ax5.set_xticklabels(labels_g)
    ax5.set_title("Social Activity (goout) vs Final Grade G3",
                  fontsize=13, fontweight="bold")
    ax5.set_xlabel("Social Activity Frequency")
    ax5.set_ylabel("Final Grade G3")
    ax5.legend()
    plt.tight_layout()
    for ext in ("png", "pdf"):
        fig5.savefig(os.path.join(OUT_DIR, f"scatter_goout_g3.{ext}"),
                     dpi=150, bbox_inches="tight")
    plt.close(fig5)
    print("  ✔ Saved: scatter_goout_g3.png / .pdf")

    # ---------------------------------------------------------------------------
    # B4. Combined Heatmap — goout × Walc vs Mean G3
    # ---------------------------------------------------------------------------
    if "Walc" in df.columns:
        pivot = df.pivot_table(values="G3", index="goout", columns="Walc", aggfunc="mean")
        pivot.index = [GOOUT_LABELS.get(i, i) for i in pivot.index]
        pivot.columns = [SCALE_LABELS.get(i, i) for i in pivot.columns]

        fig6, ax6 = plt.subplots(figsize=(9, 5))
        im = ax6.imshow(pivot.values, cmap="RdYlGn", aspect="auto",
                        vmin=df["G3"].min(), vmax=df["G3"].max())
        fig6.colorbar(im, ax=ax6, label="Mean G3")
        ax6.set_xticks(range(len(pivot.columns)))
        ax6.set_yticks(range(len(pivot.index)))
        ax6.set_xticklabels(pivot.columns, rotation=20, ha="right", fontsize=9)
        ax6.set_yticklabels(pivot.index, fontsize=9)
        for i in range(len(pivot.index)):
            for j in range(len(pivot.columns)):
                val = pivot.values[i, j]
                if not np.isnan(val):
                    ax6.text(j, i, f"{val:.1f}", ha="center", va="center",
                             fontsize=8, color="black", fontweight="bold")
        ax6.set_title("Mean G3 Heatmap: Social Activity (goout) × Weekend Alcohol (Walc)",
                      fontsize=12, fontweight="bold")
        ax6.set_xlabel("Weekend Alcohol Consumption")
        ax6.set_ylabel("Social Activity Frequency")
        plt.tight_layout()
        for ext in ("png", "pdf"):
            fig6.savefig(os.path.join(OUT_DIR, f"heatmap_goout_walc_g3.{ext}"),
                         dpi=150, bbox_inches="tight")
        plt.close(fig6)
        print("  ✔ Saved: heatmap_goout_walc_g3.png / .pdf")

# ---------------------------------------------------------------------------
# Insight Summary
# ---------------------------------------------------------------------------
print()
print("=" * 60)
print("INSIGHT SUMMARY — Lifestyle vs Academic Performance")
print("=" * 60)
if "alc_total" in df.columns and df["alc_total"].notnull().any():
    print(f"  Alcohol ↔ G3 : r = {r_a:+.3f}  (p = {p_a:.4f})")
    print(f"    → {'Negative' if r_a < 0 else 'Positive'} effect of alcohol on final grade")
if "goout" in df.columns:
    print(f"  Goout   ↔ G3 : r = {r_g:+.3f}  (p = {p_g:.4f})")
    print(f"    → {'Going out more is associated with lower grades' if r_g < 0 else 'No negative effect of going out'}")
print(f"\n  All charts saved to: {OUT_DIR}")
print("=" * 60)
