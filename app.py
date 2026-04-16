import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="AIC3D Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# STYLE
# -----------------------------
st.markdown("""
<style>
.block-container {
    max-width: 1280px;
    padding-top: 1.4rem;
    padding-bottom: 3rem;
}
.main-title {
    font-size: 3.1rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    margin-bottom: 0.15rem;
}
.sub-title {
    font-size: 1.08rem;
    opacity: 0.9;
    margin-bottom: 1rem;
    line-height: 1.6;
}
.card {
    border: 1px solid rgba(148,163,184,0.22);
    border-radius: 18px;
    padding: 1rem 1.1rem;
    margin-bottom: 1rem;
    background: rgba(255,255,255,0.02);
}
.section-head {
    font-size: 1.18rem;
    font-weight: 700;
    margin-bottom: 0.7rem;
}
[data-testid="stMetric"] {
    border: 1px solid rgba(148,163,184,0.22);
    border-radius: 18px;
    padding: 0.8rem;
}
.small-note {
    font-size: 0.92rem;
    opacity: 0.85;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# DATA (embedded so the app always works)
# -----------------------------
summary_df = pd.DataFrame({
    "Experiment": ["Experiment 1: Diverse drugs", "Experiment 2: NSAIDs (similar class)"],
    "Points": [9, 17],
    "Dominant Signal": ["pH", "Structure"],
    "RF Train/Test R²": [0.7641, 0.9158],
    "RF CV R²": [-21.2320, 0.7157],
    "RF Overall LODO R²": [-0.0677, 0.2327],
})

metrics_df = pd.DataFrame({
    "Experiment": [
        "Experiment 1: Diverse drugs", "Experiment 1: Diverse drugs",
        "Experiment 2: NSAIDs (similar class)", "Experiment 2: NSAIDs (similar class)"
    ],
    "Model": ["LinearRegression", "RandomForest", "LinearRegression", "RandomForest"],
    "Train/Test MSE": [2.7993, 1.2857, 0.1886, 0.1394],
    "Train/Test R²": [0.4864, 0.7641, 0.8861, 0.9158],
    "CV MSE": [15.3486, 7.0386, 0.5369, 0.6231],
    "CV R²": [-48.1190, -21.2320, 0.7479, 0.7157],
    "Overall LODO MSE": [10.0565, 6.1455, 0.5762, 1.6936],
    "Overall LODO MAE": [2.6873, 1.8463, 0.5944, 1.0000],
    "Overall LODO R²": [-0.7472, -0.0677, 0.7389, 0.2327]
})

lodo_df = pd.DataFrame({
    "Experiment": [
        "Experiment 1: Diverse drugs","Experiment 1: Diverse drugs","Experiment 1: Diverse drugs",
        "Experiment 1: Diverse drugs","Experiment 1: Diverse drugs","Experiment 1: Diverse drugs",
        "Experiment 2: NSAIDs (similar class)","Experiment 2: NSAIDs (similar class)",
        "Experiment 2: NSAIDs (similar class)","Experiment 2: NSAIDs (similar class)",
        "Experiment 2: NSAIDs (similar class)","Experiment 2: NSAIDs (similar class)",
        "Experiment 2: NSAIDs (similar class)","Experiment 2: NSAIDs (similar class)",
        "Experiment 2: NSAIDs (similar class)","Experiment 2: NSAIDs (similar class)"
    ],
    "Model": [
        "LinearRegression","LinearRegression","LinearRegression",
        "RandomForest","RandomForest","RandomForest",
        "LinearRegression","LinearRegression","LinearRegression","LinearRegression","LinearRegression",
        "RandomForest","RandomForest","RandomForest","RandomForest","RandomForest"
    ],
    "Drug": [
        "Amoxicillin","Clarithromycin","Trimethoprim",
        "Amoxicillin","Clarithromycin","Trimethoprim",
        "Aspirin","Diclofenac","Ibuprofen","Naproxen","Paracetamol",
        "Aspirin","Diclofenac","Ibuprofen","Naproxen","Paracetamol"
    ],
    "MSE": [
        3.6854,19.7479,6.7362,
        1.3179,15.9342,1.1844,
        0.4261,0.3236,0.2148,0.1226,1.6285,
        0.5717,0.3397,0.1058,0.9583,5.5348
    ],
    "MAE": [
        1.3372,4.2314,2.4933,
        0.8282,3.7594,0.9511,
        0.6431,0.4946,0.4069,0.3262,1.0785,
        0.7521,0.5384,0.2736,0.9013,2.2292
    ],
    "R2": [
        -3.1135,-0.6313,-11.3208,
        -0.4709,-0.3162,-1.1664,
        -37.2554,-0.3102,-14.6489,-1.9776,-2.5498,
        -50.3268,-0.3752,-6.7072,-22.2688,-11.0646
    ]
})

feature_df = pd.DataFrame({
    "Experiment": ["Experiment 1: Diverse drugs"]*6 + ["Experiment 2: NSAIDs (similar class)"]*6,
    "Feature": ["pH","LogP","MW","TPSA","HBA","HBD","MW","HBD","TPSA","pH","LogP","HBA"],
    "Importance": [0.622647,0.115581,0.103378,0.088683,0.066999,0.002712,
                   0.458990,0.285239,0.115907,0.067660,0.067236,0.004968]
})

expert_df = pd.DataFrame({
    "Source": [
        "EPA cheminformatics expert",
        "Biodegradation researcher",
        "Environmental chemistry expert",
        "Laura Carter"
    ],
    "Takeaway": [
        "Dataset too small and chemically heterogeneous for meaningful generalizable ML.",
        "Very small datasets cannot support reliable structure–activity learning; leakage and scale matter.",
        "Dataset too small for a meaningful predictive model.",
        "Simple global descriptors are a useful baseline, but they miss mechanism-specific degradation across diverse classes."
    ]
})

# -----------------------------
# SIDEBAR
# -----------------------------
with st.sidebar:
    st.title("AIC3D")
    st.caption("Interactive research dashboard")

    experiments = summary_df["Experiment"].tolist()
    selected_experiment = st.selectbox("Choose experiment", experiments)

    models = metrics_df["Model"].tolist()
    model_options = sorted(metrics_df["Model"].unique().tolist())
    selected_model = st.selectbox("Choose model", model_options, index=model_options.index("RandomForest"))

    st.markdown("### Links")
    st.markdown("[GitHub](https://github.com/pragya-ag15/AIC3D-dashboard)")
    st.markdown("[LinkedIn](https://www.linkedin.com/in/pragyaag15/)")
    st.markdown("[Email](mailto:pragyaagarwal004@gmail.com)")

# -----------------------------
# FILTERS
# -----------------------------
curr_summary = summary_df[summary_df["Experiment"] == selected_experiment].iloc[0]
curr_metrics = metrics_df[
    (metrics_df["Experiment"] == selected_experiment) &
    (metrics_df["Model"] == selected_model)
].iloc[0]
curr_lodo = lodo_df[
    (lodo_df["Experiment"] == selected_experiment) &
    (lodo_df["Model"] == selected_model)
].copy()
curr_features = feature_df[feature_df["Experiment"] == selected_experiment].copy()

# -----------------------------
# HERO
# -----------------------------
st.markdown('<div class="main-title">AIC3D</div>', unsafe_allow_html=True)
st.markdown(
    """
    <div class="sub-title">
    AI-Catalyzed Drug Degradation Detector — an exploratory machine learning project testing whether
    simple molecular descriptors and pH can predict pharmaceutical degradation behavior, and where that approach breaks down.
    </div>
    """,
    unsafe_allow_html=True
)

hero1, hero2 = st.columns([1.3, 1])

with hero1:
    st.markdown("""
    <div class="card">
    <b>Research question</b><br><br>
    Can simple molecular descriptors and environmental pH predict degradation behavior in a way that generalizes to unseen compounds?
    <br><br>
    <b>Final insight:</b> models learn useful patterns within constrained settings, but robust cross-compound generalization remains weak.
    </div>
    """, unsafe_allow_html=True)

with hero2:
    st.markdown("""
    <div class="card">
    <b>What makes this a project, not just a showcase</b><br><br>
    • two-experiment comparison<br>
    • rigorous validation with LODO<br>
    • feature analysis<br>
    • interpretation of failure<br>
    • external expert feedback
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# METRICS
# -----------------------------
m1, m2, m3, m4 = st.columns(4)
m1.metric("Points", int(curr_summary["Points"]))
m2.metric("Dominant signal", curr_summary["Dominant Signal"])
m3.metric("Train/Test R²", f"{curr_metrics['Train/Test R²']:.3f}")
m4.metric("CV R²", f"{curr_metrics['CV R²']:.3f}")

m5, m6, m7, m8 = st.columns(4)
m5.metric("Overall LODO R²", f"{curr_metrics['Overall LODO R²']:.3f}")
m6.metric("Overall LODO MAE", f"{curr_metrics['Overall LODO MAE']:.3f}")
m7.metric("Model", selected_model)
m8.metric("Experiment", "Diverse" if "Diverse" in selected_experiment else "Similar-class")

st.divider()

# -----------------------------
# MAIN TABS
# -----------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Overview", "Validation", "Features", "Expert Feedback", "Project Data"
])

with tab1:
    c1, c2 = st.columns([1, 1])

    with c1:
        st.markdown("### Why two experiments?")
        st.markdown("""
        The project compares a **chemically diverse** dataset against a **chemically similar** one.
        This makes it possible to test whether model performance changes with chemical diversity.
        """)

        st.markdown("### Experiment logic")
        if "Diverse" in selected_experiment:
            st.markdown("""
            <div class="card">
            <b>Experiment 1 — Diverse drugs</b><br><br>
            Drugs: Amoxicillin, Clarithromycin, Trimethoprim<br>
            Purpose: test whether descriptor-based ML can generalize across very different compounds.<br><br>
            Result: pH dominates and generalization remains weak.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="card">
            <b>Experiment 2 — Similar-class drugs</b><br><br>
            Drugs: Aspirin, Diclofenac, Ibuprofen, Naproxen, Paracetamol<br>
            Purpose: test whether models perform better within a more chemically related space.<br><br>
            Result: internal performance improves, but held-out generalization is still fragile.
            </div>
            """, unsafe_allow_html=True)

    with c2:
        evolution = pd.DataFrame({
            "Stage": ["Initial success", "Better validation", "Diverse drugs", "Similar-class drugs", "Final conclusion"],
            "Value": [0.97, -0.75, -0.07, 0.23, 1.0],
            "Label": [
                "High internal score",
                "LODO exposed overfitting",
                "pH-dominated",
                "Structure mattered more",
                "Generalization still limited"
            ]
        })
        fig_story = px.line(
            evolution, x="Stage", y="Value", markers=True, text="Label",
            title="How the project evolved"
        )
        fig_story.update_traces(textposition="top center")
        fig_story.update_layout(height=420)
        st.plotly_chart(fig_story, use_container_width=True)

    compare_long = summary_df.melt(
        id_vars=["Experiment"],
        value_vars=["RF Train/Test R²", "RF CV R²", "RF Overall LODO R²"],
        var_name="Metric",
        value_name="Value"
    )
    fig_compare = px.bar(
        compare_long,
        x="Metric",
        y="Value",
        color="Experiment",
        barmode="group",
        title="Random Forest comparison across evaluation settings"
    )
    fig_compare.update_layout(height=430)
    st.plotly_chart(fig_compare, use_container_width=True)

with tab2:
    left, right = st.columns(2)

    with left:
        fig_r2 = px.bar(
            curr_lodo,
            x="Drug",
            y="R2",
            color="R2",
            color_continuous_scale="RdYlGn",
            title=f"{selected_model} — LODO R² by held-out drug"
        )
        fig_r2.add_hline(y=0, line_dash="dash")
        fig_r2.update_layout(height=430)
        st.plotly_chart(fig_r2, use_container_width=True)

    with right:
        err_df = curr_lodo.melt(
            id_vars=["Experiment", "Model", "Drug"],
            value_vars=["MSE", "MAE"],
            var_name="Metric",
            value_name="Value"
        )
        fig_err = px.bar(
            err_df,
            x="Drug",
            y="Value",
            color="Metric",
            barmode="group",
            title=f"{selected_model} — LODO error profile"
        )
        fig_err.update_layout(height=430)
        st.plotly_chart(fig_err, use_container_width=True)

    if "Diverse" in selected_experiment:
        st.warning(
            "In the diverse-drug setting, internal metrics are much weaker and LODO remains negative. "
            "This suggests the model cannot transfer across mechanistically different compounds."
        )
    else:
        st.info(
            "In the similar-class setting, train/test and CV improve substantially. "
            "But LODO is still weak for most held-out drugs, so the model is not a robust unseen-drug predictor."
        )

with tab3:
    a, b = st.columns([1, 1])

    with a:
        fig_feat = px.bar(
            curr_features.sort_values("Importance", ascending=False),
            x="Feature",
            y="Importance",
            color="Importance",
            color_continuous_scale="Blues",
            title=f"{selected_experiment} — Feature importance"
        )
        fig_feat.update_layout(height=430)
        st.plotly_chart(fig_feat, use_container_width=True)

    with b:
        desc_df = pd.DataFrame({
            "Feature": ["LogP", "MW", "HBD", "HBA", "TPSA", "pH"],
            "Meaning": [
                "Hydrophobicity",
                "Molecular size",
                "Hydrogen bond donor count",
                "Hydrogen bond acceptor count",
                "Polar surface area",
                "Environmental acidity/basicity"
            ]
        })
        st.dataframe(desc_df, use_container_width=True, hide_index=True)

    if "Diverse" in selected_experiment:
        st.markdown("""
        <div class="card">
        <b>Interpretation:</b> In the diverse dataset, <b>pH dominates</b>. The model seems to rely more on the environmental variable
        than on learning a transferable structural rule across very different drug classes.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="card">
        <b>Interpretation:</b> In the similar-class dataset, <b>structural descriptors matter more</b>.
        That suggests the model can learn local structure–activity relationships inside a constrained chemical space.
        </div>
        """, unsafe_allow_html=True)

with tab4:
    st.markdown("### External validation")
    cols = st.columns(2)
    for i, row in expert_df.iterrows():
        with cols[i % 2]:
            st.markdown(
                f"""
                <div class="card">
                <b>{row['Source']}</b><br><br>
                {row['Takeaway']}
                </div>
                """,
                unsafe_allow_html=True
            )

    st.success(
        "The expert feedback strengthened the project. It confirmed that the observed limitations are scientifically meaningful, not just technical problems."
    )

with tab5:
    st.markdown("### Held-out results table")
    st.dataframe(curr_lodo, use_container_width=True)

    st.markdown("### Experiment summary")
    st.dataframe(summary_df, use_container_width=True, hide_index=True)

    with st.expander("Show full metrics"):
        st.dataframe(metrics_df, use_container_width=True, hide_index=True)

    csv_data = lodo_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download all LODO results as CSV",
        csv_data,
        file_name="AIC3D_v2_lodo_both.csv",
        mime="text/csv"
    )
