import os
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="AIC3D Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------
# Minimal styling only
# -----------------------------------
st.markdown("""
<style>
.block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}
[data-testid="stMetricValue"] {
    font-size: 1.15rem !important;
    line-height: 1.2 !important;
}
[data-testid="stMetricLabel"] {
    font-size: 0.82rem !important;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------------
# Helpers
# -----------------------------------
def load_csv():
    for fname in ["AIC3D_v2_results.csv", "aic3d_v2_results.csv"]:
        if os.path.exists(fname):
            return pd.read_csv(fname), fname
    return None, None

def show_img(fname, caption=None):
    if os.path.exists(fname):
        st.image(fname, caption=caption, use_container_width=True)

df, csv_path = load_csv()

# -----------------------------------
# Sidebar
# -----------------------------------
with st.sidebar:
    st.title("AIC3D")
    st.caption("Research dashboard")

    st.markdown("### Project")
    st.markdown("[GitHub](https://github.com/pragya-ag15/AIC3D-dashboard)")
    st.markdown("[LinkedIn](https://www.linkedin.com/in/pragyaag15/)")
    st.markdown("[Email](mailto:pragyaagarwal004@gmail.com)")

    st.markdown("### Dashboard Utility")
    st.write("This dashboard presents model context, validation results, figures, and downloadable outputs.")

    if df is not None and csv_path is not None:
        with open(csv_path, "rb") as f:
            st.download_button(
                label="Download LODO CSV",
                data=f,
                file_name=os.path.basename(csv_path),
                mime="text/csv",
                use_container_width=True
            )

# -----------------------------------
# Header
# -----------------------------------
st.title("AIC3D")
st.subheader("AI-Catalyzed Drug Decay Detector")
st.write(
    "Environmental degradation prediction for pharmaceutical compounds using molecular descriptors and pH-dependent conditions."
)

st.write(
    "AIC3D is a machine learning project built to estimate drug degradation behavior before environmental release. "
    "The system explores whether computational screening can provide earlier insight than traditional reactive testing alone."
)

# -----------------------------------
# Top metrics
# -----------------------------------
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

# -----------------------------------
# Key finding
# -----------------------------------
st.markdown("## Key Finding")
st.info(
    "The model achieves strong internal performance but fails under Leave-One-Drug-Out validation. "
    "This indicates limited generalization across unseen drugs and shows why evaluation design matters in scientific machine learning."
)

# -----------------------------------
# Tabs
# -----------------------------------
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Overview",
    "Method",
    "Results",
    "Molecular Analysis",
    "Figures",
    "Conclusion"
])

# -----------------------------------
# Overview
# -----------------------------------
with tab1:
    c1, c2 = st.columns(2)

    with c1:
        st.markdown("### Problem Context")
        st.write(
            "Pharmaceutical compounds can enter the environment through wastewater, disposal, and incomplete treatment. "
            "Their persistence depends on molecular structure and environmental conditions such as pH."
        )
        st.write(
            "AIC3D explores whether machine learning can estimate degradation-related behavior earlier than conventional testing workflows."
        )

    with c2:
        st.markdown("### Project Focus")
        st.write("• Predict degradation-related behavior from structure and pH")
        st.write("• Test whether the model generalizes to unseen drugs")
        st.write("• Distinguish useful chemical signal from shortcut learning")

    st.markdown("### Research Positioning")
    st.write(
        "This dashboard is intended as a portfolio-grade research interface rather than a static summary page. "
        "It combines project context, validation evidence, model interpretation, visual outputs, and downloadable results."
    )

# -----------------------------------
# Method
# -----------------------------------
with tab2:
    c1, c2 = st.columns([1, 1])

    with c1:
        st.markdown("### Feature Construction")
        st.write("• 2048-bit Morgan fingerprints (radius = 2)")
        st.write("• TPSA")
        st.write("• logP")
        st.write("• Molecular Weight")
        st.write("• H-bond Donors")
        st.write("• H-bond Acceptors")
        st.write("• pH")

        st.markdown("### Model")
        st.write("Random Forest Regressor")

        st.markdown("### Validation Strategy")
        st.write("• 80/20 train-test split")
        st.write("• 5-fold cross-validation")
        st.write("• Leave-One-Drug-Out validation")

    with c2:
        show_img("project_pipeline.png", "AIC3D pipeline")
        if not os.path.exists("project_pipeline.png"):
            st.caption("Add project_pipeline.png to the repo root to show the pipeline visual here.")

# -----------------------------------
# Results
# -----------------------------------
with tab3:
    st.markdown("### Validation Context")
    st.warning(
        "Internal metrics alone can overestimate real-world usefulness. "
        "LODO is more rigorous because each held-out drug is completely unseen during training."
    )

    st.markdown("### Generalization Gap")
    st.write(
        "AIC3D performs well on internal evaluation but drops under drug-level holdout testing. "
        "That gap is the most important scientific result in the project."
    )

    c1, c2 = st.columns([0.95, 1.05])

    with c1:
        st.markdown("### Feature Importance")
        importance_df = pd.DataFrame({
            "Feature": ["TPSA", "pH", "MolWt", "Other descriptors / fingerprints"],
            "Importance": [0.1104, 0.0653, 0.0042, 0.8201]
        }).sort_values("Importance")
        st.bar_chart(importance_df.set_index("Feature"))

    with c2:
        st.markdown("### Interpretation")
        st.write(
            "The model appears especially sensitive to TPSA and pH. "
            "This is partly chemically meaningful, but LODO suggests that these signals do not generalize reliably across unseen compounds."
        )

    st.markdown("### LODO Results")
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
            st.markdown(f"### {preferred_col} by Held-Out Drug")
            chart_df = df[[first_col, preferred_col]].copy().set_index(first_col)
            st.bar_chart(chart_df)
        elif numeric_cols:
            st.markdown("### Numeric Overview")
            st.bar_chart(df.set_index(first_col)[numeric_cols])
    else:
        st.error("AIC3D_v2_results.csv was not found in the repo root.")

# -----------------------------------
# Molecular Analysis
# -----------------------------------
with tab4:
    st.markdown("### Chemical Descriptor Breakdown")
    st.write(
        "This section makes the model more interpretable by breaking the 2055-dimensional feature space into understandable groups."
    )

    descriptor_df = pd.DataFrame({
        "Descriptor Group": [
            "Morgan Fingerprints",
            "TPSA",
            "logP",
            "Molecular Weight",
            "H-bond Donors",
            "H-bond Acceptors",
            "pH"
        ],
        "Role in Model": [
            "Encodes structural subpatterns across the molecule",
            "Captures polar surface behavior",
            "Represents hydrophobicity / partitioning tendency",
            "Represents molecular size",
            "Captures hydrogen-bond donation capacity",
            "Captures hydrogen-bond acceptance capacity",
            "Represents environmental condition affecting degradation"
        ],
        "Feature Count": [2048, 1, 1, 1, 1, 1, 1]
    })

    st.dataframe(descriptor_df, use_container_width=True, hide_index=True)

    st.info(
        "This descriptor view helps reduce the 'black box' effect by showing how structural fingerprints and classical chemical properties combine inside the model."
    )

# -----------------------------------
# Figures
# -----------------------------------
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
        st.info("No figure files were found in the repo root.")

# -----------------------------------
# Conclusion
# -----------------------------------
with tab6:
    st.markdown("### Conclusion")
    st.write(
        "AIC3D demonstrates that molecular descriptors and environmental variables can capture degradation-related patterns. "
        "However, Leave-One-Drug-Out evaluation shows that these patterns do not generalize reliably across unseen compounds."
    )
    st.write(
        "The project’s strongest contribution is methodological honesty: strong internal metrics alone are not sufficient "
        "to validate predictive systems in chemistry."
    )
    st.write(
        "This positions AIC3D as a complete and transparent research prototype rather than an overclaimed predictive tool."
    )
