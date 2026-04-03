import streamlit as st
import pandas as pd

# Page config
st.set_page_config(page_title="AIC3D Dashboard", layout="wide")

# Title
st.title("🧪 AIC3D — Drug Degradation Predictor")

# Project Summary
st.markdown("## 📌 Project Summary")
st.write("""
AIC3D is a machine learning model designed to predict drug degradation rates 
based on molecular descriptors and environmental pH.

**Key finding:**  
The model performs well on seen data but fails to generalize across unseen drugs (LODO validation).
""")

# Load data
try:
    df = pd.read_csv("AIC3D_v2_results.csv")
    
    st.markdown("## 📊 LODO Results")
    st.dataframe(df)

except FileNotFoundError:
    st.error("CSV file not found. Make sure 'AIC3D_v2_results.csv' is uploaded.")

# Key Insight
st.markdown("## 🔍 Key Insight")
st.write("""
The model heavily relies on pH as a dominant feature.  
This leads to poor generalization when predicting degradation for completely unseen drugs.
""")

# Feature Importance
st.markdown("## ⚙️ Feature Importance")

importance_df = pd.DataFrame({
    "Feature": ["pH", "LogP", "TPSA", "HBA", "MW", "HBD"],
    "Importance": [0.67, 0.10, 0.09, 0.08, 0.04, 0.01]
})

st.bar_chart(importance_df.set_index("Feature"))
