pip install streamlit
import streamlit as st
import pandas as pd

st.title("AIC3D — Drug Degradation Predictor")

st.markdown("### Project Summary")
st.write("""
AIC3D predicts drug degradation rates using molecular descriptors and pH.
Key finding: Model fails to generalize across drugs.
""")

# Load results
df = pd.read_csv("AIC3D_v2_results.csv")

st.markdown("### LODO Results")
st.dataframe(df)

st.markdown("### Key Insight")
st.write("Model relies heavily on pH and fails cross-drug generalization.")

st.markdown("### Feature Importance")
importance = {
    "pH": 0.67,
    "LogP": 0.10,
    "TPSA": 0.09,
    "HBA": 0.08,
    "MW": 0.04,
    "HBD": 0.01
}
st.bar_chart(importance)
