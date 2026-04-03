import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="AIC3D Dashboard", layout="wide")

# ----------------------------
# Helper functions
# ----------------------------
def show_image_if_exists(path, caption):
    if os.path.exists(path):
        st.image(path, caption=caption, use_container_width=True)
    else:
        st.info(f"Add '{path}' to your GitHub repo to display: {caption}")

def metric_card(label, value):
    st.metric(label, value)

# ----------------------------
# Header
# ----------------------------
st.title("AIC3D: AI-Catalyzed Drug Decay Detector")
st.subheader("Environmental degradation prediction for pharmaceutical compounds")

st.markdown("""
AIC3D is a machine learning project built to predict drug degradation behavior before environmental release, 
using molecular descriptors and pH-dependent conditions. The goal is to explore whether computational screening 
can help identify stability and degradation risks earlier, rather than relying only on reactive laboratory testing 
after manufacturing and distribution.
""")

st.divider()

# ----------------------------
# Overview metrics
# ----------------------------
st.markdown("## Project Overview")

col1, col2, col3, col4 = st.columns(4)
with col1:
    metric_card("Model Type", "Random Forest")
with col2:
    metric_card("Validation Method", "LODO")
with col3:
    metric_card("Feature Vector Size", "2055")
with col4:
    metric_card("Primary Use Case", "Pre-screening")

st.markdown("""
**Core question:** Can molecular structure and environmental context be used to estimate degradation trends across drugs?

**Main outcome:**  
The model performed strongly on internal/random-split evaluation, but Leave-One-Drug-Out validation showed poor generalization 
to unseen drugs. This suggests the system captures within-dataset patterns well, but is not yet robust enough for reliable 
cross-drug prediction.
""")

st.divider()

# ----------------------------
# Problem statement
# ----------------------------
st.markdown("## 1. Problem Statement")
st.write("""
Pharmaceutical compounds often enter the environment through wastewater, improper disposal, and incomplete treatment. 
Their persistence depends on molecular structure and environmental conditions such as pH. Traditional degradation testing 
is often slow, expensive, and reactive. AIC3D explores whether a machine learning model can provide an earlier computational 
screening layer to flag compounds that may degrade slowly or unpredictably.
""")

st.markdown("""
This project focuses on:
- predicting degradation-related behavior from structure + pH
- testing whether the model can generalize to completely unseen drugs
- identifying whether the model is learning real chemical patterns or over-relying on simple shortcuts
""")

st.divider()

# ----------------------------
# Methodology
# ----------------------------
st.markdown("## 2. Methodology")

col1, col2 = st.columns([1.2, 1])

with col1:
    st.markdown("""
### Input Features
The model combines:
- 2048-bit Morgan fingerprints (radius = 2)
- TPSA
- logP
- Molecular Weight
- H-bond Donors
- H-bond Acceptors
- pH

This produces a final feature vector of **2055 dimensions**.

### Model
- Random Forest Regressor
- scikit-learn implementation

### Evaluation Approaches
1. **Random split / internal validation**
   - 80/20 train-test split
   - 5-fold cross-validation using MSE

2. **LODO validation**
   - Leave-One-Drug-Out
   - One full drug held out at a time
   - Tests whether the model generalizes across compounds
""")

with col2:
    st.markdown("""
### Why LODO Matters
Random train-test splits can look strong even when the model has seen very similar chemical patterns in training.

LODO is a harder and more honest validation strategy because:
- the held-out drug is completely unseen
- performance drop reveals overfitting risk
- it better reflects real deployment scenarios
""")

st.divider()

# ----------------------------
# Dataset section
# ----------------------------
st.markdown("## 3. Dataset")

st.write("""
The dataset combines curated degradation information across multiple drugs and pH conditions. 
The emphasis was on creating a compact but chemically meaningful benchmark that could test whether 
the model captures broader degradation patterns rather than memorizing specific examples.
""")

dataset_summary = pd.DataFrame({
    "Aspect": [
        "Drug examples",
        "Conditions included",
        "Target behavior",
        "Feature sources",
        "Validation focus"
    ],
    "Details": [
        "Ibuprofen, Aspirin, Paracetamol, Naproxen, Diclofenac, and extended additions",
        "Multiple pH-dependent conditions",
        "Degradation rate / log-transformed behavior",
        "RDKit descriptors + Morgan fingerprints + pH",
        "Cross-drug generalization"
    ]
})

st.dataframe(dataset_summary, use_container_width=True, hide_index=True)

st.divider()

# ----------------------------
# Main quantitative results
# ----------------------------
st.markdown("## 4. Main Results")

col1, col2, col3 = st.columns(3)
with col1:
    metric_card("5-Fold CV MSE", "0.0277")
with col2:
    metric_card("Train MSE", "0.0130")
with col3:
    metric_card("Test MSE", "0.1062")

st.markdown("""
### Interpretation
These results initially suggest the model is learning useful relationships. However, internal test performance alone is not enough. 
The more important question is whether the model can predict degradation for **new drugs it has never seen before**.
""")

st.divider()

# ----------------------------
# Feature importance
# ----------------------------
st.markdown("## 5. Feature Importance")

feature_importance_df = pd.DataFrame({
    "Feature": ["TPSA", "pH", "MolWt", "Other descriptors / fingerprint contributions"],
    "Importance": [0.1104, 0.0653, 0.0042, 0.8201]
})

col1, col2 = st.columns([1.1, 1])

with col1:
    st.bar_chart(feature_importance_df.set_index("Feature"))

with col2:
    st.markdown("""
### Insight
The model appears especially sensitive to:
- **TPSA**
- **pH**

This is chemically meaningful to some degree, but the LODO results suggest that these signals are not enough 
to support strong out-of-drug generalization. In practice, the model may be learning a mixture of real chemistry 
and dataset-specific shortcuts.
""")

st.divider()

# ----------------------------
# LODO results
# ----------------------------
st.markdown("## 6. Leave-One-Drug-Out Results")

try:
    df = pd.read_csv("AIC3D_v2_results.csv")
    st.write("""
The table below contains the drug-by-drug LODO results. This is the most important validation block in the project because it shows 
how performance changes when the model is asked to predict a completely unseen compound.
""")
    st.dataframe(df, use_container_width=True)

    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()

    if "MSE" in df.columns:
        st.markdown("### LODO MSE by Drug")
        chart_df = df.set_index(df.columns[0])["MSE"]
        st.bar_chart(chart_df)

    elif len(numeric_cols) > 0:
        st.markdown("### Numeric Result Overview")
        st.bar_chart(df.set_index(df.columns[0])[numeric_cols])

except FileNotFoundError:
    st.error("AIC3D_v2_results.csv not found. Upload it to the root of your GitHub repo.")

st.markdown("""
### LODO Conclusion
LODO validation showed that the model does **not** generalize reliably across unseen drugs.  
This is an important and valuable result: it demonstrates scientific honesty and identifies the main limitation 
that future versions of AIC3D need to solve.
""")

st.divider()

# ----------------------------
# Figures / visuals
# ----------------------------
st.markdown("## 7. Figures")

st.write("""
To make this page feel like a full project deck, add your figures as image files in the GitHub repo. 
Suggested filenames are already wired below. If a file is missing, the app will simply show a note.
""")

fig1, fig2 = st.columns(2)
with fig1:
    show_image_if_exists("project_pipeline.png", "Figure 1. AIC3D project pipeline")
    show_image_if_exists("feature_importance.png", "Figure 2. Feature importance visualization")
with fig2:
    show_image_if_exists("lodo_results_plot.png", "Figure 3. LODO performance across drugs")
    show_image_if_exists("problem_context.png", "Figure 4. Environmental context and motivation")

st.markdown("""
### Recommended Figures to Add
Use these as PNG files in your repo:
- `problem_context.png`
- `project_pipeline.png`
- `feature_importance.png`
- `lodo_results_plot.png`

You can export them from:
- Canva
- PowerPoint
- Python/Matplotlib
- screenshots from Colab outputs
""")

st.divider()

# ----------------------------
# Why this matters
# ----------------------------
st.markdown("## 8. Why This Project Matters")

st.write("""
AIC3D matters because it moves environmental degradation assessment toward an earlier and more scalable computational workflow. 
Even though the current model does not yet generalize robustly across drugs, the project establishes:
- a complete prototype pipeline
- a chemically grounded feature framework
- a more rigorous validation approach through LODO
- a clear direction for improvement
""")

st.markdown("""
This makes the project useful not only for its predictions, but for its **evidence-based identification of failure modes**.
That is what turns it from a simple ML demo into a real research project.
""")

st.divider()

# ----------------------------
# Limitations
# ----------------------------
st.markdown("## 9. Limitations")

st.markdown("""
- Small and heterogeneous dataset
- Limited cross-drug coverage
- Strong sensitivity to pH-related patterns
- Random split performance can overestimate usefulness
- More external validation is needed before practical deployment
""")

st.divider()

# ----------------------------
# Next steps
# ----------------------------
st.markdown("## 10. Next Steps")

st.markdown("""
Planned future directions:
- expand the dataset with more drugs and more condition diversity
- obtain expert review from environmental chemistry / pharmaceutical specialists
- build a stronger external validation benchmark
- compare multiple model families beyond Random Forest
- publish a project write-up / article / research summary
- create a public-facing project website and dashboard
""")

st.divider()

# ----------------------------
# Final takeaway
# ----------------------------
st.markdown("## 11. Final Takeaway")

st.write("""
AIC3D successfully built an end-to-end pipeline for predicting drug degradation behavior from molecular and environmental inputs. 
The strongest result of the project is not just that a model was trained, but that a more realistic validation setup revealed 
the current limitation clearly: **generalization across unseen drugs remains the main challenge**.

That makes this project a strong foundation for a next version rather than an overclaimed finished solution.
""")
