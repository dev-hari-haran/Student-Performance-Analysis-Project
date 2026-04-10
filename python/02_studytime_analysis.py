"""
Student Performance Analysis
Task 2  —  Study Time vs Academic Performance
File    :  python/02_studytime_analysis.py
Run     :  VS Code Run Button (top right)
Output  :  outputs/charts/task2_*.png  &  task2_*.pdf
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
from scipy import stats
import os, warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────────────────
# PATHS
# ─────────────────────────────────────────────────────────────
BASE_DIR   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH  = os.path.join(BASE_DIR, "data",    "student-mat-clean.csv")
CHART_DIR  = os.path.join(BASE_DIR, "outputs", "charts")
os.makedirs(CHART_DIR, exist_ok=True)

ALPHA = 0.05

# ─────────────────────────────────────────────────────────────
# STYLE
# ─────────────────────────────────────────────────────────────
plt.rcParams.update({
    "font.family"       : "DejaVu Sans",
    "axes.spines.top"   : False,
    "axes.spines.right" : False,
    "axes.grid"         : True,
    "grid.alpha"        : 0.22,
    "grid.linestyle"    : "--",
    "axes.titlesize"    : 12,
    "axes.labelsize"    : 11,
    "xtick.labelsize"   : 10,
    "ytick.labelsize"   : 10,
})

# Task 2 color palette — Blues
BLUES = ["#BDD7EE", "#6BAED6", "#2171B5", "#08306B"]
BG    = "#F5F8FC"

# ─────────────────────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────────────────────
def load_data():
    df = pd.read_csv(DATA_PATH, sep=None, engine="python")
    print(f"  Loaded : {df.shape[0]} rows x {df.shape[1]} cols")
    print(f"  G3 range : {df['G3'].min()} – {df['G3'].max()}")
    return df

# ─────────────────────────────────────────────────────────────
# SAVE HELPER  (PNG + PDF)
# ─────────────────────────────────────────────────────────────
def save_chart(fig, name):
    for ext in ("png", "pdf"):
        path = os.path.join(CHART_DIR, f"{name}.{ext}")
        fig.savefig(path, dpi=180, bbox_inches="tight",
                    facecolor=fig.get_facecolor())
        print(f"  Saved  → {path}")

# ─────────────────────────────────────────────────────────────
# ANALYSIS
# ─────────────────────────────────────────────────────────────
def analyse(df):
    study_labels = {1: "< 2 hrs", 2: "2–5 hrs",
                    3: "5–10 hrs", 4: "> 10 hrs"}

    groups  = [df[df["studytime"] == lvl]["G3"].dropna().values
               for lvl in [1, 2, 3, 4]]
    means   = [g.mean()       for g in groups]
    medians = [np.median(g)   for g in groups]
    counts  = [len(g)         for g in groups]

    f_stat, p_anova = stats.f_oneway(*groups)
    rho,    p_spear = stats.spearmanr(df["studytime"], df["G3"])

    # ── Console summary
    print("\n" + "="*55)
    print("  TASK 2 — Study Time vs Academic Performance")
    print("="*55)
    print(f"\n  {'Group':<14} {'Mean G3':>8} {'Median':>8} {'n':>5}")
    print(f"  {'-'*37}")
    for i, lvl in enumerate([1, 2, 3, 4]):
        print(f"  {study_labels[lvl]:<14} {means[i]:>8.2f} "
              f"{medians[i]:>8.1f} {counts[i]:>5}")
    print(f"\n  ANOVA    F = {f_stat:.3f},  p = {p_anova:.4f}  "
          f"{'[Significant]' if p_anova < ALPHA else '[Not significant]'}")
    print(f"  Spearman ρ = {rho:.3f},   p = {p_spear:.4f}")

    return study_labels, groups, means, medians, counts, f_stat, p_anova, rho, p_spear

# ─────────────────────────────────────────────────────────────
# VISUALISATION  — 3 panels: Scatter | Boxplot | Bar chart
# ─────────────────────────────────────────────────────────────
# ─────────────────────────────────────────────────────────────
# VISUALISATION  — 3 panels: Scatter | Boxplot | Bar chart
# ─────────────────────────────────────────────────────────────
def visualise(df, study_labels, groups, means, medians,
              counts, f_stat, p_anova, rho, p_spear):

    fig = plt.figure(figsize=(18, 6), facecolor=BG)
    fig.suptitle(
        "Task 2  ·  Study Time vs Academic Performance",
        fontsize=15, fontweight="bold", color="#08306B", y=1.02
    )
    gs = gridspec.GridSpec(1, 3, figure=fig, wspace=0.40)

    # ── Panel A : Scatter plot with trend line ────────────────
    ax0 = fig.add_subplot(gs[0])
    ax0.set_facecolor("#EDF3FB")

    np.random.seed(42)
    jitter = np.random.uniform(-0.18, 0.18, len(df))
    sc = ax0.scatter(
        df["studytime"] + jitter, df["G3"],
        c=df["G3"], cmap="Blues", vmin=0, vmax=20,
        alpha=0.55, edgecolors="#2171B5", linewidths=0.25, s=40
    )
    
    # Calculate trend line safely
    xs = np.linspace(0.8, 4.2, 100)
    coeffs = np.polyfit(df["studytime"], df["G3"], 1)
    ax0.plot(xs, np.poly1d(coeffs)(xs),
             color="#E24B4A", lw=2, linestyle="--",
             label=f"Trend  ρ = {rho:+.2f}")
    
    ax0.set_xticks([1, 2, 3, 4])
    ax0.set_xticklabels([study_labels[i] for i in [1, 2, 3, 4]], fontsize=9)
    ax0.set_xlim(0.5, 4.5)
    ax0.set_ylim(-0.5, 21)
    ax0.set_xlabel("Study Time (hrs/week)")
    ax0.set_ylabel("Final Grade (G3)")
    ax0.set_title("Scatter Plot", fontweight="bold")
    ax0.legend(fontsize=9, loc="upper left")
    plt.colorbar(sc, ax=ax0, label="G3", shrink=0.75, pad=0.02)
    ax0.text(0.98, 0.04,
             f"Spearman ρ = {rho:.3f}\np = {p_spear:.4f}",
             transform=ax0.transAxes, ha="right", fontsize=8.5,
             color="#08306B",
             bbox=dict(boxstyle="round,pad=0.35",
                       fc="white", ec="#BDD7EE", lw=0.8))

    # ── Panel B : Boxplot ─────────────────────────────────────
    ax1 = fig.add_subplot(gs[1])
    ax1.set_facecolor("#EDF3FB")

    bp = ax1.boxplot(
        groups, patch_artist=True, widths=0.50,
        medianprops=dict(color="white", lw=2.5),
        whiskerprops=dict(color="#555"),
        capprops=dict(color="#555"),
        flierprops=dict(marker="o", mfc="#888", ms=3.5, ls="none")
    )
    for patch, c in zip(bp["boxes"], BLUES):
        patch.set_facecolor(c)
        patch.set_alpha(0.88)

    ax1.set_xticks([1, 2, 3, 4])
    ax1.set_xticklabels([study_labels[i] for i in [1, 2, 3, 4]], fontsize=9)
    ax1.set_ylim(-0.5, 21)
    ax1.set_xlabel("Study Time (hrs/week)")
    ax1.set_ylabel("Final Grade (G3)")
    ax1.set_title("Grade Distribution (Boxplot)", fontweight="bold")
    ax1.axhline(df["G3"].mean(), color="#E24B4A", ls="--", lw=1.3,
                label=f"Overall mean = {df['G3'].mean():.1f}")
    ax1.legend(fontsize=9)
    for i, (m, n) in enumerate(zip(means, counts), 1):
        ax1.text(i, -0.35, f"n={n}", ha="center",
                 fontsize=8, color="#555")
    sig_c = "#27AE60" if p_anova < ALPHA else "#E24B4A"
    ax1.text(0.98, 0.04,
             f"ANOVA  F = {f_stat:.2f}\np = {p_anova:.4f}",
             transform=ax1.transAxes, ha="right", fontsize=8.5,
             color=sig_c,
             bbox=dict(boxstyle="round,pad=0.35",
                       fc="white", ec="#BDD7EE", lw=0.8))

    # ── Panel C : Mean G3 bar chart ───────────────────────────
    ax2 = fig.add_subplot(gs[2])
    ax2.set_facecolor("#EDF3FB")

    x    = np.arange(4)
    # Filter out NaNs for the bars and calculation
    clean_means = [0 if np.isnan(m) else m for m in means]
    max_val = np.nanmax(clean_means) if len(clean_means) > 0 else 20
    
    bars = ax2.bar(x, clean_means, color=BLUES, edgecolor="white",
                    width=0.55, zorder=3)
    ax2.set_xticks(x)
    ax2.set_xticklabels([study_labels[i] for i in [1, 2, 3, 4]], fontsize=9)
    
    # FIX: Safety check for ylim to prevent ValueError
    ax2.set_ylim(0, (max_val * 1.25) if max_val > 0 else 20)
    
    ax2.set_xlabel("Study Time (hrs/week)")
    ax2.set_ylabel("Mean G3")
    ax2.set_title("Mean Grade per Study Group", fontweight="bold")
    
    for bar, m in zip(bars, clean_means):
        ax2.text(bar.get_x() + bar.get_width() / 2,
                  bar.get_height() + 0.18, f"{m:.1f}",
                  ha="center", va="bottom",
                  fontsize=10, fontweight="bold", color="#08306B")
    
    legend_els = [mpatches.Patch(fc=BLUES[i], label=study_labels[i+1])
                  for i in range(4)]
    ax2.legend(handles=legend_els, fontsize=8, loc="upper left")

    # ── Insight strip ─────────────────────────────────────────
    # Use clean_means to find best group to avoid argmax error on NaN
    best_idx = int(np.nanargmax(clean_means))
    best_grp = study_labels[best_idx + 1]
    highest_mean = clean_means[best_idx]
    
    insight  = (f"Students studying {best_grp} achieve the highest mean G3 = "
                f"{highest_mean:.1f}.  "
                f"Spearman ρ = {rho:.3f} confirms a "
                f"{'positive' if rho > 0 else 'negative'} relationship "
                f"({'significant' if p_spear < ALPHA else 'not significant'}).")
    
    fig.text(0.5, -0.05, f"Insight  ·  {insight}",
              ha="center", fontsize=9.5, style="italic", color="#08306B",
              bbox=dict(boxstyle="round,pad=0.45",
                        fc="#DDEEFF", ec="#BDD7EE", lw=0.8))

    save_chart(fig, "task2_studytime_vs_grades")
    plt.show()
# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("\n" + "="*55)
    print("  TASK 2  —  Loading data...")
    print("="*55)
    df = load_data()
    results = analyse(df)
    visualise(df, *results)
    print("\n  Task 2 complete.")
