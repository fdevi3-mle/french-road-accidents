import streamlit as st

from src.utils import FIGURE_8, FIGURE_11, FIGURE_30

st.set_page_config(
    page_title="Containerization",
    page_icon="🐳",
    layout="wide"
)
st.write("# Containerization 🐳")
st.markdown("""
Once the UD Model Training was done and the Models were uploaded to the _CometML_ model registry. We needed to create an Inference Service where the user can query for
Severity Classifications & Forecast Predictions. To build such a system we employed a relatively cool architecture (see image below) where each component was containerized in a _Docker_ system.
""")

st.write("##")
st.image(FIGURE_30, caption="Figure: Road Accident Service Architecture Diagram", width =1400)
st.divider()
st.markdown("""
In the next few pages we will go over the main components of the __Road Accident Architecture Service__ Diagram as listed below
1. REST API Endpoints
    + Inference Endpoint:
        - "/predict/forecast"
        - "/predict/severity"
    + Admin Endpoint: via security clearance only
        - "/admin"
    + Metrics Endpoint with "/metrics"
2. Prometheus Service for "/metrics" scrapping
3. Grafana Service with Dashboard for Monitoring
4. Test Clients (both User and Admin) just for testing
""")
