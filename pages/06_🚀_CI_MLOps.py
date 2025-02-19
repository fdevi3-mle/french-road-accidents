import streamlit as st

from src.utils import FIGURE_8, FIGURE_11

st.set_page_config(
    page_title="Danger Zones",
    page_icon="🚀",
    layout="wide"
)
st.write("# CI And MLOps 🚀")
st.markdown("""
 I decided to set up an
automatic Machine Learning system . The idea was to create a CI Pipeline
wherein the machine learning model would run and deploy the model as an
artifact of the pipeline for later use. This is how one would do even a simple ML
project in a production environment. CI/CD allows one to focus on the task of just
creating code and not worrying about running the model locally. This would
significantly free up my hardware and computational limitations .
So with this in mind and the desire to run longer training models I built a CI/CD
Pipeline which allows me to code and not worry about the local training of the
model and thus optimizing its parameters (see Figure 8)
""")
_, col, _ = st.columns([1, 2, 1])
with col:
    st.write("#")
    st.image(FIGURE_8, caption="Figure8: CI/CD Pipeline Architecture", width=600)
    st.write("#")


st.markdown("""
ZenML was chosen as an MLOps orchestrator as it provided both a local and
cloud orchestration. The ZenML pipeline consists of steps involved in setting up a
an automatic Machine Learning Flow for the entire process of loading the data to
training the ML Model (see run-zenml.py).This pipeline was quite a feat and would allow me to finally focus on
creating models and tuning them rather than running the models.
I hit another roadblock in the space provided by DS and even after a request , no
reply was given. I am including this in the report as it is important to understand
how the DS is extremely poor and it's nothing short of a waste of time.
I would have loved to run a longer training for either the classifier or the time
series model but we are sticking with the results we achieved.
""")

#https://discuss.streamlit.io/t/how-to-add-extra-lines-space/2220/5
_, col, _ = st.columns([1, 3, 1])
with col:
    st.write("#")
    st.image(FIGURE_11, caption="Figure: Orchestrator Pipeline", width =600)
    st.write("#")

st.markdown("""
## Experiment Tracking with Neptune AI

The classifier pipleline runs have been logged to [Severity Classifier NeptuneAI](https://app.neptune.ai/o/France-Road-Accidents-Test/org/SeverityClassifier)
""")

st.write("#")
st.divider()
st.subheader("Final Notes")
st.markdown("""
The entire project is [French Road Accidents](https://github.com/fdevi3-mle/french-road-accidents/tree/develop) , as usual all good code has some 
_interesting_ code behind it [Road Accidents](https://github.com/fdevi3-mle/road-accidents) where all  prototypes, experiments and spaghetti code lies :)
""")
