import os
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="AIC3D Dashboard",
    layout="wide",
    initial_sidebar_state="expanded" # Changed to expanded for better navigation
)

# -----------------------------
# Enhanced Responsive Styling
# -----------------------------
st.markdown("""
<style>
    /* Main container styling */
    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
    }

    /* Fixed Text Colors - Using a softer Slate color for better readability */
    .stMarkdown, p, span, label {
        color: #1e293b !important;
    }

    /* Hero section - Modern gradient */
    .hero {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        color: #f8fafc !important;
        padding: 2.5rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    .hero h1, .hero-title {
        color: #ffffff !important;
        font-size: 3rem;
        font-weight: 800;
        margin: 0;
    }
    .hero-subtitle {
        color: #cbd5e1 !important;
        font-size: 1.2rem;
        margin-top: 0.5rem;
    }

    /* Section Labels */
    .section-label {
        font-size: 1.1rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #475569 !important;
        margin-bottom: 10px;
    }

    /* Metric Card Styling */
    [data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 15px !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    [data-testid="stMetricValue"] {
        color: #1d4ed8 !important;
        font-weight: 700 !important;
    }

    /* Link and Button Styling */
    a {
        color: #2563eb !important;
        text-decoration: none;
    }
    a:hover {
        text-decoration: underline;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Recommended Sidebar Additions
# -----------------------------
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/test-tube.png", width=80)
    st.title("Navigation & Links")
    st.markdown("---")
    st.markdown("### Resources")
    st.markdown("[📄 Documentation](https://your-docs-link.com)")
    st.markdown("[💻 GitHub Repository](https://github.com/your-username/AIC3D)")
    st.markdown("[📧 Contact Support](mailto:support@aic3d.com)")
    
    st.markdown("---")
    st.info("**Tip:** Use the LODO (Leave-One-Drug-Out) results to verify chemical generalization.")

# -----------------------------
# Helpers
# -----------------------------
def load_csv():
    for fname in ["AIC3D_v2_results.csv", "aic3d_v2_results.csv"]:
        if os.path.exists(fname):
            return pd.read_csv(fname)
    return None

df = load_csv()

# -----------------------------
# Hero
# -----------------------------
st.markdown("""
<div class="hero">
    <div class="hero-title">AIC3D</div>
    <div class="hero-subtitle">AI-Catalyzed Drug Decay Detector</div>
    <p style="margin-top: 1.5rem; opacity: 0.9;">
        A machine learning system designed to estimate pharmaceutical degradation 
        using molecular descriptors and pH-dependent conditions.
    </p>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Metrics Grid
# -----------------------------
m1, m2, m3, m4 = st.columns(4)
with m1: st.metric("Model", "Random Forest")
with m2: st.metric("Validation", "LODO")
with m3: st.metric("Features", "2055")
with m4: st.metric("Mode", "Pre-screening")

st.write("")

# -----------------------------
# Key finding + hero visual
# -----------------------------
left, right = st.columns([1.15, 0.85])

with left:
    st.markdown('<div class="section-label">Key Finding</div>', unsafe_allow_html=True)
    st.warning("""
        **Generalization Gap Identified:** While internal metrics are high (MSE 0.0130), 
        the model struggles with unseen drugs (LODO MSE 0.1062). 
        This highlights the necessity of structure-based validation.
    """)

with right:
    if os.path.exists("problem_context.png"):
        st.image("problem_context.png", caption="Project context", use_container_width=True)
    else:
        st.info("💡 Project visualization placeholder.")

st.divider()

# -----------------------------
# Tabbed Content
# -----------------------------
tab1, tab2, tab3 = st.tabs(["Methodology", "Performance Data", "Final Insights"])

with tab1:
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("**Feature Engineering**")
        st.markdown("""
        - 2048-bit Morgan Fingerprints
        - Physicochemical properties (TPSA, logP, MolWt)
        - Environmental pH levels
        """)
    with col_b:
        st.markdown("**Experimental Design**")
        st.markdown("""
        - **Internal:** 5-fold Cross-Validation
        - **External:** Leave-One-Drug-Out (LODO)
        """)

with tab2:
    if df is not None:
        st.markdown('<div class="section-label">Detailed Results</div>', unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True)
        st.bar_chart(df.iloc[:, [0, 1]].set_index(df.columns[0]))
    else:
        st.error("Results file `AIC3D_v2_results.csv` not found.")

with tab3:
    st.markdown('<div class="section-label">Conclusion</div>', unsafe_allow_html=True)
    st.success("""
    AIC3D serves as a **methodological benchmark**. It proves that while ML can learn 
    chemical patterns, "chemical intuition" requires more diverse training sets 
    to generalize across novel drug scaffolds.
    """)
