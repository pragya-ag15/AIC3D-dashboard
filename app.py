import os
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
    max-width: 1250px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}
.big-title {
    font-size: 3.2rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    margin-bottom: 0.2rem;
}
.sub-title {
    font-size: 1.05rem;
    opacity: 0.9;
    margin-bottom: 1rem;
}
.info-card {
    border: 1px solid rgba(148,163,184,0.25);
    border-radius: 18px;
    padding: 1rem 1.1rem;
    margin-bottom: 1rem;
    background: rgba(255,255,255,0.02);
}
.section-head {
    font-size: 1.2rem;
    font-weight: 700;
    margin-top: 0.4rem;
    margin-bottom: 0.75rem;
}
.small-note {
    font-size: 0.92rem;
    opacity: 0.85;
}
[data-testid="stMetric"] {
    border: 1px solid rgba(148,163,184,0.25);
    border-radius: 18px;
    padding: 0.8rem;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# LOAD DATA
# -----------------------------
def load_csv(name):
    return pd.read_csv(name) if os.path.exists(name) else None

lodo_df = load_csv("AIC3D_v2_lodo_both.csv")
summary_df = load_csv("AIC3D_v2_summary.csv")
feature_df = load_csv("AIC3D_v2_feature_importance.csv")
metrics_df = load_csv("AIC3D_v2_metrics.csv")

# -----------------------------
# FALLBACK DATA (if files missing)
# -----------------------------
if lodo_df is None:
    lodo_df = pd.DataFrame({
        "Experiment": [
            "Experiment 1: Diverse drugs","Experiment 1: Diverse drugs","Experiment 1: Diverse drugs",
            "Experiment 2: NSAIDs (similar class)","Experiment 2: NSAIDs (similar class)",
            "Experiment 2: NSAIDs (similar class)","Experiment 2: NSAIDs (similar class)",
            "Experiment 2: NSAIDs (similar class)"
        ],
        "Model": ["RandomForest"]*8,
        "Drug": ["Amoxicillin","Clarithromycin","Trimethoprim","Aspirin","Diclofenac","Ibuprofen","Naproxen","Paracetamol"],
        "MSE": [1.3179,15.9342,1.1844,0.5717,0.3397,0.1058,0.9583,5.5348],
        "MAE": [0.8282,3.7594,0.9511,0.7521,0.5384,0.2736,0.9013,2.2292],
        "R2": [-0.4709,-0.3162,-1.1664,-50.3268,-0.3752,-6.7072,-22.2688,-11.0646]
    })

if summary_df is None:
    summary_df = pd.DataFrame({
        "Experiment": ["Experiment 1: Diverse drugs", "Experiment 2: NSAIDs (similar class)"],
        "TrainTest_RF_R2": [0.7641, 0.9158],
        "CV_RF_R2": [-21.2320, 0.7157],
        "LODO_RF_R2": [-0.0677, 0.2327],
        "Points": [9, 17],
        "DominantSignal": ["pH", "Structure"]
    })

if feature_df is None:
    feature_df = pd.DataFrame({
        "Experiment": ["Experiment 1: Diverse drugs"]*6 + ["Experiment 2: NSAIDs (similar class)"]*6,
        "Feature": ["pH","LogP","MW","TPSA","HBA","HBD","MW","HBD","TPSA","pH","LogP","HBA"],
        "Importance": [0.622647,0.115581,0.103378,0.088683,0.066999,0.002712,
                       0.458990,0.285239,0.115907,0.067660,0.067236,0.004968]
    })

if metrics_df is None:
    metrics_df = pd.DataFrame({
        "Experiment": [
            "Experiment 1: Diverse drugs","Experiment 1: Diverse drugs",
            "Experiment 2: NSAIDs (similar class)","Experiment 2: NSAIDs (similar class)"
        ],
        "Model": ["LinearRegression","RandomForest","LinearRegression","RandomForest"],
        "TrainTest_MSE": [2.7993,1.2857,0.1886,0.1394],
        "TrainTest_R2": [0.4864,0.7641,0.8861,0.9158],
        "CV_MSE": [15.3486,7.0386,0.5369,0.6231],
        "CV_R2": [-48.1190,-21.2320,0.7479,0.7157],
        "LODO_MSE_Overall": [10.0565,6.1455,0.5762,1.6936],
        "LODO_MAE_Overall": [2.6873,1.8463,0.5944,1.0000],
        "LODO_R2_Overall": [-0.7472,-0.0677,0.7389,0.2327]
    })

# -----------------------------
# SIDEBAR
# -----------------------------
with st.sidebar:
    st.title("AIC3D")
    st.caption("Interactive research dashboard")

    st.markdown("### Filters")
    experiment_options = sorted(lodo_df["Experiment"].unique().tolist())
    selected_experiment = st.selectbox("Experiment", experiment_options)

    model_options = sorted(metrics_df["Model"].unique().tolist())
    selected_model = st.selectbox("Model", model_options, index=model_options.index("RandomForest") if "RandomForest" in model_options else 0)

    st.markdown("### Links")
    st.markdown("[GitHub](https://github.com/pragya-ag15/AIC3D-dashboard)")
    st.markdown("[LinkedIn](https://www.linkedin.com/in/pragyaag15/)")
    st.markdown("[Email](mailto:pragyaagarwal004@gmail.com)")

    if os.path.exists("AIC3D_v2_lodo_both.csv"):
        with open("AIC3D_v2_lodo_both.csv", "rb") as f:
            st.download_button(
                "Download LODO CSV",
                f,
                file_name="AIC3D_v2_lodo_both.csv",
                mime="text/csv",
                use_container_width=True
            )

# -----------------------------
# FILTERED DATA
# -----------------------------
curr_lodo = lodo_df[(lodo_df["Experiment"] == selected_experiment) & (lodo_df["Model"] == selected_model)].copy()
curr_metrics = metrics_df[(metrics_df["Experiment"] == selected_experiment) & (metrics_df["Model"] == selected_model)].copy()
curr_features = feature_df[feature_df["Experiment"] == selected_experiment].copy()

selected_summary = summary_df[summary_df["Experiment"] == selected_experiment].iloc[0]

# -----------------------------
# HERO
# -----------------------------
st.markdown('<div class="big-title">AIC3D</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">AI-Catalyzed Drug Degradation Detector — an exploratory ML project on hydrolysis prediction, generalization, and why simple descriptor models break down.</div>',
    unsafe_allow_html=True
)

c1, c2 = st.columns([1.3, 1])

with c1:
    st.markdown("""
    <div class="info-card">
    <b>Core research question</b><br><br>
    Can simple molecular descriptors and environmental pH predict pharmaceutical degradation behavior in a way that generalizes to unseen compounds?
    <br><br>
    <b>Final answer:</b> only partially within constrained chemical spaces — and not robustly across drug classes.
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="info-card">
    <b>What makes this a research project</b><br><br>
    • two-experiment comparison<br>
    • multiple validation strategies<br>
    • explicit generalization testing with LODO<br>
    • feature interpretation<br>
    • external expert feedback
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# METRICS
# -----------------------------
m1, m2, m3, m4 = st.columns(4)
m1.metric("Experiment", "Diverse" if "Diverse" in selected_experiment else "Similar-class")
m2.metric("Points", int(selected_summary["Points"]))
m3.metric("Dominant signal", selected_summary["DominantSignal"])
m4.metric("Main framing", "Generalization limit")

if not curr_metrics.empty:
    row = curr_metrics.iloc[0]
    m5, m6, m7, m8 = st.columns(4)
    m5.metric("Train/Test R²", f"{row['TrainTest_R2']:.3f}")
    m6.metric("CV R²", f"{row['CV_R2']:.3f}")
    m7.metric("Overall LODO R²", f"{row['LODO_R2_Overall']:.3f}")
    m8.metric("Overall LODO MAE", f"{row['LODO_MAE_Overall']:.3f}")

st.divider()

# -----------------------------
# TABS
# -----------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Research Story", "Validation", "Feature Analysis", "Expert Feedback", "Data"
])

# -----------------------------
# TAB 1
# -----------------------------
with tab1:
    a, b = st.columns([1, 1])

    with a:
        st.markdown("### Why this project exists")
        st.markdown("""
        Pharmaceutical compounds can persist in the environment depending on structure and conditions like pH.
        AIC3D explores whether computational screening can provide useful early insight into degradation behavior.
        """)

        st.markdown("### Why two experiments?")
        st.markdown("""
        The project compares:
        - **Experiment 1:** chemically diverse drugs
        - **Experiment 2:** chemically similar drugs

        This makes the project stronger because it tests whether model behavior changes with chemical diversity.
        """)

    with b:
        story_fig = go.Figure()
        story_fig.add_trace(go.Scatter(
            x=["Initial model", "Better validation", "Diverse dataset", "Similar-class dataset", "Final insight"],
            y=[0.97, -1.0, -0.07, 0.23, 1.0],
            mode="lines+markers+text",
            text=["High internal score", "LODO exposed issue", "pH dominated", "Structure mattered more", "Generalization still weak"],
            textposition="top center"
        ))
        story_fig.update_layout(
            title="How the project evolved",
            xaxis_title="Project stage",
            yaxis_title="Interpretive progression",
            height=420
        )
        st.plotly_chart(story_fig, use_container_width=True)

    st.markdown("### Final takeaway")
    st.info(
        "AIC3D is valuable not because it produced a fully successful predictor, "
        "but because it showed where descriptor-based ML works, where it fails, and why."
    )

# -----------------------------
# TAB 2
# -----------------------------
with tab2:
    left, right = st.columns([1.1, 1])

    with left:
        st.markdown("### Held-out drug performance")
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
        st.markdown("### Error profile")
        fig_err = px.bar(
            curr_lodo.melt(id_vars=["Experiment", "Model", "Drug"], value_vars=["MSE", "MAE"], var_name="Metric", value_name="Value"),
            x="Drug",
            y="Value",
            color="Metric",
            barmode="group",
            title=f"{selected_model} — LODO error by held-out drug"
        )
        fig_err.update_layout(height=430)
        st.plotly_chart(fig_err, use_container_width=True)

    st.markdown("### Experiment comparison")
    compare_long = summary_df.melt(
        id_vars=["Experiment"],
        value_vars=["TrainTest_RF_R2", "CV_RF_R2", "LODO_RF_R2"],
        var_name="Metric",
        value_name="Value"
    )
    fig_compare = px.bar(
        compare_long,
        x="Metric",
        y="Value",
        color="Experiment",
        barmode="group",
        title="Random Forest performance across evaluation settings"
    )
    fig_compare.update_layout(height=420)
    st.plotly_chart(fig_compare, use_container_width=True)

    st.markdown("### Interpretation")
    if "Diverse" in selected_experiment:
        st.warning(
            "In the diverse-drug setting, performance collapses under CV and LODO. "
            "This suggests the model cannot transfer across mechanistically different compounds."
        )
    else:
        st.success(
            "In the similar-class setting, internal metrics improve, showing the model can learn within-class patterns. "
            "But LODO remains weak, so true held-out generalization is still limited."
        )

# -----------------------------
# TAB 3
# -----------------------------
with tab3:
    c1, c2 = st.columns([1, 1])

    with c1:
        st.markdown("### Feature importance")
        fig_feat = px.bar(
            curr_features.sort_values("Importance", ascending=False),
            x="Feature",
            y="Importance",
            color="Importance",
            color_continuous_scale="Blues",
            title=f"{selected_experiment} — feature importance"
        )
        fig_feat.update_layout(height=430)
        st.plotly_chart(fig_feat, use_container_width=True)

    with c2:
        st.markdown("### What the features mean")
        descriptor_df = pd.DataFrame({
            "Feature": ["LogP", "MW", "HBD", "HBA", "TPSA", "pH"],
            "Meaning": [
                "Hydrophobicity / partitioning tendency",
                "Molecular size",
                "Hydrogen bond donor count",
                "Hydrogen bond acceptor count",
                "Topological polar surface area",
                "Environmental acidity/basicity"
            ]
        })
        st.dataframe(descriptor_df, use_container_width=True, hide_index=True)

    st.markdown("### Key pattern")
    if "Diverse" in selected_experiment:
        st.markdown("""
        <div class="info-card">
        In the diverse dataset, <b>pH dominates</b>. That suggests the model is leaning on the environmental variable
        rather than learning a transferable structural rule across very different drug classes.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="info-card">
        In the similar-class dataset, <b>structural descriptors dominate more strongly</b>. That suggests the model
        can learn local structure–activity relationships within a constrained chemical space.
        </div>
        """, unsafe_allow_html=True)

# -----------------------------
# TAB 4
# -----------------------------
with tab4:
    st.markdown("### What external feedback added")

    feedback_cards = [
        ("EPA cheminformatics expert",
         "The dataset is far too small and chemically heterogeneous for meaningful generalizable modeling."),
        ("Biodegradation researcher",
         "Very small datasets cannot support reliable structure–activity learning; leakage and data scale matter."),
        ("Environmental chemistry expert",
         "The dataset is too small for a meaningful predictive model."),
        ("Laura Carter",
         "Simple global descriptors can be a useful baseline, but they do not capture mechanism-specific degradation across diverse classes.")
    ]

    cols = st.columns(2)
    for i, (who, msg) in enumerate(feedback_cards):
        with cols[i % 2]:
            st.markdown(
                f"""
                <div class="info-card">
                <b>{who}</b><br><br>
                {msg}
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("### Synthesis")
    st.info(
        "The expert feedback did not contradict the project — it strengthened it. "
        "It confirmed that the observed failure is data-driven and mechanistically meaningful, not just a coding issue."
    )

# -----------------------------
# TAB 5
# -----------------------------
with tab5:
    st.markdown("### LODO results table")
    st.dataframe(curr_lodo, use_container_width=True)

    st.markdown("### Full experiment summary")
    st.dataframe(summary_df, use_container_width=True, hide_index=True)

    with st.expander("Show full metrics table"):
        st.dataframe(metrics_df, use_container_width=True, hide_index=True)

    st.markdown("### Suggested article angle")
    st.markdown("""
    - Initial high scores were misleading  
    - Better validation changed the conclusion  
    - Chemical diversity changed what the model learned  
    - Expert feedback confirmed the interpretation  
    - The project became stronger because it explained failure honestly
    """)
