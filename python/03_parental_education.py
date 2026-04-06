"""
Student Performance Analysis
Task 3  —  Parental Education Impact
File    :  python/03_parental_education.py
Run     :  VS Code Run Button (top right)
Output  :  outputs/charts/task3_*.png  &  task3_*.pdf
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

# Task 3 color palettes — Greens (mother) + Purples (father)
GREENS  = ["#C7E9C0", "#74C476", "#31A354", "#006D2C", "#00441B"]
PURPLES = ["#DADAEB", "#9E9AC8", "#756BB1", "#54278F", "#3F007D"]
BG      = "#F7F5FC"

EDU_LABELS = {0: "None", 1: "Primary", 2: "Middle",
              3: "Secondary", 4: "Higher"}

# ─────────────────────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────────────────────
def load_data():
    df = pd.read_csv(DATA_PATH, sep=None, engine="python")
    print(f"  Loaded : {df.shape[0]} rows x {df.shape[1]} cols")
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
    medu_levels = sorted(df["Medu"].unique())
    fedu_levels = sorted(df["Fedu"].unique())

    medu_means = df.groupby("Medu")["G3"].mean()
    fedu_means = df.groupby("Fedu")["G3"].mean()
    medu_counts= df.groupby("Medu")["G3"].count()
    fedu_counts= df.groupby("Fedu")["G3"].count()

    medu_grps  = [df[df["Medu"] == l]["G3"].dropna() for l in medu_levels]
    fedu_grps  = [df[df["Fedu"] == l]["G3"].dropna() for l in fedu_levels]

    f_m, p_m   = stats.f_oneway(*[g for g in medu_grps if len(g) > 0])
    f_f, p_f   = stats.f_oneway(*[g for g in fedu_grps if len(g) > 0])

    rho_m, p_rho_m = stats.spearmanr(df["Medu"], df["G3"])
    rho_f, p_rho_f = stats.spearmanr(df["Fedu"], df["G3"])

    # ── Console summary
    print("\n" + "="*55)
    print("  TASK 3 — Parental Education Impact")
    print("="*55)

    print(f"\n  {'Medu Level':<14} {'Mean G3':>8} {'n':>6}")
    print(f"  {'-'*30}")
    for lvl in medu_levels:
        print(f"  {EDU_LABELS.get(lvl, lvl):<14} "
              f"{medu_means[lvl]:>8.2f} {medu_counts[lvl]:>6}")

    print(f"\n  ANOVA (Medu) F={f_m:.3f}, p={p_m:.4f}  "
          f"{'[Significant]' if p_m < ALPHA else '[Not significant]'}")
    print(f"  Spearman ρ   = {rho_m:.3f}, p={p_rho_m:.4f}")

    print(f"\n  {'Fedu Level':<14} {'Mean G3':>8} {'n':>6}")
    print(f"  {'-'*30}")
    for lvl in fedu_levels:
        print(f"  {EDU_LABELS.get(lvl, lvl):<14} "
              f"{fedu_means[lvl]:>8.2f} {fedu_counts[lvl]:>6}")

    print(f"\n  ANOVA (Fedu) F={f_f:.3f}, p={p_f:.4f}  "
          f"{'[Significant]' if p_f < ALPHA else '[Not significant]'}")
    print(f"  Spearman ρ   = {rho_f:.3f}, p={p_rho_f:.4f}")

    return (medu_levels, fedu_levels, medu_means, fedu_means,
            medu_counts, fedu_counts, medu_grps, fedu_grps,
            f_m, p_m, f_f, p_f, rho_m, p_rho_m, rho_f, p_rho_f)

# ─────────────────────────────────────────────────────────────
# VISUALISATION — 4 panels:
#   [Mother bar] [Father bar] [Mother box] [Father box]
# ─────────────────────────────────────────────────────────────
def visualise(df, medu_levels, fedu_levels, medu_means, fedu_means,
              medu_counts, fedu_counts, medu_grps, fedu_grps,
              f_m, p_m, f_f, p_f, rho_m, p_rho_m, rho_f, p_rho_f):

    fig = plt.figure(figsize=(18, 10), facecolor=BG)
    fig.suptitle(
        "Task 3  ·  Parental Education Impact on Student Grades",
        fontsize=15, fontweight="bold", color="#2D1B6B", y=1.01
    )
    gs = gridspec.GridSpec(2, 2, figure=fig,
                           hspace=0.46, wspace=0.38)

    # ── Helper: annotate bars
    def annotate_bars(ax, bars, vals, color):
        for bar, v in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + 0.12, f"{v:.1f}",
                    ha="center", va="bottom",
                    fontsize=10, fontweight="bold", color=color)

    # ── Helper: stat badge
    def stat_badge(ax, f, p, rho, bg_color, txt_color):
        sig = "Significant" if p < ALPHA else "Not significant"
        ax.text(0.98, 0.04,
                f"ANOVA  F={f:.2f},  p={p:.4f}\n"
                f"Spearman ρ = {rho:.3f}  [{sig}]",
                transform=ax.transAxes, ha="right", fontsize=8.5,
                color=txt_color,
                bbox=dict(boxstyle="round,pad=0.4",
                          fc="white", ec=bg_color, lw=0.9))

    # ── Panel A : Mother education bar chart (top-left) ───────
    ax0 = fig.add_subplot(gs[0, 0])
    ax0.set_facecolor("#EFF7EF")
    m_vals  = [medu_means[l] for l in medu_levels]
    m_cnts  = [medu_counts[l] for l in medu_levels]
    m_xlbls = [EDU_LABELS.get(l, str(l)) for l in medu_levels]
    g_colors= GREENS[:len(medu_levels)]
    x0 = np.arange(len(medu_levels))
    b0 = ax0.bar(x0, m_vals, color=g_colors, edgecolor="white",
                 width=0.55, zorder=3)
    ax0.set_xticks(x0)
    ax0.set_xticklabels(m_xlbls, fontsize=10)
    ax0.set_ylim(0, max(m_vals) * 1.26)
    ax0.set_xlabel("Mother's Education Level")
    ax0.set_ylabel("Mean Final Grade (G3)")
    ax0.set_title("Mother's Education vs Mean G3", fontweight="bold")
    annotate_bars(ax0, b0, m_vals, "#006D2C")
    for i, (bar, n) in enumerate(zip(b0, m_cnts)):
        ax0.text(bar.get_x() + bar.get_width() / 2,
                 0.25, f"n={n}", ha="center",
                 fontsize=8, color="white", fontweight="bold")
    stat_badge(ax0, f_m, p_m, rho_m, "#74C476", "#006D2C")

    # ── Panel B : Father education bar chart (top-right) ──────
    ax1 = fig.add_subplot(gs[0, 1])
    ax1.set_facecolor("#F3EFF9")
    f_vals  = [fedu_means[l] for l in fedu_levels]
    f_cnts  = [fedu_counts[l] for l in fedu_levels]
    f_xlbls = [EDU_LABELS.get(l, str(l)) for l in fedu_levels]
    p_colors= PURPLES[:len(fedu_levels)]
    x1 = np.arange(len(fedu_levels))
    b1 = ax1.bar(x1, f_vals, color=p_colors, edgecolor="white",
                 width=0.55, zorder=3)
    ax1.set_xticks(x1)
    ax1.set_xticklabels(f_xlbls, fontsize=10)
    ax1.set_ylim(0, max(f_vals) * 1.26)
    ax1.set_xlabel("Father's Education Level")
    ax1.set_ylabel("Mean Final Grade (G3)")
    ax1.set_title("Father's Education vs Mean G3", fontweight="bold")
    annotate_bars(ax1, b1, f_vals, "#54278F")
    for bar, n in zip(b1, f_cnts):
        ax1.text(bar.get_x() + bar.get_width() / 2,
                 0.25, f"n={n}", ha="center",
                 fontsize=8, color="white", fontweight="bold")
    stat_badge(ax1, f_f, p_f, rho_f, "#9E9AC8", "#54278F")

    # ── Panel C : Mother education boxplot (bottom-left) ──────
    ax2 = fig.add_subplot(gs[1, 0])
    ax2.set_facecolor("#EFF7EF")
    valid_m = [(l, g) for l, g in zip(medu_levels, medu_grps) if len(g) > 0]
    bp0 = ax2.boxplot(
        [g.values for _, g in valid_m],
        patch_artist=True, widths=0.48,
        medianprops=dict(color="white", lw=2.2),
        whiskerprops=dict(color="#444"),
        capprops=dict(color="#444"),
        flierprops=dict(marker="o", mfc="#888", ms=3, ls="none")
    )
    for patch, c in zip(bp0["boxes"], GREENS):
        patch.set_facecolor(c); patch.set_alpha(0.85)
    ax2.set_xticklabels([EDU_LABELS.get(l, l) for l, _ in valid_m], fontsize=9)
    ax2.set_ylim(-0.5, 21)
    ax2.set_xlabel("Mother's Education Level")
    ax2.set_ylabel("Final Grade (G3)")
    ax2.set_title("G3 Distribution by Mother's Education", fontweight="bold")
    ax2.axhline(df["G3"].mean(), color="#E24B4A", ls="--", lw=1.2,
                label=f"Overall mean = {df['G3'].mean():.1f}")
    ax2.legend(fontsize=9)

    # ── Panel D : Father education boxplot (bottom-right) ─────
    ax3 = fig.add_subplot(gs[1, 1])
    ax3.set_facecolor("#F3EFF9")
    valid_f = [(l, g) for l, g in zip(fedu_levels, fedu_grps) if len(g) > 0]
    bp1 = ax3.boxplot(
        [g.values for _, g in valid_f],
        patch_artist=True, widths=0.48,
        medianprops=dict(color="white", lw=2.2),
        whiskerprops=dict(color="#444"),
        capprops=dict(color="#444"),
        flierprops=dict(marker="o", mfc="#888", ms=3, ls="none")
    )
    for patch, c in zip(bp1["boxes"], PURPLES):
        patch.set_facecolor(c); patch.set_alpha(0.85)
    ax3.set_xticklabels([EDU_LABELS.get(l, l) for l, _ in valid_f], fontsize=9)
    ax3.set_ylim(-0.5, 21)
    ax3.set_xlabel("Father's Education Level")
    ax3.set_ylabel("Final Grade (G3)")
    ax3.set_title("G3 Distribution by Father's Education", fontweight="bold")
    ax3.axhline(df["G3"].mean(), color="#E24B4A", ls="--", lw=1.2,
                label=f"Overall mean = {df['G3'].mean():.1f}")
    ax3.legend(fontsize=9)

    # ── Insight strip ─────────────────────────────────────────
    best_m = EDU_LABELS.get(
        medu_levels[int(np.argmax(m_vals))], "Higher")
    best_f = EDU_LABELS.get(
        fedu_levels[int(np.argmax(f_vals))], "Higher")
    insight = (
        f"Students whose mothers have '{best_m}' education "
        f"achieve the highest mean G3 = {max(m_vals):.1f}.  "
        f"Father's '{best_f}' education similarly yields "
        f"mean G3 = {max(f_vals):.1f}.  "
        f"Both ANOVA results are "
        f"{'significant' if p_m < ALPHA and p_f < ALPHA else 'mixed'}, "
        f"confirming parental education impacts grades."
    )
    fig.text(0.5, -0.04, f"Insight  ·  {insight}",
             ha="center", fontsize=9.5, style="italic", color="#2D1B6B",
             wrap=True,
             bbox=dict(boxstyle="round,pad=0.45",
                       fc="#EDE8F8", ec="#9E9AC8", lw=0.8))

    save_chart(fig, "task3_parental_education_vs_grades")
    plt.show()

# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("\n" + "="*55)
    print("  TASK 3  —  Loading data...")
    print("="*55)
    df      = load_data()
    results = analyse(df)
    visualise(df, *results)
    print("\n  Task 3 complete.")
