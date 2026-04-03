import os
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="AIC3D Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --------------------------------------------------
# CSS (FINAL POLISH + METRIC SIZE FIX)
# --------------------------------------------------
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1200px;
}

/* GLOBAL TEXT */
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
}

.hero-subtitle {
    font-size: 1.05rem;
    opacity: 0.92;
}

/* SECTION */
.section-title {
    font-size: 1.35rem;
    font-weight: 700;
    margin-bottom: 0.8rem;
}

/* CARDS */
.soft-card {
    background: #f1f5f9;
    border: 1px solid #e2e8f0;
    padding: 1.1rem;
    border-radius: 18px;
    box-shadow: 0 6px 18px rgba(15, 23, 42, 0.05);
}

/* METRICS */
[data-testid="stMetric"] {
    background: white;
    border: 1px solid #e5e7eb;
    padding: 0.8rem;
    border-radius: 16px;
}

/* FIX LABEL */
[data-testid="stMetricLabel"] {
    font-size: 0.85rem !important;
    color: #475569 !important;
}

/* FIX VALUE (IMPORTANT) */
[data-testid="stMetricValue"] {
    font-size: 1.4rem !important;   /* smaller so it fits */
    font-weight: 600 !important;
    color: #0f172a !important;
}

/* fallback */
[data-testid="stMetric"] * {
    color: #0f172a !important;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Helpers
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
    <br>
    AIC3D predicts degradation behavior using molecular descriptors and environmental pH.
    The system evaluates whether computational screening can provide earlier insight than traditional testing.
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

col5, col6, col7 = st.columns(3)

col5.metric("CV MSE", "0.0277")
col6.metric("Train MSE", "0.0130")
col7.metric("Test MSE", "0.1062")

st.divider()

# --------------------------------------------------
# SUMMARY
# --------------------------------------------------
st.markdown('<div class="section-title">Key Finding</div>', unsafe_allow_html=True)
st.markdown("""
<div class="soft-card">
The model achieves strong internal performance but fails under Leave-One-Drug-Out validation.
This indicates limited generalization across unseen drugs, highlighting the importance of evaluation design
in scientific machine learning workflows.
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# TABS
# --------------------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Overview",
    "Method",
    "Results",
    "Figures",
    "Conclusion"
])

# --------------------------------------------------
# OVERVIEW
# --------------------------------------------------
with tab1:
    st.markdown('<div class="section-title">Problem Context</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="soft-card">
    Pharmaceutical compounds enter the environment through wastewater and disposal.
    Their persistence depends on molecular structure and pH conditions.

    AIC3D explores whether machine learning can estimate degradation trends earlier than traditional testing methods.
    </div>
    """, unsafe_allow_html=True)

# --------------------------------------------------
# METHOD
# --------------------------------------------------
with tab2:
    st.markdown('<div class="section-title">Methodology</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="soft-card">
    Features:
    • Morgan fingerprints (2048-bit)<br>
    • TPSA, logP, molecular weight<br>
    • Hydrogen bonding features<br>
    • pH<br><br>

    Model: Random Forest<br><br>

    Validation:
    • Cross-validation (internal)<br>
    • Leave-One-Drug-Out (external generalization)
    </div>
    """, unsafe_allow_html=True)

    show_img("project_pipeline.png", "Pipeline")

# --------------------------------------------------
# RESULTS
# --------------------------------------------------
with tab3:
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
    show_img("summary_metrics.png", "Summary")

# --------------------------------------------------
# CONCLUSION (FIXED)
# --------------------------------------------------
with tab5:
    st.markdown('<div class="section-title">Conclusion</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="soft-card">
    AIC3D demonstrates that molecular descriptors and environmental variables can capture degradation-related patterns.
    However, evaluation through Leave-One-Drug-Out reveals that these patterns do not generalize reliably across unseen compounds.

    The project highlights a key insight: strong internal metrics are not sufficient to validate predictive systems in chemistry.
    Robust generalization requires more diverse data and more rigorous validation strategies.

    This positions AIC3D as a complete and transparent research prototype rather than an overfitted predictive tool.
    </div>
    """, unsafe_allow_html=True)
