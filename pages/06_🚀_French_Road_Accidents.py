import streamlit as st

from src.utils import FIGURE_28

st.set_page_config(
    page_title="French Road Accidents Unified Decisionmaker",
    page_icon="🖥️",
    layout="wide"
)
st.write("# French Road Accidents Unified Decisionmaker 🚀")
st.divider()
st.image(FIGURE_28, caption="Figure: Architecture Diagram", width =1650)
st.write("#")
st.markdown("""
As part of DataScientets (DS) continuing course on MLE , I present DS is _French Road Accidents Unified Decisionmaker_. 
To begin with we take the lessons learnt from the _DataScience Project_ and expand it to create an entire MLOps system.
The architecture of the system can be seen above. 
The Entire architecture can be broken into 2 Main Blocks
+ Road Accident Model Trainer
+ Road Accident Service
""")
st.markdown("""
#### Road Accident Model Trainer:
This block consists mainly of an orchestration pipeline which is used to train the Unified DecisonMaker Models [^1]. We will talk more about this later

#### Road Accident Service:
This block mainly allows the users to access the _latest_ versions of the UD models and call an inference endpoint to make predictions about the severity of the accident or forecasting the next _n_ periods of the year
[^1]: In our previous project we have both a forecaster and a severity classifier , these 2 put together will hence be refered to as Unified DecisionMaker(UD) Models
""")