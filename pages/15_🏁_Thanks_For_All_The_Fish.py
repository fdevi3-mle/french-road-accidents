import streamlit as st

from src.utils import FIGURE_8, FIGURE_11, FIGURE_30, FIGURE_16, FIGURE_28

st.set_page_config(
    page_title="Thanks for all the Fish ",
    page_icon="🏁",
    layout="wide"
)
st.write("# Thanks for all the Fish 🏁")
st.write("###")
st.image(FIGURE_28, caption="Figure: Complete Project Architecture Diagram", width =1400)
