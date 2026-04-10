# =============================================================================
# 07_hypothesis_testing.py
# Student Performance Analysis — Statistical Hypothesis Testing
# Tests:
#   H1 — Does study time significantly affect grades? (One-Way ANOVA + post-hoc)
#   H2 — Is there a significant grade difference between genders? (Independent t-test)
# Dataset: student-mat-clean.csv
# Output:  outputs/charts/07_hypothesis_testing/
# =============================================================================

import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy import stats
from itertools import combinations

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "student-mat-clean.csv")
OUT_DIR   = os.path.join(BASE_DIR, "outputs", "charts", "07_hypothesis_testing")
os.makedirs(OUT_DIR, exist_ok=True)

STUDYTIME_LABELS = {1: "<2 hrs", 2: "2–5 hrs", 3: "5–10 hrs", 4: ">10 hrs"}
ALPHA = 0.05

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def significance_stars(p):
    if p < 0.001: return "***"
    if p < 0.01:  return "**"
    if p < 0.05:  return "*"
    return "ns"

def print_section(title):
    print()
    print("=" * 60)
    print(title)
    print("=" * 60)

# ---------------------------------------------------------------------------
# Load
# ---------------------------------------------------------------------------
df = pd.read_csv(DATA_PATH)

print_section("HYPOTHESIS TESTING — Student Performance Analysis")
print(f"  Dataset : {DATA_PATH}")
print(f"  Records : {len(df)}")
print(f"  Alpha   : {ALPHA}")

# ============================================================
# H1 — Does Study Time Significantly Affect Grades? (ANOVA)
# ============================================================
print_section("H1: ANOVA — Study Time vs Final Grade (G3)")
print("  H₀: Mean G3 is equal across all study-time groups")
print("  H₁: At least one group mean is significantly different")

st_groups = {k: df.loc[df["studytime"] == k, "G3"].dropna().values
             for k in sorted(STUDYTIME_LABELS)}
group_list   = list(st_groups.values())
group_labels = [STUDYTIME_LABELS[k] for k in sorted(STUDYTIME_LABELS)]

f_stat, p_anova = stats.f_oneway(*group_list)
print(f"\n  One-Way ANOVA")
print(f"    F-statistic : {f_stat:.4f}")
print(f"    p-value     : {p_anova:.6f}  {significance_stars(p_anova)}")
decision_anova = "REJECT H₀" if p_anova < ALPHA else "FAIL TO REJECT H₀"
print(f"    Decision    : {decision_anova}")
if p_anova < ALPHA:
    print("    ✔ Study time has a statistically significant effect on G3.")
else:
    print("    ✘ No statistically significant difference found.")

# ---------------------------------------------------------------------------
# Levene's Test for Equal Variances
# ---------------------------------------------------------------------------
lev_stat, p_lev = stats.levene(*group_list)
print(f"\n  Levene's Test (equal variances)")
print(f"    W = {lev_stat:.4f},  p = {p_lev:.4f}")
print(f"    Variances {'are NOT' if p_lev < ALPHA else 'are'} equal across groups")

# ---------------------------------------------------------------------------
# Post-hoc — Pairwise t-tests (Bonferroni correction)
# ---------------------------------------------------------------------------
keys = sorted(st_groups)
pairs = list(combinations(keys, 2))
bonf_alpha = ALPHA / len(pairs)
print(f"\n  Post-hoc Pairwise t-tests (Bonferroni α = {bonf_alpha:.4f})")
print(f"  {'Group A':<12} {'Group B':<12} {'t':>8} {'p':>10} {'Sig':>6}")
print("  " + "-" * 52)
posthoc_results = []
for k1, k2 in pairs:
    t, p = stats.ttest_ind(st_groups[k1], st_groups[k2], equal_var=False)
    sig = "✔" if p < bonf_alpha else "–"
    print(f"  {STUDYTIME_LABELS[k1]:<12} {STUDYTIME_LABELS[k2]:<12} "
          f"{t:>8.3f} {p:>10.4f} {sig:>6}")
    posthoc_results.append((STUDYTIME_LABELS[k1], STUDYTIME_LABELS[k2], t, p, sig))

# ---------------------------------------------------------------------------
# Chart H1-A — Box Plot with ANOVA result annotation
# ---------------------------------------------------------------------------
fig1, ax1 = plt.subplots(figsize=(9, 5))
bp = ax1.boxplot(group_list, labels=group_labels, patch_artist=True,
                 medianprops=dict(color="black", linewidth=2),
                 notch=False)
palette = ["#4C72B0", "#55A868", "#C44E52", "#8172B2"]
for patch, color in zip(bp["boxes"], palette):
    patch.set_facecolor(color)
    patch.set_alpha(0.72)
ax1.set_title("G3 Distribution by Study Time\n"
              f"One-Way ANOVA: F={f_stat:.2f}, p={p_anova:.4f}  {significance_stars(p_anova)}",
              fontsize=13, fontweight="bold")
ax1.set_xlabel("Study Time per Week")
ax1.set_ylabel("Final Grade G3 (0–20)")
ax1.axhline(df["G3"].mean(), color="grey", linestyle="--", linewidth=1,
            label=f"Overall Mean: {df['G3'].mean():.2f}")
ax1.legend(fontsize=9)
# Annotate significance stars between pairs
y_max = df["G3"].max() + 1
for idx, (lbl_a, lbl_b, t_val, p_val, sig) in enumerate(posthoc_results):
    if sig == "✔":
        xa = group_labels.index(lbl_a) + 1
        xb = group_labels.index(lbl_b) + 1
        y  = y_max + idx * 0.8
        ax1.plot([xa, xb], [y, y], color="black", linewidth=0.8)
        ax1.text((xa + xb) / 2, y + 0.1, "✔", ha="center", va="bottom", fontsize=8)
plt.tight_layout()
for ext in ("png", "pdf"):
    fig1.savefig(os.path.join(OUT_DIR, f"h1_anova_studytime_boxplot.{ext}"),
                 dpi=150, bbox_inches="tight")
plt.close(fig1)
print("\n  ✔ Saved: h1_anova_studytime_boxplot.png / .pdf")

# ---------------------------------------------------------------------------
# Chart H1-B — Mean G3 per group with 95% CI error bars
# ---------------------------------------------------------------------------
means_st = [g.mean() for g in group_list]
cis_st   = [stats.sem(g) * stats.t.ppf(0.975, len(g) - 1) for g in group_list]

fig2, ax2 = plt.subplots(figsize=(8, 5))
x_pos = np.arange(len(group_labels))
ax2.bar(x_pos, means_st, color=palette, edgecolor="white", width=0.55, alpha=0.85)
ax2.errorbar(x_pos, means_st, yerr=cis_st, fmt="none",
             color="black", capsize=6, linewidth=1.5)
ax2.bar_label(ax2.containers[0], fmt="%.2f", padding=6, fontsize=9, fontweight="bold")
ax2.set_xticks(x_pos)
ax2.set_xticklabels(group_labels)
ax2.set_title("Mean G3 by Study Time (95% CI Error Bars)", fontsize=13, fontweight="bold")
ax2.set_ylabel("Mean G3 (0–20)")
ax2.set_ylim(0, 22)
ax2.text(0.98, 0.97,
         f"ANOVA: F={f_stat:.2f}, p={p_anova:.4f} {significance_stars(p_anova)}",
         transform=ax2.transAxes, ha="right", va="top", fontsize=9,
         bbox=dict(boxstyle="round,pad=0.3", facecolor="lightyellow", alpha=0.8))
plt.tight_layout()
for ext in ("png", "pdf"):
    fig2.savefig(os.path.join(OUT_DIR, f"h1_mean_g3_ci_bars.{ext}"),
                 dpi=150, bbox_inches="tight")
plt.close(fig2)
print("  ✔ Saved: h1_mean_g3_ci_bars.png / .pdf")

# ============================================================
# H2 — Gender Difference in Grades (Independent t-test)
# ============================================================
print_section("H2: t-test — Gender vs Final Grade (G3)")
print("  H₀: Mean G3 is equal for Male and Female students")
print("  H₁: There is a significant difference in mean G3 by gender")

if "sex" in df.columns:
    male   = df.loc[df["sex"] == "M", "G3"].dropna().values
    female = df.loc[df["sex"] == "F", "G3"].dropna().values
elif "gender" in df.columns:
    unique_vals = df["gender"].dropna().unique()
    male_val   = next((v for v in unique_vals if str(v).upper() in ("M", "MALE")), None)
    female_val = next((v for v in unique_vals if str(v).upper() in ("F", "FEMALE")), None)
    male   = df.loc[df["gender"] == male_val, "G3"].dropna().values if male_val else np.array([])
    female = df.loc[df["gender"] == female_val, "G3"].dropna().values if female_val else np.array([])
else:
    print("  ⚠ No 'sex' or 'gender' column found. Skipping H2.")
    male = female = np.array([])

if len(male) > 0 and len(female) > 0:
    # Levene
    lev_g_stat, p_lev_g = stats.levene(male, female)
    equal_var = p_lev_g >= ALPHA

    # t-test
    t_stat, p_ttest = stats.ttest_ind(male, female, equal_var=equal_var)
    cohen_d = (male.mean() - female.mean()) / np.sqrt(
        ((len(male) - 1) * male.std()**2 + (len(female) - 1) * female.std()**2)
        / (len(male) + len(female) - 2)
    )

    print(f"\n  Group Sizes : Male = {len(male)},  Female = {len(female)}")
    print(f"  Mean G3     : Male = {male.mean():.3f},  Female = {female.mean():.3f}")
    print(f"  Std G3      : Male = {male.std():.3f},   Female = {female.std():.3f}")
    print(f"\n  Levene's Test : W = {lev_g_stat:.4f},  p = {p_lev_g:.4f}")
    print(f"  t-test variant: {'Welch' if not equal_var else 'Student'}")
    print(f"\n  Independent t-test")
    print(f"    t-statistic : {t_stat:.4f}")
    print(f"    p-value     : {p_ttest:.6f}  {significance_stars(p_ttest)}")
    print(f"    Cohen's d   : {cohen_d:.4f}  "
          f"({'small' if abs(cohen_d) < 0.5 else 'medium' if abs(cohen_d) < 0.8 else 'large'} effect)")
    decision_t = "REJECT H₀" if p_ttest < ALPHA else "FAIL TO REJECT H₀"
    print(f"    Decision    : {decision_t}")
    if p_ttest < ALPHA:
        higher = "Male" if male.mean() > female.mean() else "Female"
        print(f"    ✔ Significant gender difference: {higher} students score higher on average.")
    else:
        print("    ✘ No statistically significant gender difference in G3.")

    # -----------------------------------------------------------------------
    # Chart H2-A — Box Plot: Male vs Female G3
    # -----------------------------------------------------------------------
    fig3, ax3 = plt.subplots(figsize=(7, 5))
    bp2 = ax3.boxplot([male, female], labels=["Male", "Female"], patch_artist=True,
                      medianprops=dict(color="black", linewidth=2))
    gender_colors = ["#4C72B0", "#C44E52"]
    for patch, c in zip(bp2["boxes"], gender_colors):
        patch.set_facecolor(c)
        patch.set_alpha(0.75)
    # Significance bracket
    y_top = max(male.max(), female.max()) + 1.5
    ax3.plot([1, 2], [y_top, y_top], color="black", linewidth=1)
    ax3.text(1.5, y_top + 0.2, significance_stars(p_ttest), ha="center",
             va="bottom", fontsize=13, fontweight="bold")
    ax3.set_title(f"G3 Distribution by Gender\n"
                  f"t = {t_stat:.3f},  p = {p_ttest:.4f}  {significance_stars(p_ttest)}",
                  fontsize=13, fontweight="bold")
    ax3.set_ylabel("Final Grade G3 (0–20)")
    legend_patches = [
        mpatches.Patch(color=gender_colors[0], alpha=0.75, label=f"Male   (n={len(male)}, μ={male.mean():.2f})"),
        mpatches.Patch(color=gender_colors[1], alpha=0.75, label=f"Female (n={len(female)}, μ={female.mean():.2f})"),
    ]
    ax3.legend(handles=legend_patches, fontsize=9)
    plt.tight_layout()
    for ext in ("png", "pdf"):
        fig3.savefig(os.path.join(OUT_DIR, f"h2_ttest_gender_boxplot.{ext}"),
                     dpi=150, bbox_inches="tight")
    plt.close(fig3)
    print("\n  ✔ Saved: h2_ttest_gender_boxplot.png / .pdf")

    # -----------------------------------------------------------------------
    # Chart H2-B — Violin Plot: Male vs Female G3
    # -----------------------------------------------------------------------
    fig4, ax4 = plt.subplots(figsize=(7, 5))
    vp = ax4.violinplot([male, female], positions=[1, 2], showmedians=True, showmeans=False)
    for body, c in zip(vp["bodies"], gender_colors):
        body.set_facecolor(c)
        body.set_alpha(0.65)
    vp["cmedians"].set_color("black")
    vp["cmedians"].set_linewidth(2)
    ax4.set_xticks([1, 2])
    ax4.set_xticklabels(["Male", "Female"])
    ax4.set_title("G3 Distribution by Gender (Violin Plot)", fontsize=13, fontweight="bold")
    ax4.set_ylabel("Final Grade G3 (0–20)")
    ax4.text(0.98, 0.97,
             f"Cohen's d = {cohen_d:.3f}\n"
             f"p = {p_ttest:.4f} {significance_stars(p_ttest)}",
             transform=ax4.transAxes, ha="right", va="top", fontsize=9,
             bbox=dict(boxstyle="round,pad=0.3", facecolor="lightyellow", alpha=0.8))
    plt.tight_layout()
    for ext in ("png", "pdf"):
        fig4.savefig(os.path.join(OUT_DIR, f"h2_gender_violin.{ext}"),
                     dpi=150, bbox_inches="tight")
    plt.close(fig4)
    print("  ✔ Saved: h2_gender_violin.png / .pdf")

    # -----------------------------------------------------------------------
    # Chart H2-C — Grade progression G1, G2, G3 by Gender
    # -----------------------------------------------------------------------
    grade_cols = [c for c in ["G1", "G2", "G3"] if c in df.columns]
    if len(grade_cols) == 3:
        m_means = [df.loc[df.get("sex", df.get("gender")) == ("M" if "sex" in df.columns else male_val), c].mean()
                   for c in grade_cols]
        f_means = [df.loc[df.get("sex", df.get("gender")) == ("F" if "sex" in df.columns else female_val), c].mean()
                   for c in grade_cols]
        fig5, ax5 = plt.subplots(figsize=(8, 5))
        ax5.plot(grade_cols, m_means, "o-", color="#4C72B0", linewidth=2.2,
                 markersize=8, label=f"Male (n={len(male)})")
        ax5.plot(grade_cols, f_means, "s-", color="#C44E52", linewidth=2.2,
                 markersize=8, label=f"Female (n={len(female)})")
        for grades, means in [(grade_cols, m_means), (grade_cols, f_means)]:
            for g, m in zip(grades, means):
                ax5.annotate(f"{m:.2f}", (g, m), textcoords="offset points",
                             xytext=(0, 8), ha="center", fontsize=9)
        ax5.set_title("Grade Progression G1 → G2 → G3 by Gender", fontsize=13, fontweight="bold")
        ax5.set_ylabel("Mean Grade (0–20)")
        ax5.set_xlabel("Grade Period")
        ax5.legend()
        ax5.set_ylim(0, 22)
        plt.tight_layout()
        for ext in ("png", "pdf"):
            fig5.savefig(os.path.join(OUT_DIR, f"h2_grade_progression_gender.{ext}"),
                         dpi=150, bbox_inches="tight")
        plt.close(fig5)
        print("  ✔ Saved: h2_grade_progression_gender.png / .pdf")

# ---------------------------------------------------------------------------
# Final Summary
# ---------------------------------------------------------------------------
print_section("FINAL STATISTICAL SUMMARY")
print(f"  H1 (ANOVA  — Study Time → G3)")
print(f"     F = {f_stat:.3f},  p = {p_anova:.4f}  {significance_stars(p_anova)}")
print(f"     → {decision_anova}")
if len(male) > 0 and len(female) > 0:
    print(f"\n  H2 (t-test — Gender    → G3)")
    print(f"     t = {t_stat:.3f},  p = {p_ttest:.4f}  {significance_stars(p_ttest)}")
    print(f"     Cohen's d = {cohen_d:.3f}")
    print(f"     → {decision_t}")
print(f"\n  Significance levels: * p<.05  ** p<.01  *** p<.001  ns = not significant")
print(f"\n  All charts saved to: {OUT_DIR}")
print("=" * 60)
