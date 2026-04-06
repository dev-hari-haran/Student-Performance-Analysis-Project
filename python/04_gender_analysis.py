"""
Student Performance Analysis
Task 4  —  Gender-Based Performance Analysis
File    :  python/04_gender_analysis.py
Run     :  VS Code Run Button (top right)
Output  :  outputs/charts/task4_*.png  &  task4_*.pdf
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

# Task 4 color palette — Coral (Female) + Teal (Male)
C_FEMALE = "#E8735A"
C_MALE   = "#2196A6"
C_BOTH   = [C_FEMALE, C_MALE]
BG       = "#F7FAFA"

# ─────────────────────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────────────────────
def load_data():
    df = pd.read_csv(DATA_PATH, sep=None, engine="python")
    print(f"  Loaded : {df.shape[0]} rows x {df.shape[1]} cols")

    # Handle sex column whether encoded (0/1) or raw (F/M)
    if df["sex"].dtype in [np.int64, np.float64, int, float]:
        df["sex_label"] = df["sex"].map({0: "Female", 1: "Male"})
    else:
        df["sex_label"] = df["sex"].map({"F": "Female", "M": "Male"})

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
    female = df[df["sex_label"] == "Female"]["G3"].dropna()
    male   = df[df["sex_label"] == "Male"]["G3"].dropna()

    # Descriptive stats
    stats_df = df.groupby("sex_label")["G3"].agg(
        ["mean", "median", "std", "min", "max", "count"]
    ).rename(columns={
        "mean":"Mean", "median":"Median", "std":"Std Dev",
        "min":"Min", "max":"Max", "count":"n"
    })

    # H2: Independent t-test
    t_stat, p_t = stats.ttest_ind(female, male)

    # Mann-Whitney U (non-parametric alternative)
    u_stat, p_u = stats.mannwhitneyu(female, male, alternative="two-sided")

    # Cohen's d — effect size
    pooled_std = np.sqrt((female.std()**2 + male.std()**2) / 2)
    cohens_d   = (female.mean() - male.mean()) / pooled_std

    # Grade band distribution
    def grade_band(g):
        if g == 0:    return "Zero"
        elif g <= 9:  return "Fail (1–9)"
        elif g <= 13: return "Pass (10–13)"
        elif g <= 16: return "Good (14–16)"
        else:         return "Excellent (17–20)"

    df["grade_band"] = df["G3"].apply(grade_band)
    band_order = ["Zero", "Fail (1–9)", "Pass (10–13)",
                  "Good (14–16)", "Excellent (17–20)"]
    band_dist  = (df.groupby(["sex_label", "grade_band"])
                    .size()
                    .unstack(fill_value=0)
                    .reindex(columns=band_order, fill_value=0))

    # ── Console summary
    print("\n" + "="*55)
    print("  TASK 4 — Gender-Based Performance Analysis")
    print("="*55)
    print(f"\n{stats_df.round(2).to_string()}")
    print(f"\n  H2 Independent t-test:")
    print(f"    t = {t_stat:.3f},  p = {p_t:.4f}  "
          f"{'[Significant]' if p_t < ALPHA else '[Not significant]'}")
    print(f"  Mann-Whitney U = {u_stat:.0f},  p = {p_u:.4f}")
    print(f"  Cohen's d = {cohens_d:.3f}  "
          f"({'small' if abs(cohens_d)<0.5 else 'medium' if abs(cohens_d)<0.8 else 'large'} effect)")

    return (female, male, stats_df, t_stat, p_t,
            u_stat, p_u, cohens_d, band_dist, band_order)

# ─────────────────────────────────────────────────────────────
# VISUALISATION — 4 panels:
#   [Boxplot G1/G2/G3] [Mean bar G1/G2/G3]
#   [Grade band stacked bar] [KDE distribution]
# ─────────────────────────────────────────────────────────────
def visualise(df, female, male, stats_df, t_stat, p_t,
              u_stat, p_u, cohens_d, band_dist, band_order):

    fig = plt.figure(figsize=(18, 10), facecolor=BG)
    fig.suptitle(
        "Task 4  ·  Gender-Based Academic Performance Analysis",
        fontsize=15, fontweight="bold", color="#1A3A4A", y=1.01
    )
    gs = gridspec.GridSpec(2, 2, figure=fig,
                           hspace=0.46, wspace=0.38)

    # ── Panel A : Boxplot G1, G2, G3 by gender (top-left) ────
    ax0 = fig.add_subplot(gs[0, 0])
    ax0.set_facecolor("#F0F8FA")

    grade_cols = ["G1", "G2", "G3"]
    positions  = [1, 2, 4, 5, 7, 8]
    colors_seq = [C_FEMALE, C_MALE] * 3
    all_data   = []
    for g in grade_cols:
        all_data.append(df[df["sex_label"]=="Female"][g].dropna().values)
        all_data.append(df[df["sex_label"]=="Male"][g].dropna().values)

    bp = ax0.boxplot(
        all_data, positions=positions,
        patch_artist=True, widths=0.7,
        medianprops=dict(color="white", lw=2.2),
        whiskerprops=dict(color="#555"),
        capprops=dict(color="#555"),
        flierprops=dict(marker="o", mfc="#aaa", ms=3, ls="none")
    )
    for patch, c in zip(bp["boxes"], colors_seq):
        patch.set_facecolor(c); patch.set_alpha(0.85)

    ax0.set_xticks([1.5, 4.5, 7.5])
    ax0.set_xticklabels(["G1 (Period 1)", "G2 (Period 2)", "G3 (Final)"],
                        fontsize=10)
    ax0.set_ylim(-0.5, 21)
    ax0.set_ylabel("Grade")
    ax0.set_title("Grade Distribution by Gender (All Periods)",
                  fontweight="bold")
    legend_els = [mpatches.Patch(fc=C_FEMALE, label="Female"),
                  mpatches.Patch(fc=C_MALE,   label="Male")]
    ax0.legend(handles=legend_els, fontsize=9, loc="upper left")

    sig_c = "#27AE60" if p_t < ALPHA else "#E24B4A"
    ax0.text(0.98, 0.04,
             f"t-test  t={t_stat:.2f},  p={p_t:.4f}\n"
             f"Cohen's d = {cohens_d:.3f}",
             transform=ax0.transAxes, ha="right", fontsize=8.5,
             color=sig_c,
             bbox=dict(boxstyle="round,pad=0.4",
                       fc="white", ec="#B0D8E0", lw=0.8))

    # ── Panel B : Mean G1/G2/G3 grouped bar chart (top-right) ─
    ax1 = fig.add_subplot(gs[0, 1])
    ax1.set_facecolor("#F0F8FA")

    x     = np.arange(len(grade_cols))
    width = 0.32
    f_means = [df[df["sex_label"]=="Female"][g].mean() for g in grade_cols]
    m_means = [df[df["sex_label"]=="Male"][g].mean()   for g in grade_cols]

    b_f = ax1.bar(x - width/2, f_means, width, color=C_FEMALE,
                  edgecolor="white", label="Female", alpha=0.88)
    b_m = ax1.bar(x + width/2, m_means, width, color=C_MALE,
                  edgecolor="white", label="Male",   alpha=0.88)

    for bar, v in zip(list(b_f) + list(b_m),
                      f_means    + m_means):
        ax1.text(bar.get_x() + bar.get_width()/2,
                 bar.get_height() + 0.15, f"{v:.1f}",
                 ha="center", va="bottom",
                 fontsize=9, fontweight="bold",
                 color="#1A3A4A")

    ax1.set_xticks(x)
    ax1.set_xticklabels(["G1 (Period 1)", "G2 (Period 2)", "G3 (Final)"],
                        fontsize=10)
    ax1.set_ylim(0, max(f_means + m_means) * 1.22)
    ax1.set_ylabel("Mean Grade")
    ax1.set_title("Mean Grades by Gender Across All Periods",
                  fontweight="bold")
    ax1.legend(fontsize=9)

    # Difference annotation on G3
    diff = abs(f_means[2] - m_means[2])
    higher = "Female" if f_means[2] > m_means[2] else "Male"
    ax1.annotate(
        f"Δ G3 = {diff:.2f}\n({higher} higher)",
        xy=(2 + width/2, max(f_means[2], m_means[2])),
        xytext=(2.3, max(f_means[2], m_means[2]) + 0.6),
        fontsize=8.5, color="#1A3A4A",
        arrowprops=dict(arrowstyle="->", color="#555", lw=0.8)
    )

    # ── Panel C : Grade band stacked bar (bottom-left) ────────
    ax2 = fig.add_subplot(gs[1, 0])
    ax2.set_facecolor("#F0F8FA")

    band_colors = ["#D3D3D3", "#E07070", "#F0C070",
                   "#70B8D0", "#5CB85C"]
    bottom_f = np.zeros(1)
    bottom_m = np.zeros(1)
    bar_w    = 0.40

    for band, bc in zip(band_order, band_colors):
        fv = band_dist.loc["Female", band] if "Female" in band_dist.index else 0
        mv = band_dist.loc["Male",   band] if "Male"   in band_dist.index else 0
        ax2.bar([0], [fv], bottom=bottom_f, color=bc, edgecolor="white",
                width=bar_w, label=band)
        ax2.bar([0.5], [mv], bottom=bottom_m, color=bc, edgecolor="white",
                width=bar_w)
        bottom_f += fv
        bottom_m += mv

    ax2.set_xticks([0, 0.5])
    ax2.set_xticklabels(["Female", "Male"], fontsize=11)
    ax2.set_ylabel("Number of Students")
    ax2.set_title("Grade Band Distribution by Gender", fontweight="bold")
    ax2.legend(fontsize=8, loc="upper right",
               title="Grade Band", title_fontsize=8)

    # Count labels
    for xi, total in [(0, int(bottom_f[0])), (0.5, int(bottom_m[0]))]:
        ax2.text(xi, total + 1.5, f"n={total}",
                 ha="center", fontsize=9, fontweight="bold", color="#1A3A4A")

    # ── Panel D : KDE distribution of G3 (bottom-right) ──────
    ax3 = fig.add_subplot(gs[1, 1])
    ax3.set_facecolor("#F0F8FA")

    from scipy.stats import gaussian_kde
    for grp, c, lbl in [(female, C_FEMALE, "Female"),
                        (male,   C_MALE,   "Male")]:
        kde  = gaussian_kde(grp, bw_method=0.5)
        xs   = np.linspace(0, 20, 300)
        ys   = kde(xs)
        ax3.plot(xs, ys, color=c, lw=2.2, label=lbl)
        ax3.fill_between(xs, ys, alpha=0.18, color=c)
        ax3.axvline(grp.mean(), color=c, lw=1.4,
                    linestyle="--", alpha=0.8)
        ax3.text(grp.mean() + 0.2, max(ys) * 0.92,
                 f"μ={grp.mean():.1f}",
                 fontsize=8.5, color=c, fontweight="bold")

    ax3.set_xlabel("Final Grade (G3)")
    ax3.set_ylabel("Density")
    ax3.set_title("G3 Distribution Curve by Gender (KDE)",
                  fontweight="bold")
    ax3.set_xlim(0, 20)
    ax3.legend(fontsize=9)
    ax3.text(0.98, 0.04,
             f"Mann-Whitney U = {u_stat:.0f}\np = {p_u:.4f}",
             transform=ax3.transAxes, ha="right", fontsize=8.5,
             color="#1A3A4A",
             bbox=dict(boxstyle="round,pad=0.4",
                       fc="white", ec="#B0D8E0", lw=0.8))

    # ── Insight strip ─────────────────────────────────────────
    higher_g3 = "Female" if female.mean() > male.mean() else "Male"
    lower_g3  = "Male" if higher_g3 == "Female" else "Female"
    sig_str   = "a statistically significant" if p_t < ALPHA else "no statistically significant"
    insight   = (
        f"{higher_g3} students have a slightly higher mean G3 "
        f"({female.mean():.2f} vs {male.mean():.2f}).  "
        f"The t-test shows {sig_str} difference (p={p_t:.4f}).  "
        f"Cohen's d = {cohens_d:.3f} indicates a "
        f"{'small' if abs(cohens_d)<0.5 else 'medium'} effect size — "
        f"gender alone is not a strong predictor of performance."
    )
    fig.text(0.5, -0.04, f"Insight  ·  {insight}",
             ha="center", fontsize=9.5, style="italic", color="#1A3A4A",
             wrap=True,
             bbox=dict(boxstyle="round,pad=0.45",
                       fc="#E8F5F8", ec="#B0D8E0", lw=0.8))

    save_chart(fig, "task4_gender_analysis")
    plt.show()

# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("\n" + "="*55)
    print("  TASK 4  —  Loading data...")
    print("="*55)
    df      = load_data()
    results = analyse(df)
    visualise(df, *results)
    print("\n  Task 4 complete.")
