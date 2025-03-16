import streamlit as st

from src.utils import FIGURE_8, FIGURE_11, FIGURE_17, FIGURE_6, FIGURE_29, FIGURE_23

st.set_page_config(
    page_title="ZenML The Maestro",
    page_icon="🖥🎵",
    layout="wide"
)
st.write("# ZenML, The Maestro 🖥🎵")
st.markdown("""
ZenML was chosen as an MLOps orchestrator as it provided both a local and
cloud orchestration. The ZenML pipeline consists of steps involved in setting up a
an automatic Machine Learning Flow for the entire process of loading the data to
training the ML Model (see run-zenml.py).This pipeline thus creates an entire _Machine Learning_ System and allowed me to focus on writing code rather than worry about the model training details.

ZenML is pretty cool as it allows to build and orchestrate (run) and entire Machine Learning System. It divides the system into  multiple `@step`
which could be built up together like a _Lego_ House via `@pipeline`. We can take a look at the architecture diagram for the ZenML Flow[^1] below.    

[^1]: The Pipeline was cached so , only steps that change will be run again, This considerably saves time while training since training can go for about hrs depending on parameters and model.
""")


#https://discuss.streamlit.io/t/how-to-add-extra-lines-space/2220/5
_, col, _ = st.columns([1, 10, 1])
with col:
    st.write("###")
    st.image(FIGURE_11, caption="Figure: Orchestrator Pipeline", width =1200)
    st.write("###")

st.markdown("""
We can break down the pipeline into smaller pieces as below

#### Comon Pipeline Steps:
+ Data Loader : Load the `Input.parquet` data into the system
+ Data Validation : Validate the Input Data using [Pandera](https://pandera.readthedocs.io/en/stable/#) [^1] (see image below)
+ Data Drift Monitoring : Check whether the data is drifting [^2] (see image below)
+ Load DataSet : Version and Load Dataset to [CometML](https://www.comet.com/) (see image below)
+ Data Processor : Perform the necessary pre-processing steps and Data Cleaning 

[^1]: Data Validation here is an overkill since the `RoadAccidentEnum` does validation but DS team wanted it so I put it in. Basically its unnecessary
[^2]: Again , a "genius" since the data is not changing, but as was asked , as it was done.
""")
st.divider()
left_col,mid_col,right_col = st.columns(3,border=True)
with left_col:
    st.write("##")
    st.image(FIGURE_23, caption="Data Validation with Panders Scheme Validation")
with right_col:
    st.image(FIGURE_17, caption="Evidently Drift Monitoring")

with mid_col:
    st.image(FIGURE_29, caption="Load & Version DataSet in CometML")

st.markdown("""
#### Forecast Pipeline:
+ Time Series Creator : Create a time series from the data and separating the required cols.
+ Forecast Model : Train an __ARIMA__ model to forecast the data
+ Plot Model : Validate the trained model has an acceptable _MAPE_ Score and plot the predicted vs actual data
""")


st.markdown("""
#### Severity Classifier:
+ Train Test Split : Split the Data into Training and Testing sets
+ Severity Classifier Model : Train an __GradientBoostingClassifier__ model to predict the severity of the accident 
""")
st.markdown("""
#### Common Loading Steps:
+ Model Monitoring Step : Monitor the Forecast[^1] and Severity[^2] models for metrics drift.
+ Log Model: Version and Upload the UD Models to the CometML Registry.

[^1]: Forecast aka Time Series, Future Accident Predictor . I will interchangebly use these names but they meann the same thing
[^2]: Severity, GBC, Classifier, Severity Classifier . Both models together are UD Models
""")
