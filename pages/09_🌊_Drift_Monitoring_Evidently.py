import streamlit as st

from src.utils import FIGURE_8, FIGURE_11, FIGURE_23, FIGURE_17, FIGURE_29, FIGURE_21, FIGURE_19, FIGURE_20

st.set_page_config(
    page_title="Drift Monitoring using Evidently",
    page_icon="🌊",
    layout="wide"
)
st.write("# Drift Monitoring Using Evidently🌊")
st.markdown("""
One of the requirements for the project was some sort of Monitoring. Thankfully _Evidently_ Provides a free service so one can monitor

+ Data Drift Monitoring : Monitor the Data for Drift (see image below)
+ Forecast Model Monitor : Monitor that the model provides _good_ scores (see image below)
+ Severity Model Monitor : Monitor the model for classification scores (see image below)
""")

st.divider()
left_col,mid_col,right_col = st.columns(3,border=True)

with left_col:
    st.image(FIGURE_17, caption="Evidently Data Drift Monitoring")
with right_col:
    st.image(FIGURE_21, caption="Evidently Model Drift Monitoring")
with mid_col:
    st.image(FIGURE_19, caption="Evidently Model Drift Monitoring")

st.markdown("""
#### Alert System:
We can also set an alert system if the monitoring results are not upto par . for eg
+ Forecast Alert : Send an auto alert if the Forecast _mape_ score goes above 25 (see image below)
""")
_, col, _ = st.columns([1, 5, 1])
with col:
    st.write("#")
    st.image(FIGURE_20, caption="Auto Alert Evidently Monitoring", width=800)
    st.write("#")
