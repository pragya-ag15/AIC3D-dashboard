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

.hero {
    padding: 0.25rem 0 1rem 0;
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

hr {
    margin-top: 1.25rem !important;
    margin-bottom: 1.25rem !important;
}
</style>
""", unsafe_allow_html=True)


def load_csv():
    for fname in ["AIC3D_v2_results.csv", "aic3d_v2_results.csv"]:
        if os.path.exists(fname):
            return pd.read_csv(fname), fname
    return None, None


df, csv_path = load_csv()

with st.sidebar:
    st.title("AIC3D")
    st.caption("Research dashboard")

    st.markdown("### Project")
    st.markdown("[GitHub](https://github.com/pragya-ag15/AIC3D-dashboard)")
    st.markdown("[LinkedIn](https://www.linkedin.com/in/pragyaag15/)")
    st.markdown("[Email](mailto:pragyaagarwal004@gmail.com)")

    st.markdown("### Dashboard Utility")
    st.write(
        "This dashboard presents model context, validation results, figures, and downloadable outputs."
    )

    if df is not None and csv_path is not None:
        with open(csv_path, "rb") as f:
            st.download_button(
                label="Download LODO CSV",
                data=f,
                file_name=os.path.basename(csv_path),
                mime="text/csv",
                use_container_width=True,
            )

st.markdown('<div class="hero">', unsafe_allow_html=True)
st.markdown('<div class="hero-title">AIC3D</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-subtitle">AI-Catalyzed Drug Decay Detector</div>',
    unsafe_allow_html=True,
)
st.markdown(
    """
    <div class="hero-text">
    Environmental degradation prediction for pharmaceutical compounds using molecular descriptors and
    pH-dependent conditions.<br><br>
    AIC3D is a machine learning project built to estimate drug degradation behavior before environmental release.
    The system explores whether computational screening can provide earlier insight than traditional reactive
    testing alone.
    </div>
    """,
    unsafe_allow_html=True,
)
st.markdown("</div>", unsafe_allow_html=True)

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

st.divider()

st.markdown("## Key Finding")
st.markdown(
    """
    <div class="border-box">
    The model achieves strong internal performance but fails under Leave-One-Drug-Out validation.
    This indicates limited generalization across unseen drugs and shows why evaluation design matters
    in scientific machine learning.
    </div>
    """,
    unsafe_allow_html=True,
)

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    ["Overview", "Method", "Results", "Molecular Analysis", "Figures", "Conclusion"]
)

with tab1:
    c1, c2 = st.columns(2)

    with c1:
        st.markdown('<div class="section-title">Problem Context</div>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="border-box">
            Pharmaceutical compounds can enter the environment through wastewater, improper disposal,
            and incomplete treatment. Their persistence depends on molecular structure and environmental
            conditions such as pH.<br><br>
            AIC3D explores whether machine learning can estimate degradation-related behavior earlier than
            conventional testing workflows.
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown('<div class="section-title">Project Focus</div>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="border-box">
            • Predict degradation-related behavior from structure and pH<br>
            • Test whether the model generalizes to unseen drugs<br>
            • Distinguish useful chemical signal from shortcut learning
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown('<div class="section-title">Research Positioning</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="border-box-subtle">
        This dashboard is designed as a portfolio-grade research interface rather than a static summary page.
        It combines project context, validation evidence, model interpretation, visual outputs, and downloadable results.
        </div>
        """,
        unsafe_allow_html=True,
    )

with tab2:
    c1, c2 = st.columns([1, 1])

    with c1:
        st.markdown('<div class="section-title">Methodology</div>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="border-box">
            <b>Features</b><br>
            • 2048-bit Morgan fingerprints (radius = 2)<br>
            • TPSA<br>
            • logP<br>
            • Molecular Weight<br>
            • H-bond Donors<br>
            • H-bond Acceptors<br>
            • pH<br><br>

            <b>Model</b><br>
            Random Forest Regressor<br><br>

            <b>Validation Strategy</b><br>
            • 80/20 train-test split<br>
            • 5-fold cross-validation<br>
            • Leave-One-Drug-Out validation
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        if os.path.exists("project_pipeline.png"):
            st.image("project_pipeline.png", caption="AIC3D pipeline", use_container_width=True)
        else:
            st.markdown(
                """
                <div class="border-box-subtle">
                Add <code>project_pipeline.png</code> to the repo root to display the pipeline visual here.
                </div>
                """,
                unsafe_allow_html=True,
            )

with tab3:
    st.markdown('<div class="section-title">Validation Context</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="border-box">
        Internal metrics alone can overestimate real-world usefulness.
        LODO is more rigorous because each held-out drug is completely unseen during training.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section-title">Generalization Gap</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="border-box-subtle">
        AIC3D performs well on internal evaluation but drops under drug-level holdout testing.
        That gap is the most important scientific result in the project.
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns([0.95, 1.05])

    with c1:
        st.markdown('<div class="section-title">Feature Importance</div>', unsafe_allow_html=True)
        importance_df = pd.DataFrame(
            {
                "Feature": ["TPSA", "pH", "MolWt", "Other descriptors / fingerprints"],
                "Importance": [0.1104, 0.0653, 0.0042, 0.8201],
            }
        ).sort_values("Importance")
        st.bar_chart(importance_df.set_index("Feature"))

    with c2:
        st.markdown('<div class="section-title">Interpretation</div>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="border-box">
            The model appears especially sensitive to TPSA and pH.
            This is partly chemically meaningful, but LODO suggests that these signals do not generalize
            reliably across unseen compounds.
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown('<div class="section-title">LODO Results</div>', unsafe_allow_html=True)

    if df is not None:
        st.dataframe(df, use_container_width=True)

        numeric_cols = df.select_dtypes(include="number").columns.tolist()
        first_col = df.columns[0]

        preferred_col = None
        for col in ["RandomForest", "MSE", "RMSE", "R2"]:
            if col in df.columns:
                preferred_col = col
                break

        if preferred_col:
            st.markdown(f"#### {preferred_col} by Held-Out Drug")
            chart_df = df[[first_col, preferred_col]].copy().set_index(first_col)
            st.bar_chart(chart_df)
        elif numeric_cols:
            st.markdown("#### Numeric Overview")
            st.bar_chart(df.set_index(first_col)[numeric_cols])
    else:
        st.markdown(
            """
            <div class="border-box-subtle">
            <code>AIC3D_v2_results.csv</code> was not found in the repo root.
            </div>
            """,
            unsafe_allow_html=True,
        )

with tab4:
    st.markdown('<div class="section-title">Chemical Descriptor Breakdown</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="border-box">
        This section makes the model more interpretable by breaking the 2055-dimensional feature space
        into understandable groups.
        </div>
        """,
        unsafe_allow_html=True,
    )

    descriptor_df = pd.DataFrame(
        {
            "Descriptor Group": [
                "Morgan Fingerprints",
                "TPSA",
                "logP",
                "Molecular Weight",
                "H-bond Donors",
                "H-bond Acceptors",
                "pH",
            ],
            "Role in Model": [
                "Encodes structural subpatterns across the molecule",
                "Captures polar surface behavior",
                "Represents hydrophobicity / partitioning tendency",
                "Represents molecular size",
                "Captures hydrogen-bond donation capacity",
                "Captures hydrogen-bond acceptance capacity",
                "Represents environmental condition affecting degradation",
            ],
            "Feature Count": [2048, 1, 1, 1, 1, 1, 1],
        }
    )
    st.dataframe(descriptor_df, use_container_width=True, hide_index=True)

with tab5:
    figure_list = [
        ("problem_context.png", "Project context"),
        ("project_pipeline.png", "Pipeline"),
        ("feature_importance.png", "Feature importance"),
        ("lodo_results_plot.png", "LODO performance"),
        ("summary_metrics.png", "Summary metrics"),
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
        st.markdown(
            """
            <div class="border-box-subtle">
            No figure files were found in the repo root.
            </div>
            """,
            unsafe_allow_html=True,
        )

with tab6:
    st.markdown('<div class="section-title">Conclusion</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="border-box">
        AIC3D demonstrates that molecular descriptors and environmental variables can capture degradation-related patterns.
        However, Leave-One-Drug-Out evaluation shows that these patterns do not generalize reliably across unseen compounds.<br><br>

        The project's strongest contribution is methodological honesty: strong internal metrics alone are not sufficient
        to validate predictive systems in chemistry.<br><br>

        This positions AIC3D as a complete and transparent research prototype rather than an overclaimed predictive tool.
        </div>
        """,
        unsafe_allow_html=True,
    )
