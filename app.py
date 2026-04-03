import os
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="AIC3D Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --------------------------------------------------
# Styling (FIXED + OPTION B APPLIED)
# --------------------------------------------------
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1200px;
}

html, body, [class*="css"] {
    font-family: "Inter", "Segoe UI", sans-serif;
    color: #0f172a;
}

/* HERO */
.hero-card {
    padding: 2.2rem;
    border-radius: 22px;
    background: linear-gradient(135deg, #0f172a 0%, #172554 45%, #1e3a8a 100%);
    color: white;
    margin-bottom: 1.2rem;
    box-shadow: 0 12px 28px rgba(15, 23, 42, 0.18);
}

.hero-title {
    font-size: 2.4rem;
    font-weight: 800;
    margin-bottom: 0.5rem;
}

.hero-subtitle {
    font-size: 1.05rem;
    opacity: 0.92;
    margin-bottom: 1rem;
}

/* SECTION TITLES */
.section-title {
    font-size: 1.35rem;
    font-weight: 700;
    margin-bottom: 0.8rem;
}

/* OPTION B CARD (FIXED) */
.soft-card {
    background: #f1f5f9;
    border: 1px solid #e2e8f0;
    padding: 1.1rem;
    border-radius: 18px;
    box-shadow: 0 6px 18px rgba(15, 23, 42, 0.05);
    color: #0f172a;   /* FIX */
}

/* METRIC BOX */
[data-testid="stMetric"] {
    background: white;
    border: 1px solid #e5e7eb;
    padding: 0.8rem;
    border-radius: 16px;
    box-shadow: 0 6px 16px rgba(15, 23, 42, 0.05);
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Helper
# --------------------------------------------------
def load_csv():
    for name in ["AIC3D_v2_results.csv", "aic3d_v2_results.csv"]:
        if os.path.exists(name):
            return pd.read_csv(name)
    return None

def show_img(name, caption):
    if os.path.exists(name):
        st.image(name, caption=caption, use_container_width=True)

df = load_csv()

# --------------------------------------------------
# HERO
# --------------------------------------------------
st.markdown("""
<div class="hero-card">
    <div class="hero-title">AIC3D</div>
    <div class="hero-subtitle">
        AI-Catalyzed Drug Decay Detector<br>
        Environmental degradation prediction for pharmaceutical compounds
    </div>
    <div>
        AIC3D is a machine learning system designed to predict drug degradation behavior before environmental release.
        It uses molecular descriptors and pH conditions to evaluate whether degradation risks can be identified earlier
        than traditional laboratory-based testing.
    </div>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# METRICS
# --------------------------------------------------
col1, col2, col3, col4 = st.columns(4)
col1.metric("Model Type", "Random Forest")
col2.metric("Validation Method", "LODO")
col3.metric("Feature Vector Size", "2055")
col4.metric("Use Case", "Pre-screening")

# --------------------------------------------------
# SUMMARY
# --------------------------------------------------
left, right = st.columns([1.2, 0.8])

with left:
    st.markdown('<div class="section-title">Executive Summary</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="soft-card">
    The model performs well under internal validation but fails under Leave-One-Drug-Out testing.
    This indicates that it captures dataset-specific patterns rather than fully generalizable chemical behavior.
    </div>
    """, unsafe_allow_html=True)

with right:
    show_img("problem_context.png", "Project Context")

st.divider()

# --------------------------------------------------
# TABS
# --------------------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Overview",
    "Method",
    "Results",
    "Figures",
    "Next Steps"
])

# --------------------------------------------------
# OVERVIEW
# --------------------------------------------------
with tab1:
    c1, c2 = st.columns(2)

    with c1:
        st.markdown('<div class="section-title">Problem</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="soft-card">
        Pharmaceutical compounds persist in the environment depending on molecular structure and pH.
        Traditional testing is slow and reactive. AIC3D explores predictive screening.
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="section-title">Focus</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="soft-card">
        • Predict degradation from structure + pH<br>
        • Test generalization to unseen drugs<br>
        • Identify model limitations
        </div>
        """, unsafe_allow_html=True)

# --------------------------------------------------
# METHOD
# --------------------------------------------------
with tab2:
    st.markdown('<div class="section-title">Methodology</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="soft-card">
    Features: Morgan fingerprints + chemical descriptors + pH<br><br>
    Model: Random Forest<br><br>
    Validation:
    • 80/20 split + 5-fold CV<br>
    • LODO (Leave-One-Drug-Out)
    </div>
    """, unsafe_allow_html=True)

    show_img("project_pipeline.png", "Pipeline")

# --------------------------------------------------
# RESULTS
# --------------------------------------------------
with tab3:
    r1, r2, r3 = st.columns(3)
    r1.metric("CV MSE", "0.0277")
    r2.metric("Train MSE", "0.0130")
    r3.metric("Test MSE", "0.1062")

    st.markdown("""
    <div class="soft-card">
    Strong internal performance, but LODO reveals weak generalization.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Feature Importance")
    importance_df = pd.DataFrame({
        "Feature": ["TPSA", "pH", "MolWt", "Other"],
        "Importance": [0.1104, 0.0653, 0.0042, 0.8201]
    }).sort_values("Importance")

    st.bar_chart(importance_df.set_index("Feature"))

    if df is not None:
        st.markdown("### LODO Results")
        st.dataframe(df, use_container_width=True)

        numeric_cols = df.select_dtypes(include="number").columns
        if len(numeric_cols) > 0:
            st.bar_chart(df.set_index(df.columns[0])[numeric_cols])

# --------------------------------------------------
# FIGURES
# --------------------------------------------------
with tab4:
    show_img("feature_importance.png", "Feature Importance")
    show_img("lodo_results_plot.png", "LODO Performance")
    show_img("summary_metrics.png", "Summary Metrics")

# --------------------------------------------------
# NEXT STEPS
# --------------------------------------------------
with tab5:
    st.markdown('<div class="section-title">Next Steps</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="soft-card">
    • Expand dataset<br>
    • Get expert validation<br>
    • Improve generalization<br>
    • Publish research/write-up
    </div>
    """, unsafe_allow_html=True)
