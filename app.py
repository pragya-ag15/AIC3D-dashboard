import os
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="AIC3D Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------
# Safe styling only
# -----------------------------
st.markdown("""
<style>
.block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Global readable text */
html, body, [data-testid="stAppViewContainer"], [data-testid="stAppViewContainer"] * {
    color: #0f172a;
}

/* Hero section */
.hero {
    background: linear-gradient(135deg, #0f172a 0%, #172554 50%, #1d4ed8 100%);
    color: white !important;
    padding: 2rem 2rem 1.6rem 2rem;
    border-radius: 22px;
    margin-bottom: 1.25rem;
}
.hero h1, .hero h3, .hero p, .hero div {
    color: white !important;
}
.hero-title {
    font-size: 2.5rem;
    font-weight: 800;
    margin-bottom: 0.4rem;
}
.hero-subtitle {
    font-size: 1.05rem;
    opacity: 0.95;
    margin-bottom: 0.9rem;
}

/* Section labels */
.section-label {
    font-size: 1.2rem;
    font-weight: 700;
    margin-bottom: 0.6rem;
    color: #0f172a !important;
}

/* Metric boxes */
[data-testid="stMetric"] {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 0.85rem;
    box-shadow: 0 4px 14px rgba(15, 23, 42, 0.05);
}
[data-testid="stMetricLabel"] {
    color: #475569 !important;
    font-size: 0.85rem !important;
}
[data-testid="stMetricValue"] {
    color: #0f172a !important;
    font-size: 1.2rem !important;
    font-weight: 700 !important;
    line-height: 1.2 !important;
}
[data-testid="stMetricDelta"] {
    display: none;
}

/* Tabs */
button[data-baseweb="tab"] {
    color: #0f172a !important;
    font-weight: 600 !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: #1d4ed8 !important;
}

/* Dataframe / markdown readability */
.stMarkdown p, .stMarkdown li, .stMarkdown div, .stMarkdown span {
    color: #0f172a !important;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Helpers
# -----------------------------
def load_csv():
    for fname in ["AIC3D_v2_results.csv", "aic3d_v2_results.csv"]:
        if os.path.exists(fname):
            return pd.read_csv(fname)
    return None

def show_img(fname, caption=None):
    if os.path.exists(fname):
        st.image(fname, caption=caption, use_container_width=True)

df = load_csv()

# -----------------------------
# Hero
# -----------------------------
st.markdown("""
<div class="hero">
    <div class="hero-title">AIC3D</div>
    <div class="hero-subtitle">AI-Catalyzed Drug Decay Detector</div>
    <div style="font-size:1rem; line-height:1.7;">
        Environmental degradation prediction for pharmaceutical compounds.<br><br>
        AIC3D is a machine learning system designed to estimate drug degradation behavior before environmental release,
        using molecular descriptors and pH-dependent conditions to test whether computational screening can provide
        earlier insight than traditional laboratory-only workflows.
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Metrics
# -----------------------------
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("Model Type", "Random Forest")
with m2:
    st.metric("Validation Method", "LODO")
with m3:
    st.metric("Feature Vector Size", "2055")
with m4:
    st.metric("Use Case", "Pre-screening")

m5, m6, m7 = st.columns(3)
with m5:
    st.metric("CV MSE", "0.0277")
with m6:
    st.metric("Train MSE", "0.0130")
with m7:
    st.metric("Test MSE", "0.1062")

st.write("")

# -----------------------------
# Key finding + hero visual
# -----------------------------
left, right = st.columns([1.15, 0.85])

with left:
    st.markdown('<div class="section-label">Key Finding</div>', unsafe_allow_html=True)
    with st.container(border=True):
        st.write(
            "The model achieves strong internal performance but fails under Leave-One-Drug-Out validation. "
            "This indicates limited generalization across unseen drugs and shows why rigorous evaluation "
            "matters in scientific machine learning."
        )

with right:
    if os.path.exists("problem_context.png"):
        st.image("problem_context.png", caption="Project context", use_container_width=True)

st.divider()

# -----------------------------
# Tabs
# -----------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Overview", "Method", "Results", "Figures", "Conclusion"]
)

# -----------------------------
# Overview
# -----------------------------
with tab1:
    c1, c2 = st.columns(2)

    with c1:
        st.markdown('<div class="section-label">Problem Context</div>', unsafe_allow_html=True)
        with st.container(border=True):
            st.write(
                "Pharmaceutical compounds can enter the environment through wastewater, improper disposal, "
                "and incomplete treatment. Their persistence depends on molecular structure and environmental "
                "conditions such as pH."
            )
            st.write(
                "AIC3D explores whether machine learning can estimate degradation-related behavior earlier "
                "than traditional reactive testing."
            )

    with c2:
        st.markdown('<div class="section-label">Project Focus</div>', unsafe_allow_html=True)
        with st.container(border=True):
            st.write("• Predict degradation-related behavior from structure and pH")
            st.write("• Test whether the model generalizes to unseen drugs")
            st.write("• Identify whether performance reflects real chemical signal or shortcut learning")

# -----------------------------
# Method
# -----------------------------
with tab2:
    c1, c2 = st.columns([1, 1])

    with c1:
        st.markdown('<div class="section-label">Methodology</div>', unsafe_allow_html=True)
        with st.container(border=True):
            st.write("**Features**")
            st.write("• 2048-bit Morgan fingerprints")
            st.write("• TPSA")
            st.write("• logP")
            st.write("• Molecular Weight")
            st.write("• H-bond Donors and Acceptors")
            st.write("• pH")
            st.write("")
            st.write("**Model**")
            st.write("Random Forest Regressor")
            st.write("")
            st.write("**Validation**")
            st.write("• 80/20 split with cross-validation")
            st.write("• Leave-One-Drug-Out evaluation")

    with c2:
        if os.path.exists("project_pipeline.png"):
            st.image("project_pipeline.png", caption="AIC3D pipeline", use_container_width=True)
        else:
            with st.container(border=True):
                st.write(
                    "Pipeline figure not found. Keep `project_pipeline.png` in the repo root if you want it displayed here."
                )

# -----------------------------
# Results
# -----------------------------
with tab3:
    c1, c2 = st.columns([0.95, 1.05])

    with c1:
        st.markdown('<div class="section-label">Feature Importance</div>', unsafe_allow_html=True)
        importance_df = pd.DataFrame({
            "Feature": ["TPSA", "pH", "MolWt", "Other descriptors / fingerprints"],
            "Importance": [0.1104, 0.0653, 0.0042, 0.8201]
        }).sort_values("Importance")
        st.bar_chart(importance_df.set_index("Feature"))

    with c2:
        st.markdown('<div class="section-label">Interpretation</div>', unsafe_allow_html=True)
        with st.container(border=True):
            st.write(
                "The model appears especially sensitive to TPSA and pH. While this is partly chemically meaningful, "
                "LODO evaluation shows that the learned patterns do not transfer reliably to unseen compounds."
            )

    st.write("")
    st.markdown('<div class="section-label">LODO Results</div>', unsafe_allow_html=True)

    if df is not None:
        st.dataframe(df, use_container_width=True)

        numeric_cols = df.select_dtypes(include="number").columns.tolist()
        first_col = df.columns[0]

        preferred = None
        for col in ["RandomForest", "MSE", "RMSE", "R2"]:
            if col in df.columns:
                preferred = col
                break

        if preferred:
            st.markdown(f"**{preferred} by held-out drug**")
            chart_df = df[[first_col, preferred]].copy().set_index(first_col)
            st.bar_chart(chart_df)
        elif numeric_cols:
            st.markdown("**Numeric overview**")
            st.bar_chart(df.set_index(first_col)[numeric_cols])

    else:
        with st.container(border=True):
            st.write("`AIC3D_v2_results.csv` was not found in the repo root.")

# -----------------------------
# Figures
# -----------------------------
with tab4:
    figure_list = [
        ("feature_importance.png", "Feature importance"),
        ("lodo_results_plot.png", "LODO performance"),
        ("summary_metrics.png", "Summary metrics"),
        ("problem_context.png", "Project context"),
        ("project_pipeline.png", "Project pipeline"),
    ]

    existing = [(f, c) for f, c in figure_list if os.path.exists(f)]

    if existing:
        for i in range(0, len(existing), 2):
            cols = st.columns(2)
            for j, col in enumerate(cols):
                if i + j < len(existing):
                    with col:
                        st.image(existing[i + j][0], caption=existing[i + j][1], use_container_width=True)
    else:
        with st.container(border=True):
            st.write("No figure files were found in the repo root.")

# -----------------------------
# Conclusion
# -----------------------------
with tab5:
    st.markdown('<div class="section-label">Conclusion</div>', unsafe_allow_html=True)
    with st.container(border=True):
        st.write(
            "AIC3D demonstrates that molecular descriptors and environmental variables can capture "
            "degradation-related patterns. However, evaluation through Leave-One-Drug-Out reveals that "
            "these patterns do not generalize reliably across unseen compounds."
        )
        st.write(
            "The project’s strongest contribution is methodological honesty: strong internal metrics alone "
            "are not sufficient to validate predictive systems in chemistry."
        )
        st.write(
            "This positions AIC3D as a complete and transparent research prototype rather than an overclaimed predictive tool."
        )
