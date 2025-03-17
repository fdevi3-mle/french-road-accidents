import streamlit as st

from src.utils import FIGURE_8, FIGURE_11, FIGURE_22

st.set_page_config(
    page_title="CI/CD",
    page_icon="🖥️",
    layout="wide"
)
st.write("# Self Hosted CI/CD 🖥️")
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
    st.image(FIGURE_8, caption="Figure8: CI/CD Pipeline Architecture", width=800)
    st.write("#")

st.markdown("""
The CI/CD runs only on _develop_ due the extreme limitations of the cheap EC2 instances provided by DataSceintets [^1]. 
Self Hosted runners gives one good practise how to run actual production based training where the host machine thus has capable hardware.

The CI Workflow consists of a number of steps which run either when _develop_ is triggered (usually Merge Requests) or a manual trigger:
+ Checkout : Checks out the repo into the self hosted machine (see pics below)
+ Setup: Sets up a python environment for training
+ Requirements : Installs the necessary requirements for the project
+ ZenML Flow : Runs a ZenMl pipeline
+ Automated Tests : Tests out the some aspects of the project
+ Upload Model : Uploads artifacts from the steps above for retrieval

[^1]: An extension of space[~10 Euros] or even increasing the timeout is a simple matter , yet after asking over 5x times , this over 12000 Euro course doesnt provide any additional support
""")

st.divider()
st.subheader('Small Snippet Of Develop Workflow')
code_2= '''name: Develop ZenML Workflow

on:
  push:
    branches: ["develop"]
jobs:
  develop:
    name: Develop ZenML JOB
    runs-on: self-hosted
    defaults:
      run:
        working-directory: ${{ github.workspace }}
    steps:
      - uses: actions/checkout@v4
        with:
          lfs: 'true'
      - uses: actions/setup-python@v5
'''
st.code(code_2, language="yaml")
st.divider()
#https://discuss.streamlit.io/t/how-to-add-extra-lines-space/2220/5
_, col, _ = st.columns([1, 4, 1])
with col:
    st.write("#")
    st.image(FIGURE_22, caption="Figure: Self Hosted Runners", width =800)
    st.write("#")

st.markdown("""
#### Self Hosted Runner Limitations
The EC2 had a lot of limitations , Firstly only ~ 4GB of space was left and was never expanded . Also they for some _reason_ a very short timeouts [^2].
But nevertheless its good practise to have all machine learning components on a runner/cloud service. This ensures that the model can train/load/run anywhere.
Our next job is to look at the orchestration

[^2]: An extension of space costs barely a few euros , see [Amazon Elastics Block Store Calculator](https://calculator.aws/#/addService)
""")

