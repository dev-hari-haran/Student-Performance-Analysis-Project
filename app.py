# =============================================================================
# app.py  —  Student Performance Analysis Dashboard
# Run with:  streamlit run app.py
# Charts    : outputs/charts/*.png  (flat folder)
# =============================================================================

import streamlit as st
import os
from PIL import Image

# ---------------------------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Student Performance Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# CHART ROOT  —  flat folder: outputs/charts/
# ---------------------------------------------------------------------------
BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
CHART_DIR = os.path.join(BASE_DIR, "outputs", "charts")

def img(filename):
    path = os.path.join(CHART_DIR, filename)
    if os.path.exists(path):
        return Image.open(path)
    return None

def show_img(filename, caption=""):
    image = img(filename)
    if image:
        st.image(image, caption=caption, use_column_width=True)
    else:
        st.warning(f"⚠ Chart not found: `{filename}` — run the analysis script first.")

# ---------------------------------------------------------------------------
# GLOBAL CSS
# ---------------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@400;500;600&display=swap');

:root {
    --bg:      #0d1117;
    --surface: #161b22;
    --card:    #1c2433;
    --border:  #30363d;
    --gold:    #f7c948;
    --teal:    #4dd9ac;
    --pink:    #e05c97;
    --blue:    #6ea8fe;
    --text:    #e6edf3;
    --muted:   #8b949e;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(160deg, #0d1117 0%, #1a1f2e 100%) !important;
    border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] * { color: var(--text) !important; }

h1, h2, h3 { font-family: 'Syne', sans-serif !important; }
h1 { font-size: 2.3rem !important; }
h2 { font-size: 1.55rem !important; }
h3 { font-size: 1.1rem !important; color: var(--teal) !important; }

[data-testid="metric-container"] {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 16px 20px !important;
}
[data-testid="metric-container"] label {
    color: var(--muted) !important;
    font-size: 0.76rem !important;
    letter-spacing: .06em !important;
    text-transform: uppercase !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: var(--gold) !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 2rem !important;
}

[data-baseweb="tab-list"] {
    background: var(--surface) !important;
    border-radius: 12px !important;
    padding: 4px !important;
    gap: 6px !important;
    border: 1px solid var(--border) !important;
}
[data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 8px !important;
    color: var(--muted) !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    padding: 8px 14px !important;
    border: none !important;
}
[aria-selected="true"][data-baseweb="tab"] {
    background: linear-gradient(135deg, #f7c948 0%, #e05c97 100%) !important;
    color: #0d1117 !important;
}

img { border-radius: 10px !important; }
hr  { border-color: var(--border) !important; }

.pill {
    display:inline-block; padding:3px 12px; border-radius:20px;
    font-size:0.72rem; font-weight:700; letter-spacing:.08em;
    text-transform:uppercase; font-family:'Syne',sans-serif;
    background:linear-gradient(135deg,#f7c948,#e05c97);
    color:#0d1117; margin-bottom:10px;
}

.insight {
    background: var(--card);
    border-left: 4px solid var(--teal);
    border-radius: 8px;
    padding: 14px 18px;
    margin: 12px 0;
    font-size: 0.9rem;
    line-height: 1.65;
}
.insight.gold { border-left-color: var(--gold); }
.insight.pink { border-left-color: var(--pink); }
.insight.blue { border-left-color: var(--blue); }

.rcard {
    border-radius: 12px;
    padding: 18px;
    margin-bottom: 14px;
    font-size: 0.85rem;
    line-height: 1.65;
    color: var(--muted);
}
.rcard .rtitle {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 0.95rem;
    margin: 8px 0 6px;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:10px 0 20px;'>
        <div style='font-size:2.8rem;'>🎓</div>
        <div style='font-family:Syne,sans-serif;font-size:1.05rem;
                    font-weight:800;color:#f7c948;line-height:1.35;margin-top:6px;'>
            Student Performance<br>Analysis
        </div>
        <div style='color:#8b949e;font-size:0.73rem;margin-top:5px;'>
            Dataset: student-mat-clean.csv
        </div>
    </div><hr>
    """, unsafe_allow_html=True)

    page = st.radio("", [
        "🏠  Overview",
        "🔹  01 · Preprocessing",
        "🔹  02 · Study Time",
        "🔹  03 · Parental Education",
        "🔹  04 · Gender Analysis",
        "🔹  05 · Correlation",
        "🔹  06 · Lifestyle",
        "🔹  07 · Hypothesis Testing",
        "💡  Showcase Questions",
    ], label_visibility="collapsed")

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("""
    <div style='color:#8b949e;font-size:0.73rem;line-height:1.9;'>
        <b style='color:#e6edf3;'>Charts</b> → outputs/charts/*.png<br>
        <b style='color:#e6edf3;'>Modules</b><br>
        01 Preprocessing · 02 Study Time<br>
        03 Parental Edu · 04 Gender<br>
        05 Correlation · 06 Lifestyle<br>
        07 Hypothesis Testing
    </div>
    """, unsafe_allow_html=True)

# ===========================================================================
# PAGE 0 — OVERVIEW
# ===========================================================================
if page == "🏠  Overview":
    st.markdown("<div class='pill'>Dashboard</div>", unsafe_allow_html=True)
    st.markdown("# Student Performance\n## <span style='color:#4dd9ac;'>Analysis Dashboard</span>",
                unsafe_allow_html=True)
    st.markdown("<p style='color:#8b949e;'>Exploring academic outcomes through data-driven insights.</p>",
                unsafe_allow_html=True)
    st.divider()

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("📊 Modules", "7")
    k2.metric("📈 Charts", "14+")
    k3.metric("💡 Showcase Qs", "4")
    k4.metric("📁 Dataset", "Math CSV")

    st.divider()
    st.markdown("### 📦 Analysis Modules")
    modules = [
        ("01", "Preprocessing",     "#f7c948", "Grade distributions, null checks & data types."),
        ("02", "Study Time",         "#4dd9ac", "Weekly study hours vs final grade G3."),
        ("03", "Parental Education", "#6ea8fe", "Parent edu level correlation with grades."),
        ("04", "Gender Analysis",    "#e05c97", "Grade differences & progression by gender."),
        ("05", "Correlation",        "#f7c948", "Heatmap & pairplot of key variables."),
        ("06", "Lifestyle",          "#4dd9ac", "Alcohol & social activity vs performance."),
        ("07", "Hypothesis Testing", "#e05c97", "ANOVA & t-test statistical validation."),
    ]
    for i in range(0, len(modules), 4):
        cols = st.columns(4)
        for col, (num, title, color, desc) in zip(cols, modules[i:i+4]):
            col.markdown(f"""
            <div style='background:#1c2433;border:1px solid #30363d;
                        border-top:3px solid {color};border-radius:12px;
                        padding:16px;min-height:130px;'>
                <div style='font-family:Syne,sans-serif;font-size:0.68rem;
                            color:{color};font-weight:800;letter-spacing:.1em;'>MODULE {num}</div>
                <div style='font-weight:700;font-size:0.98rem;margin:6px 0 8px;'>{title}</div>
                <div style='color:#8b949e;font-size:0.81rem;line-height:1.5;'>{desc}</div>
            </div>""", unsafe_allow_html=True)

    st.divider()
    st.markdown("### 💡 Showcase Questions")
    qs = [
        ("🧑‍👩‍👧", "#6ea8fe", "Parental Support",    "For low parental education"),
        ("📉",       "#e05c97", "Academic Intervention","For poor grade trends"),
        ("🍺",       "#f7c948", "Lifestyle Awareness",  "Alcohol & social impact"),
        ("📚",       "#4dd9ac", "Study Strategies",     "Improve study habits"),
    ]
    for col, (icon, color, title, sub) in zip(st.columns(4), qs):
        col.markdown(f"""
        <div style='background:linear-gradient(135deg,{color}18,{color}06);
                    border:1px solid {color}55;border-radius:12px;
                    padding:18px;text-align:center;'>
            <div style='font-size:2rem;'>{icon}</div>
            <div style='font-family:Syne,sans-serif;font-weight:700;
                        color:{color};margin:8px 0 4px;font-size:0.9rem;'>{title}</div>
            <div style='color:#8b949e;font-size:0.76rem;'>{sub}</div>
        </div>""", unsafe_allow_html=True)

# ===========================================================================
# PAGE 1 — PREPROCESSING
# ===========================================================================
elif page == "🔹  01 · Preprocessing":
    st.markdown("<div class='pill'>Module 01</div>", unsafe_allow_html=True)
    st.markdown("## 🧹 Data Preprocessing & Overview")
    st.divider()
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### 📊 Grade Distributions")
        show_img("grade_distribution.png", "Histograms: G1, G2, G3")
    with c2:
        st.markdown("### 🗂 Categorical Columns")
        show_img("categorical_distributions.png", "Value counts of categorical features")
    st.markdown("""
    <div class='insight gold'>
        <b>🔍 Observations</b><br>
        • G3 is the primary prediction target across all modules.<br>
        • G1 and G2 are strong early-period leading indicators.<br>
        • Grade distributions are roughly normal, centred around 10–12.
    </div>""", unsafe_allow_html=True)

# ===========================================================================
# PAGE 2 — STUDY TIME
# ===========================================================================
elif page == "🔹  02 · Study Time":
    st.markdown("<div class='pill'>Module 02</div>", unsafe_allow_html=True)
    st.markdown("## 📖 Study Time vs Final Grade (G3)")
    st.divider()
    show_img("task2_studytime_vs_grades.png", "Full study-time analysis")
    st.markdown("""
    <div class='insight'>
        <b>📌 Insight</b><br>
        Students studying 5+ hours per week consistently achieve higher G3 scores.
        The regression line confirms a statistically meaningful positive trend.
    </div>""", unsafe_allow_html=True)

# ===========================================================================
# PAGE 3 — PARENTAL EDUCATION
# ===========================================================================
elif page == "🔹  03 · Parental Education":
    st.markdown("<div class='pill'>Module 03</div>", unsafe_allow_html=True)
    st.markdown("## 👨‍👩‍🎓 Parental Education Impact on Grades")
    st.divider()
    show_img("task3_parental_education_vs_grades.png", "Parental education vs grade analysis")
    st.markdown("""
    <div class='insight blue'>
        <b>📌 Insight</b><br>
        Students with higher-educated parents score notably better in G3.
        Both Medu (mother) and Fedu (father) show a positive gradient with final grades.
    </div>""", unsafe_allow_html=True)

# ===========================================================================
# PAGE 4 — GENDER ANALYSIS
# ===========================================================================
elif page == "🔹  04 · Gender Analysis":
    st.markdown("<div class='pill'>Module 04</div>", unsafe_allow_html=True)
    st.markdown("## ⚥ Gender-Based Performance Analysis")
    st.divider()
    show_img("task4_gender_analysis.png", "Gender analysis — box, violin & progression")
    st.markdown("""
    <div class='insight pink'>
        <b>📌 Insight</b><br>
        Grade progression G1 → G2 → G3 visualised per gender.
        The t-test determines whether observed differences are statistically significant.
    </div>""", unsafe_allow_html=True)

# ===========================================================================
# PAGE 5 — CORRELATION
# ===========================================================================
elif page == "🔹  05 · Correlation":
    st.markdown("<div class='pill'>Module 05</div>", unsafe_allow_html=True)
    st.markdown("## 🔗 Correlation Analysis")
    st.caption("Variables: `studytime · failures · absences · G1 · G2 · G3`")
    st.divider()

    st.markdown("### 🌡 Pearson Correlation Heatmap")
    show_img("correlation_heatmap.png", "Heatmap of all key variables")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### 📉 Strongest G3 Predictors")
        show_img("g3_correlations_bar.png", "Bar chart: correlation with G3")
    with c2:
        st.markdown("### 🔵 Pairplot")
        show_img("pairplot.png", "Scatter grid + diagonal histograms")

    st.markdown("""
    <div class='insight'>
        <b>📌 Key Findings</b><br>
        • <b>G2 & G1</b> are the strongest predictors of G3 (r &gt; 0.85).<br>
        • <b>Failures</b> shows the strongest negative correlation.<br>
        • <b>Absences</b> has a moderate negative effect on G3.<br>
        • <b>Study time</b> has a positive, moderate correlation.
    </div>""", unsafe_allow_html=True)

# ===========================================================================
# PAGE 6 — LIFESTYLE
# ===========================================================================
elif page == "🔹  06 · Lifestyle":
    st.markdown("<div class='pill'>Module 06</div>", unsafe_allow_html=True)
    st.markdown("## 🍺 Lifestyle Impact on Academic Performance")
    st.divider()

    st.markdown("### 🍷 Alcohol Consumption vs Grades")
    c1, c2, c3 = st.columns(3)
    with c1: show_img("alcohol_vs_g3_bar.png",  "Bar: Alcohol vs Mean G3")
    with c2: show_img("alcohol_boxplot_g3.png", "Box: G3 by Alcohol Group")
    with c3: show_img("scatter_alcohol_g3.png", "Scatter + Regression")

    st.markdown("### 🎉 Social Activity + Combined Heatmap")
    c4, c5 = st.columns(2)
    with c4: show_img("goout_vs_g3_bar.png",       "Goout Frequency vs Mean G3")
    with c5: show_img("heatmap_goout_walc_g3.png", "Heatmap: Goout × Walc → G3")

    st.markdown("### 📉 Social Scatter")
    show_img("scatter_goout_g3.png", "Scatter: Goout vs G3 with regression")

    st.markdown("""
    <div class='insight gold'>
        <b>📌 Lifestyle Insights</b><br>
        • Higher alcohol (Walc) negatively correlates with G3.<br>
        • Students who go out very often show lower average grades.<br>
        • The combined heatmap: high Walc + high Goout = worst performing segment.
    </div>""", unsafe_allow_html=True)

# ===========================================================================
# PAGE 7 — HYPOTHESIS TESTING
# ===========================================================================
elif page == "🔹  07 · Hypothesis Testing":
    st.markdown("<div class='pill'>Module 07</div>", unsafe_allow_html=True)
    st.markdown("## 🧪 Statistical Hypothesis Testing")
    st.divider()

    st.markdown("### H₁ · ANOVA — Does Study Time Significantly Affect Grades?")
    h1, h2 = st.columns(2)
    with h1: show_img("h1_anova_studytime_boxplot.png", "ANOVA — Study Time Box Plot")
    with h2: show_img("h1_mean_g3_ci_bars.png",         "Mean G3 with 95% CI Error Bars")

    st.markdown("""
    <div class='insight'>
        <b>H₁ Result</b> — One-Way ANOVA<br>
        Tests whether mean G3 differs across study-time groups.
        Bonferroni post-hoc pairwise t-tests identify which specific groups differ.
    </div>""", unsafe_allow_html=True)

    st.divider()
    st.markdown("### H₂ · t-test — Is There a Significant Gender Difference in G3?")
    show_img("task4_gender_analysis.png", "Gender: box plot, violin & grade progression")

    st.markdown("""
    <div class='insight pink'>
        <b>H₂ Result</b> — Independent t-test (Welch)<br>
        • Cohen's d measures practical effect size.<br>
        • G1→G2→G3 progression shows trends over time by gender.<br>
        <span style='color:#8b949e;'>Significance notation: * p&lt;.05 &nbsp;** p&lt;.01 &nbsp;*** p&lt;.001</span>
    </div>""", unsafe_allow_html=True)

# ===========================================================================
# PAGE 8 — SHOWCASE QUESTIONS
# ===========================================================================
elif page == "💡  Showcase Questions":
    st.markdown("<div class='pill'>Showcase</div>", unsafe_allow_html=True)
    st.markdown("# 💡 Policy Insights &\n## <span style='color:#4dd9ac;'>Recommendations</span>",
                unsafe_allow_html=True)
    st.markdown("<p style='color:#8b949e;'>Data-backed answers to four critical student support questions.</p>",
                unsafe_allow_html=True)
    st.divider()

    tab1, tab2, tab3, tab4 = st.tabs([
        "🧑‍👩‍👧  Parental Education",
        "📉  Academic Intervention",
        "🍺  Lifestyle Awareness",
        "📚  Study Habit Strategies",
    ])

    # ── TAB 1 ──────────────────────────────────────────────────────────────
    with tab1:
        st.markdown("## 🧑‍👩‍👧 Support Systems for Students with\n### <span style='color:#6ea8fe;'>Low Parental Education</span>",
                    unsafe_allow_html=True)
        st.divider()
        st.markdown("#### 📊 Evidence")
        show_img("task3_parental_education_vs_grades.png", "Mean G3 by Parent Education Level")
        c1, c2 = st.columns(2)
        with c1: show_img("correlation_heatmap.png",  "Correlation Heatmap")
        with c2: show_img("g3_correlations_bar.png",  "G3 Predictors")

        st.divider()
        st.markdown("#### 💡 Recommendations")
        r1, r2, r3 = st.columns(3)
        for col, icon, color, title, body in [
            (r1, "🏫", "#6ea8fe", "Mentorship Programs",
             "Pair students from low-education households with academic mentors to bridge knowledge gaps at home."),
            (r2, "📞", "#4dd9ac", "Parent Engagement",
             "Host workshops helping parents understand grading systems and creating productive home study environments."),
            (r3, "📚", "#f7c948", "Resource Access",
             "Provide free tutoring, study materials, and after-school programs for students lacking home academic support."),
        ]:
            col.markdown(f"""
            <div style='background:{color}18;border:1px solid {color}55;
                        border-radius:12px;padding:18px;'>
                <div style='font-size:1.7rem;'>{icon}</div>
                <div class='rtitle' style='color:{color};'>{title}</div>
                {body}
            </div>""", unsafe_allow_html=True)

        st.markdown("""
        <div class='insight blue' style='margin-top:18px;'>
            <b>📌 Conclusion</b><br>
            Students with no-education parents score <b>2–4 points lower</b> in G3
            on average. Early identification enables targeted, proactive support.
        </div>""", unsafe_allow_html=True)

    # ── TAB 2 ──────────────────────────────────────────────────────────────
    with tab2:
        st.markdown("## 📉 Interventions for Students with\n### <span style='color:#e05c97;'>Poor Academic Trends</span>",
                    unsafe_allow_html=True)
        st.divider()
        st.markdown("#### 📊 Evidence")
        c1, c2 = st.columns(2)
        with c1: show_img("task4_gender_analysis.png",       "G1 → G2 → G3 Trend")
        with c2: show_img("g3_correlations_bar.png",         "Variables Correlated with G3")
        c3, c4 = st.columns(2)
        with c3: show_img("h1_anova_studytime_boxplot.png",  "ANOVA Study Time Groups")
        with c4: show_img("h1_mean_g3_ci_bars.png",          "95% CI Bars")

        st.divider()
        st.markdown("#### 💡 Intervention Strategies")
        s1, s2 = st.columns(2)
        for col, items in [
            (s1, [("🚨","#e05c97","Early Warning System",
                   "Flag students scoring &lt;8 in G1/G2 for immediate counsellor check-ins before G3 is impacted."),
                  ("🔁","#f7c948","Repeat-Failure Protocol",
                   "Students with 2+ failures are highest risk. Create remedial tracks with smaller class sizes.")]),
            (s2, [("🎯","#4dd9ac","Personalised Goals",
                   "Set individual grade improvement targets (e.g. +2 from G1→G2). Reward milestone achievements."),
                  ("🧑‍🏫","#6ea8fe","Absence Management",
                   "High absences correlate negatively with G3. Enforce monitoring and engage parents when spikes occur.")])
        ]:
            for icon, color, title, body in items:
                col.markdown(f"""
                <div style='background:{color}18;border:1px solid {color}55;
                            border-radius:12px;padding:18px;margin-bottom:14px;'>
                    <div style='font-size:1.5rem;'>{icon}</div>
                    <div class='rtitle' style='color:{color};'>{title}</div>
                    {body}
                </div>""", unsafe_allow_html=True)

        st.markdown("""
        <div class='insight pink'>
            <b>📌 Conclusion</b><br>
            <b>Failures</b> and <b>G2 score</b> are the two most powerful G3 predictors.
            Students with 3+ failures have near-zero pass probability without structured intervention.
        </div>""", unsafe_allow_html=True)

    # ── TAB 3 ──────────────────────────────────────────────────────────────
    with tab3:
        st.markdown("## 🍺 Awareness Programs on\n### <span style='color:#f7c948;'>Lifestyle Impact</span>",
                    unsafe_allow_html=True)
        st.divider()

        st.markdown("#### 🍷 Alcohol Consumption vs Grades")
        c1, c2, c3 = st.columns(3)
        with c1: show_img("alcohol_vs_g3_bar.png",  "Bar: Alcohol Level vs Mean G3")
        with c2: show_img("alcohol_boxplot_g3.png", "Box: G3 by Alcohol Group")
        with c3: show_img("scatter_alcohol_g3.png", "Scatter + Regression")

        st.markdown("#### 🎉 Social Activity + Combined Effect")
        c4, c5 = st.columns(2)
        with c4: show_img("goout_vs_g3_bar.png",       "Goout Frequency vs Mean G3")
        with c5: show_img("heatmap_goout_walc_g3.png", "Heatmap: Goout × Weekend Alcohol → G3")

        st.divider()
        st.markdown("#### 💡 Awareness Program Design")
        a1, a2, a3 = st.columns(3)
        for col, icon, color, title, body in [
            (a1,"🎤","#f7c948","Campus Talks",
             "Data-backed presentations showing direct grade impact of high alcohol consumption on peer cohorts."),
            (a2,"📊","#e05c97","Self-Assessment Tool",
             "A quiz where students self-report lifestyle habits and receive a predicted grade range from the model."),
            (a3,"🏃","#4dd9ac","Healthy Alternatives",
             "Promote sport clubs, creative groups, and study meetups as alternatives to high-alcohol social outings."),
        ]:
            col.markdown(f"""
            <div style='background:{color}18;border:1px solid {color}55;
                        border-radius:12px;padding:18px;'>
                <div style='font-size:1.7rem;'>{icon}</div>
                <div class='rtitle' style='color:{color};'>{title}</div>
                {body}
            </div>""", unsafe_allow_html=True)

        st.markdown("""
        <div class='insight gold'>
            <b>📌 Conclusion</b><br>
            Students with <b>Very High</b> weekend alcohol (Walc=5) score
            <b>1.5–3 points lower</b> in G3. The heatmap shows students who
            both drink heavily <em>and</em> go out often are at the highest academic risk.
        </div>""", unsafe_allow_html=True)

    # ── TAB 4 ──────────────────────────────────────────────────────────────
    with tab4:
        st.markdown("## 📚 Strategies to Improve\n### <span style='color:#4dd9ac;'>Student Study Habits</span>",
                    unsafe_allow_html=True)
        st.divider()

        st.markdown("#### 📊 Evidence")
        show_img("task2_studytime_vs_grades.png", "Study Time vs G3 — Full Analysis")
        c1, c2 = st.columns(2)
        with c1: show_img("correlation_heatmap.png",  "Correlation Heatmap")
        with c2: show_img("h1_mean_g3_ci_bars.png",   "Mean G3 with 95% CI by Study Group")

        st.divider()
        st.markdown("#### 💡 Study Habit Improvement Strategies")
        s1, s2 = st.columns(2)
        for col, items in [
            (s1, [("⏱","#4dd9ac","Structured Timetables",
                   "Students in the &lt;2 hrs/week group score significantly lower. Introduce mandatory study planning at term start."),
                  ("👥","#6ea8fe","Peer Study Groups",
                   "Collaborative study increases accountability. Organise structured sessions 3× per week after school.")]),
            (s2, [("🎮","#f7c948","Gamified Learning",
                   "Use point systems, leaderboards, and weekly challenges to make extra study time engaging and self-motivated."),
                  ("📱","#e05c97","Digital Study Trackers",
                   "Encourage apps (Forest, Notion) to log weekly study hours and set visible personal improvement goals.")])
        ]:
            for icon, color, title, body in items:
                col.markdown(f"""
                <div style='background:{color}18;border:1px solid {color}55;
                            border-radius:12px;padding:18px;margin-bottom:14px;'>
                    <div style='font-size:1.5rem;'>{icon}</div>
                    <div class='rtitle' style='color:{color};'>{title}</div>
                    {body}
                </div>""", unsafe_allow_html=True)

        st.markdown("""
        <div class='insight'>
            <b>📌 Conclusion</b><br>
            ANOVA confirms study time has a <b>statistically significant</b> effect on G3.
            Moving students from the &lt;2 hrs group to the 5–10 hrs group
            is associated with an average gain of <b>2–3 grade points</b> —
            the most actionable lever available to schools.
        </div>""", unsafe_allow_html=True)
