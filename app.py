import os
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="AIC3D Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
.block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}
.hero-title {
    font-size: 3rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    margin-bottom: 0.2rem;
}
.hero-subtitle {
    font-size: 1.1rem;
    font-weight: 700;
    margin-bottom: 1rem;
    opacity: 0.95;
}
.hero-text {
    font-size: 1rem;
    line-height: 1.8;
    max-width: 980px;
}
.section-title {
    font-size: 1.18rem;
    font-weight: 700;
    margin-bottom: 0.65rem;
}
.border-box {
    border: 1px solid rgba(148, 163, 184, 0.35);
    border-radius: 16px;
    padding: 1rem 1.1rem;
    margin-bottom: 1rem;
}
.border-box-subtle {
    border: 1px solid rgba(148, 163, 184, 0.22);
    border-radius: 16px;
    padding: 1rem 1.1rem;
    margin-bottom: 1rem;
}
[data-testid="stMetric"] {
    border: 1px solid rgba(148, 163, 184, 0.28);
    border-radius: 16px;
    padding: 0.9rem 0.9rem 0.8rem 0.9rem;
}
[data-testid="stMetricLabel"] {
    font-size: 0.82rem !important;
}
[data-testid="stMetricValue"] {
    font-size: 1.12rem !important;
    line-height: 1.2 !important;
    font-weight: 700 !important;
}
button[data-baseweb="tab"] {
    font-weight: 600 !important;
}
</style>
""", unsafe_allow_html=True)

# -----------------------
# helper
# -----------------------
def try_load_csv(filenames):
    for fname in filenames:
        if os.path.exists(fname):
            return pd.read_csv(fname), fname
    return None, None

lodo_df, lodo_path = try_load_csv([
    "AIC3D_v2_lodo_both.csv",
    "aic3d_v2_lodo_both.csv"
])

# -----------------------
# sidebar
# -----------------------
with st.sidebar:
    st.title("AIC3D")
    st.caption("Research project dashboard")

    st.markdown("### Links")
    st.markdown("[GitHub](https://github.com/pragya-ag15/AIC3D-dashboard)")
    st.markdown("[LinkedIn](https://www.linkedin.com/in/pragyaag15/)")
    st.markdown("[Email](mailto:pragyaagarwal004@gmail.com)")

    st.markdown("### What this dashboard shows")
    st.write(
        "AIC3D explores whether simple molecular descriptors and environmental pH "
        "can predict pharmaceutical degradation behavior, and where that approach breaks down."
    )

    if lodo_df is not None and lodo_path is not None:
        with open(lodo_path, "rb") as f:
            st.download_button(
                label="Download comparison CSV",
                data=f,
                file_name=os.path.basename(lodo_path),
                mime="text/csv",
                use_container_width=True
            )

# -----------------------
# hero
# -----------------------
st.markdown('<div class="hero-title">AIC3D</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-subtitle">AI-Catalyzed Drug Degradation Detector</div>',
    unsafe_allow_html=True
)
st.markdown(
    """
    <div class="hero-text">
    AIC3D is an exploratory machine learning research project investigating whether simple molecular descriptors
    and environmental pH can predict pharmaceutical degradation behavior.<br><br>
    The final result is not a claim of predictive success, but a scientific insight:
    <b>models can capture patterns within constrained chemical spaces, but fail to generalize reliably across compounds.</b>
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------
# top metrics
# -----------------------
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("Final Framing", "Exploratory Research")
with m2:
    st.metric("Core Validation", "LODO")
with m3:
    st.metric("Experiments", "2")
with m4:
    st.metric("Main Insight", "Generalization Limit")

st.divider()

st.markdown("## Final Takeaway")
st.markdown(
    """
    <div class="border-box">
    In a chemically diverse dataset, predictions were dominated by <b>pH</b> and failed to generalize across drug classes.
    In a chemically similar dataset, <b>structural descriptors</b> became more informative and internal performance improved,
    but Leave-One-Drug-Out validation still remained weak. This suggests that coarse descriptor-based ML can serve as a baseline,
    but not as a robust cross-compound predictor of degradation behavior.
    </div>
    """,
    unsafe_allow_html=True
)

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    ["Overview", "Experiments", "Results", "Expert Feedback", "Figures", "Conclusion"]
)

# -----------------------
# overview
# -----------------------
with tab1:
    c1, c2 = st.columns(2)

    with c1:
        st.markdown('<div class="section-title">Research Question</div>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="border-box">
            Can simple molecular descriptors and environmental pH predict pharmaceutical degradation
            behavior in a way that generalizes to unseen compounds?
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:
        st.markdown('<div class="section-title">Why It Matters</div>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="border-box">
            Pharmaceutical persistence affects environmental fate and exposure risk.
            If computational methods could estimate degradation earlier, they could support
            screening before reactive testing stages.
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown('<div class="section-title">Project Scope</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="border-box-subtle">
        AIC3D does <b>not</b> claim to be a deployable predictor. It is positioned as an exploratory,
        research-style study of what descriptor-based ML can and cannot learn from small degradation datasets.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="section-title">Method Summary</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="border-box">
        <b>Features:</b> LogP, Molecular Weight, H-bond Donors, H-bond Acceptors, TPSA, pH<br><br>
        <b>Models:</b> Linear Regression and Random Forest<br><br>
        <b>Validation:</b> Train/Test Split, Cross-Validation, and Leave-One-Drug-Out (LODO)<br><br>
        <b>Target:</b> log-transformed degradation/rate constant values
        </div>
        """,
        unsafe_allow_html=True
    )

# -----------------------
# experiments
# -----------------------
with tab2:
    c1, c2 = st.columns(2)

    with c1:
        st.markdown('<div class="section-title">Experiment 1 — Diverse Drugs</div>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="border-box">
            <b>Drugs:</b> Amoxicillin, Clarithromycin, Trimethoprim<br>
            <b>Points:</b> 9<br><br>
            <b>Purpose:</b> Test whether descriptor-based ML can generalize across chemically distinct compounds.<br><br>
            <b>Observation:</b> Strong failure under CV and LODO. Feature importance showed pH dominating predictions.
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:
        st.markdown('<div class="section-title">Experiment 2 — Similar-Class Drugs</div>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="border-box">
            <b>Drugs:</b> Aspirin, Diclofenac, Ibuprofen, Naproxen, Paracetamol<br>
            <b>Points:</b> 17<br><br>
            <b>Purpose:</b> Test whether performance improves within a more chemically similar space.<br><br>
            <b>Observation:</b> Better internal metrics and stronger role for structural descriptors, but weak LODO remained.
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown('<div class="section-title">Why Two Experiments Matter</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="border-box-subtle">
        The comparison shows that model behavior changes with chemical diversity:
        heterogeneous datasets push the model toward environmental shortcuts like pH,
        while homogeneous datasets allow more within-class structural learning. Neither setting produced robust generalization.
        </div>
        """,
        unsafe_allow_html=True
    )

# -----------------------
# results
# -----------------------
with tab3:
    st.markdown('<div class="section-title">Final Comparison</div>', unsafe_allow_html=True)

    summary_df = pd.DataFrame({
        "Experiment": ["Diverse drugs", "NSAIDs / similar class"],
        "Train/Test RF R²": [0.7641, 0.9158],
        "CV RF R²": [-21.2320, 0.7157],
        "Overall LODO RF R²": [-0.0677, 0.2327],
        "Dominant Signal": ["pH", "Structure"]
    })
    st.dataframe(summary_df, use_container_width=True, hide_index=True)

    st.markdown('<div class="section-title">Interpretation</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="border-box">
        <b>Internal performance improved in the similar-class dataset</b>, but this did not translate into strong held-out drug performance.<br><br>
        This means the model can learn local or within-class relationships, yet still fails to become a reliable predictor for truly unseen compounds.
        </div>
        """,
        unsafe_allow_html=True
    )

    c1, c2 = st.columns(2)

    with c1:
        st.markdown('<div class="section-title">Experiment 1 Feature Importance</div>', unsafe_allow_html=True)
        exp1_df = pd.DataFrame({
            "Feature": ["pH", "LogP", "MW", "TPSA", "HBA", "HBD"],
            "Importance": [0.622647, 0.115581, 0.103378, 0.088683, 0.066999, 0.002712]
        }).sort_values("Importance")
        st.bar_chart(exp1_df.set_index("Feature"))

    with c2:
        st.markdown('<div class="section-title">Experiment 2 Feature Importance</div>', unsafe_allow_html=True)
        exp2_df = pd.DataFrame({
            "Feature": ["MW", "HBD", "TPSA", "pH", "LogP", "HBA"],
            "Importance": [0.458990, 0.285239, 0.115907, 0.067660, 0.067236, 0.004968]
        }).sort_values("Importance")
        st.bar_chart(exp2_df.set_index("Feature"))

    if lodo_df is not None:
        st.markdown('<div class="section-title">LODO Results Table</div>', unsafe_allow_html=True)
        st.dataframe(lodo_df, use_container_width=True)

# -----------------------
# expert feedback
# -----------------------
with tab4:
    st.markdown('<div class="section-title">Why the Expert Feedback Matters</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="border-box">
        External researchers consistently aligned with the project’s final interpretation:
        small and chemically diverse datasets are insufficient for robust generalization,
        and degradation is governed by specific reactive functionalities and mechanistic pathways
        that are not captured well by coarse descriptors alone.
        </div>
        """,
        unsafe_allow_html=True
    )

    feedback_df = pd.DataFrame({
        "Source": [
            "EPA cheminformatics expert",
            "Biodegradation researcher",
            "Environmental chemistry expert",
            "Environmental chemistry researcher"
        ],
        "Main takeaway": [
            "Dataset too small and chemically heterogeneous for meaningful generalizable ML",
            "Very small datasets cannot support reliable structure–activity learning; leakage must be avoided",
            "Dataset too small for meaningful model",
            "Simple global descriptors are useful as a baseline, but not enough across diverse classes"
        ]
    })
    st.dataframe(feedback_df, use_container_width=True, hide_index=True)

    st.markdown('<div class="section-title">What We Learned</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="border-box-subtle">
        • Descriptor-only models can provide a useful baseline<br>
        • Good internal metrics do not prove chemical generalization<br>
        • Mechanistic degradation behavior requires more than coarse global descriptors<br>
        • Demonstrating where the approach breaks down is itself a valid scientific result
        </div>
        """,
        unsafe_allow_html=True
    )

# -----------------------
# figures
# -----------------------
with tab5:
    shown_any = False

    if os.path.exists("AIC3D_v2_comparison.png"):
        st.image(
            "AIC3D_v2_comparison.png",
            caption="Effect of chemical diversity on model performance",
            use_container_width=True
        )
        shown_any = True

    if os.path.exists("AIC3D_v2_lodo_results.csv"):
        st.markdown("CSV results available in sidebar download.")
        shown_any = True

    if not shown_any:
        st.markdown(
            """
            <div class="border-box-subtle">
            Add <code>AIC3D_v2_comparison.png</code> to your repo root to display the final comparison figure here.
            </div>
            """,
            unsafe_allow_html=True
        )

# -----------------------
# conclusion
# -----------------------
with tab6:
    st.markdown('<div class="section-title">Conclusion</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="border-box">
        AIC3D shows that machine learning performance in degradation prediction depends strongly on chemical diversity.
        In heterogeneous datasets, the model relies mainly on pH; in more homogeneous datasets, structural descriptors become more informative.
        However, in both cases, Leave-One-Drug-Out validation remains weak.<br><br>

        The project’s main contribution is therefore not a high-performing predictor, but a scientifically grounded explanation of
        <b>why descriptor-based ML breaks down in small-data degradation modeling</b>.<br><br>

        This positions AIC3D as a complete exploratory research project and a foundation for future work using
        larger datasets, mechanism-aware features, or hybrid chemistry + ML approaches.
        </div>
        """,
        unsafe_allow_html=True
    )
