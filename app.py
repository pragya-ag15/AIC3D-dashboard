import os
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="AIC3D Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# Pro Aesthetic Styling
# -----------------------------
st.markdown("""
<style>
    /* Resetting the forced dark colors for better visibility */
    :root {
        --text-color: inherit;
    }
    
    /* Hero section - Glassmorphism style */
    .hero {
        background: linear-gradient(135deg, #1e40af 0%, #1e3a8a 100%);
        color: white !important;
        padding: 2.5rem;
        border-radius: 15px;
        margin-bottom: 2rem;
    }
    .hero h1 { color: white !important; margin-bottom: 0; }
    .hero p { color: #d1d5db !important; }

    /* Fix for the "Ugly" Sidebar Text visibility */
    [data-testid="stSidebar"] {
        background-color: #f8fafc;
    }
    
    /* Metric Card Polish */
    [data-testid="stMetric"] {
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 10px 15px !important;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Sidebar: Professional Links
# -----------------------------
with st.sidebar:
    st.title("Project Links")
    st.markdown(f"""
    - **GitHub:** [AIC3D Repository](https://github.com/pragya-ag15/AIC3D-dashboard)
    - **LinkedIn:** [Pragya Agarwal](https://www.linkedin.com/in/pragyaag15/)
    - **Email:** [Contact](mailto:pragyaagarwal004@gmail.com)
    """)
    st.divider()
    st.caption("AIC3D: Artificial Intelligence Chemical Degradation, Design & Discovery")

# -----------------------------
# Main UI
# -----------------------------
st.markdown("""
<div class="hero">
    <h1>AIC3D</h1>
    <p>AI-Catalyzed Drug Decay Detector: Predicting pharmaceutical environmental impact.</p>
</div>
""", unsafe_allow_html=True)

# Metrics
m1, m2, m3, m4 = st.columns(4)
m1.metric("Model", "Random Forest")
m2.metric("Validation", "LODO")
m3.metric("Features", "2055")
m4.metric("MSE (LODO)", "0.1062")

st.divider()

# -----------------------------
# Pro Features: Molecular Insights
# -----------------------------
tab1, tab2 = st.tabs(["📊 Results & LODO", "🧪 Molecular Analysis"])

with tab1:
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("Key Finding")
        st.info("**Generalization Gap:** The high variance in LODO results suggests the model is sensitive to specific molecular scaffolds.")
        
    # Example Download Feature (Pro)
    def load_csv():
        for fname in ["AIC3D_v2_results.csv", "aic3d_v2_results.csv"]:
            if os.path.exists(fname): return pd.read_csv(fname)
        return None

    df = load_csv()
    if df is not None:
        st.dataframe(df, use_container_width=True)
        # Pro Feature: Export functionality
        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Export Results as CSV", data=csv_data, file_name="AIC3D_Results.csv")
    else:
        st.warning("Results CSV not found. Ensure file is in the root directory.")

with tab2:
    st.subheader("Chemical Descriptors")
    # Pro Feature: Detailed breakdown of what the model "sees"
    st.write("The model utilizes 2048-bit Morgan fingerprints alongside physicochemical properties:")
    
    c1, c2, c3 = st.columns(3)
    c1.markdown("- **TPSA:** Polar Surface Area")
    c2.markdown("- **LogP:** Hydrophobicity")
    c3.markdown("- **MolWt:** Molecular Weight")

    # Image logic
    if os.path.exists("project_pipeline.png"):
        st.image("project_pipeline.png", caption="Analysis Pipeline", use_container_width=True)
