import os
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="AIC3D Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --------------------------------------------------
# Styling
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
}
.hero-card {
    padding: 2.2rem 2.2rem 1.8rem 2.2rem;
    border-radius: 22px;
    background: linear-gradient(135deg, #0f172a 0%, #172554 45%, #1e3a8a 100%);
    color: white;
    margin-bottom: 1.2rem;
    box-shadow: 0 12px 28px rgba(15, 23, 42, 0.18);
}
.hero-title {
    font-size: 2.4rem;
    font-weight: 800;
    line-height: 1.1;
    margin-bottom: 0.5rem;
}
.hero-subtitle {
    font-size: 1.05rem;
    opacity: 0.92;
    margin-bottom: 1rem;
}
.section-title {
    font-size: 1.35rem;
    font-weight: 700;
    margin-top: 0.3rem;
    margin-bottom: 0.8rem;
    color: #0f172a;
}
.soft-card {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    padding: 1.1rem 1.1rem 0.9rem 1.1rem;
    border-radius: 18px;
    box-shadow: 0 6px 18px rgba(15, 23, 42, 0.04);
    height: 100%;
}
.metric-box {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 18px;
    padding: 1rem;
    box-shadow: 0 6px 16px rgba(15, 23, 42, 0.05);
}
.caption-note {
    color: #475569;
    font-size: 0.95rem;
}
hr {
    margin-top: 2rem !important;
    margin-bottom: 2rem !important;
}
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
# Helpers
# --------------------------------------------------
def image_exists(path: str) -> bool:
    return os.path.exists(path)

def show_image_clean(path: str, caption: str):
    if image_exists(path):
        st.image(path, caption=caption, use_container_width=True)

def first_existing(paths):
    for p in paths:
        if os.path.exists(p):
            return p
    return None

# --------------------------------------------------
# Data loading
# --------------------------------------------------
df = None
csv_candidates = [
    "AIC3D_v2_results.csv",
    "aic3d_v2_results.csv"
]

csv_path = first_existing(csv_candidates)
if csv_path:
    df = pd.read_csv(csv_path)

# --------------------------------------------------
# Hero section
# --------------------------------------------------
st.markdown("""
<div class="hero-card">
    <div class="hero-title">AIC3D</div>
    <div class="hero-subtitle">
        AI-Catalyzed Drug Decay Detector<br>
        Environmental degradation prediction for pharmaceutical compounds
    </div>
    <div style="font-size:1rem; line-height:1.7; max-width:900px;">
        AIC3D is a machine learning project built to predict drug degradation behavior before environmental release,
        using molecular descriptors and pH-dependent conditions. The project explores whether computational screening
        can help identify degradation risks earlier, rather than relying only on reactive laboratory testing after
        manufacturing and distribution.
    </div>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Top summary row
# --------------------------------------------------
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Model Type", "Random Forest")
with col2:
    st.metric("Validation Method", "LODO")
with col3:
    st.metric("Feature Vector Size", "2055")
with col4:
    st.metric("Primary Use Case", "Pre-screening")

st.markdown("")

# --------------------------------------------------
# Executive summary + key visual
# --------------------------------------------------
left, right = st.columns([1.15, 0.85])

with left:
    st.markdown('<div class="section-title">Executive Summary</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="soft-card">
    <b>Core question:</b> Can molecular structure and environmental context be used to estimate degradation trends across drugs?<br><br>
    <b>Main outcome:</b> The model performed strongly on internal validation, but Leave-One-Drug-Out testing revealed poor
    generalization to unseen drugs. This means the system captures useful patterns within the dataset, but is not yet robust
    enough for reliable cross-drug prediction.<br><br>
    The strongest value of the project is therefore not just the model itself, but the fact that a more rigorous evaluation
    framework exposed the true limitation clearly.
    </div>
    """, unsafe_allow_html=True)

with right:
    hero_figure = first_existing(["problem_context.png", "summary_metrics.png", "project_pipeline.png"])
    if hero_figure:
        st.image(hero_figure, use_container_width=True)
    else:
        st.markdown("""
        <div class="soft-card">
        <b>Key message</b><br><br>
        AIC3D is strongest as a research prototype because it:
        <ul>
            <li>builds an end-to-end ML pipeline</li>
            <li>uses chemically grounded descriptors</li>
            <li>tests honest generalization through LODO</li>
            <li>identifies the current failure mode clearly</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# --------------------------------------------------
# Navigation tabs
# --------------------------------------------------
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Overview",
    "Method",
    "Results",
    "Figures",
    "Limitations",
    "Next Steps"
])

# --------------------------------------------------
# TAB 1: Overview
# --------------------------------------------------
with tab1:
    c1, c2 = st.columns([1, 1])

    with c1:
        st.markdown('<div class="section-title">Problem Statement</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="soft-card">
        Pharmaceutical compounds often enter the environment through wastewater, improper disposal, and incomplete treatment.
        Their persistence depends on both molecular structure and environmental conditions such as pH.
        Traditional degradation testing is often slow, expensive, and reactive.

        AIC3D explores whether a machine learning model can provide an earlier computational screening layer to flag compounds
        that may degrade slowly or unpredictably.
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="section-title">Project Focus</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="soft-card">
        <ul>
            <li>Predict degradation-related behavior from structure and pH</li>
            <li>Test whether the model generalizes to completely unseen drugs</li>
            <li>Distinguish real chemical signal from dataset-specific shortcuts</li>
            <li>Build a foundation for later research and expert validation</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")
    st.markdown('<div class="section-title">Dataset Snapshot</div>', unsafe_allow_html=True)

    dataset_summary = pd.DataFrame({
        "Aspect": [
            "Drug examples",
            "Conditions included",
            "Target behavior",
            "Feature sources",
            "Validation focus"
        ],
        "Details": [
            "Ibuprofen, Aspirin, Paracetamol, Naproxen, Diclofenac, plus expanded additions",
            "Multiple pH-dependent conditions",
            "Degradation rate / log-transformed behavior",
            "RDKit descriptors + Morgan fingerprints + pH",
            "Cross-drug generalization"
        ]
    })
    st.dataframe(dataset_summary, use_container_width=True, hide_index=True)

# --------------------------------------------------
# TAB 2: Method
# --------------------------------------------------
with tab2:
    m1, m2 = st.columns([1.05, 0.95])

    with m1:
        st.markdown('<div class="section-title">Input Features and Model</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="soft-card">
        <b>Input features</b>
        <ul>
            <li>2048-bit Morgan fingerprints (radius = 2)</li>
            <li>TPSA</li>
            <li>logP</li>
            <li>Molecular Weight</li>
            <li>H-bond Donors</li>
            <li>H-bond Acceptors</li>
            <li>pH</li>
        </ul>
        This produces a final feature vector of <b>2055 dimensions</b>.<br><br>
        <b>Model:</b> Random Forest Regressor
        </div>
        """, unsafe_allow_html=True)

    with m2:
        st.markdown('<div class="section-title">Evaluation Strategy</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="soft-card">
        <b>Internal evaluation</b>
        <ul>
            <li>80/20 train-test split</li>
            <li>5-fold cross-validation using MSE</li>
        </ul>
        <b>Generalization evaluation</b>
        <ul>
            <li>Leave-One-Drug-Out (LODO)</li>
            <li>One full drug held out at a time</li>
            <li>Tests whether the model generalizes across compounds</li>
        </ul>
        <b>Why LODO matters:</b> random splits can look strong even when a model has already seen highly similar patterns.
        LODO is more honest because it better simulates prediction on truly unseen drugs.
        </div>
        """, unsafe_allow_html=True)

    pipeline_img = first_existing(["project_pipeline.png"])
    if pipeline_img:
        st.markdown("")
        st.markdown('<div class="section-title">Pipeline Diagram</div>', unsafe_allow_html=True)
        st.image(pipeline_img, use_container_width=True)

# --------------------------------------------------
# TAB 3: Results
# --------------------------------------------------
with tab3:
    r1, r2, r3 = st.columns(3)
    with r1:
        st.metric("5-Fold CV MSE", "0.0277")
    with r2:
        st.metric("Train MSE", "0.0130")
    with r3:
        st.metric("Test MSE", "0.1062")

    st.markdown("")
    st.markdown("""
    <div class="soft-card">
    These internal metrics suggest that the model is learning meaningful relationships.
    However, internal performance alone is not enough. The real test is whether the system can predict degradation
    behavior for compounds it has never seen before.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("")
    c1, c2 = st.columns([0.95, 1.05])

    with c1:
        st.markdown('<div class="section-title">Feature Importance</div>', unsafe_allow_html=True)
        feature_importance_df = pd.DataFrame({
            "Feature": ["TPSA", "pH", "MolWt", "Other descriptors / fingerprint contributions"],
            "Importance": [0.1104, 0.0653, 0.0042, 0.8201]
        }).sort_values("Importance", ascending=True)
        st.bar_chart(feature_importance_df.set_index("Feature"))

    with c2:
        st.markdown('<div class="section-title">Interpretation</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="soft-card">
        The model appears especially sensitive to <b>TPSA</b> and <b>pH</b>. This is partly chemically meaningful,
        but the LODO results indicate that these signals are not enough for strong out-of-drug generalization.
        In practice, the model may be learning a mixture of real chemistry and dataset-specific shortcuts.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")
    st.markdown('<div class="section-title">Leave-One-Drug-Out Results</div>', unsafe_allow_html=True)

    if df is not None:
        st.dataframe(df, use_container_width=True)

        numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
        first_col = df.columns[0]

        # Show a cleaner chart if possible
        chart_rendered = False

        for preferred_col in ["RandomForest", "MSE", "R2", "RMSE"]:
            if preferred_col in df.columns:
                chart_df = df[[first_col, preferred_col]].copy()
                chart_df = chart_df.set_index(first_col)
                st.markdown(f'<div class="section-title">{preferred_col} by Held-Out Drug</div>', unsafe_allow_html=True)
                st.bar_chart(chart_df)
                chart_rendered = True
                break

        if not chart_rendered and len(numeric_cols) > 0:
            st.markdown('<div class="section-title">Numeric Result Overview</div>', unsafe_allow_html=True)
            st.bar_chart(df.set_index(first_col)[numeric_cols])

        st.markdown("""
        <div class="soft-card">
        <b>Conclusion from LODO:</b> the model does not generalize reliably across unseen drugs.
        This is not a weakness in presentation; it is one of the strongest parts of the project because it shows scientific honesty,
        proper evaluation, and a clearly defined next research step.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.error("AIC3D_v2_results.csv was not found in the repo root.")

# --------------------------------------------------
# TAB 4: Figures
# --------------------------------------------------
with tab4:
    st.markdown('<div class="section-title">Project Visuals</div>', unsafe_allow_html=True)

    figure_files = [
        ("problem_context.png", "Environmental context and motivation"),
        ("project_pipeline.png", "AIC3D project pipeline"),
        ("feature_importance.png", "Feature importance visualization"),
        ("lodo_results_plot.png", "LODO performance across drugs"),
        ("summary_metrics.png", "Quantitative summary"),
        ("lodo_r2_plot.png", "LODO R² by drug")
    ]

    existing_figures = [(path, caption) for path, caption in figure_files if os.path.exists(path)]

    if existing_figures:
        for i in range(0, len(existing_figures), 2):
            cols = st.columns(2)
            for j, col in enumerate(cols):
                if i + j < len(existing_figures):
                    path, caption = existing_figures[i + j]
                    with col:
                        st.image(path, caption=caption, use_container_width=True)
    else:
        st.markdown("""
        <div class="soft-card">
        No figures were detected yet. Make sure the PNG files are in the repo root with the exact names used in the code.
        </div>
        """, unsafe_allow_html=True)

# --------------------------------------------------
# TAB 5: Limitations
# --------------------------------------------------
with tab5:
    l1, l2 = st.columns(2)

    with l1:
        st.markdown('<div class="section-title">Current Limitations</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="soft-card">
        <ul>
            <li>Small and heterogeneous dataset</li>
            <li>Limited cross-drug coverage</li>
            <li>Strong sensitivity to pH-related patterns</li>
            <li>Random split performance can overestimate usefulness</li>
            <li>More external validation is needed before practical deployment</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    with l2:
        st.markdown('<div class="section-title">Why This Still Matters</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="soft-card">
        AIC3D still matters because it establishes:
        <ul>
            <li>a complete prototype pipeline</li>
            <li>a chemically grounded feature framework</li>
            <li>a more rigorous validation approach through LODO</li>
            <li>a clear direction for improvement</li>
        </ul>
        This turns the project from a basic ML demo into a research-oriented system with meaningful insight.
        </div>
        """, unsafe_allow_html=True)

# --------------------------------------------------
# TAB 6: Next Steps
# --------------------------------------------------
with tab6:
    n1, n2 = st.columns([1, 1])

    with n1:
        st.markdown('<div class="section-title">Planned Next Steps</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="soft-card">
        <ul>
            <li>Expand the dataset with more drugs and more condition diversity</li>
            <li>Obtain expert review from environmental chemistry and pharmaceutical specialists</li>
            <li>Build a stronger external validation benchmark</li>
            <li>Compare multiple model families beyond Random Forest</li>
            <li>Publish a project write-up, article, or paper</li>
            <li>Create a stronger public-facing dashboard and website</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    with n2:
        st.markdown('<div class="section-title">Final Takeaway</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="soft-card">
        AIC3D successfully built an end-to-end pipeline for predicting drug degradation behavior from molecular
        and environmental inputs. The strongest result of the project is not just that a model was trained, but that
        a more realistic validation setup revealed the main limitation clearly: <b>generalization across unseen drugs remains the core challenge.</b><br><br>
        That makes this project a strong foundation for a next version rather than an overclaimed finished solution.
        </div>
        """, unsafe_allow_html=True)
