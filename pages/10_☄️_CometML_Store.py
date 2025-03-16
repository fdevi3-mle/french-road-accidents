import streamlit as st

from src.utils import FIGURE_8, FIGURE_11, FIGURE_29, FIGURE_18, FIGURE_24

st.set_page_config(
    page_title="CometML Store",
    page_icon="☄️",
    layout="wide"
)
st.write("# CometML Store  ☄️")
st.markdown("""
Although ZenML has an Automatic Artifact Store and a Data Version System [^1] , it was "not" accepted (more like not understood).
Nevertheless we use _CometML_ as a cloud registry store to version, upload and download Data and UD Models. We can thus break Comet ML into 3 main pieces

+ Input Data Store : Version and Upload Input Dataset. This dataset version can be tracked 
+ Forecast Model Store : Version and Store the Forecast Model which can be retrieved from the registry
+ Severity Model Store : Version and Store the Severity Classifier Model which can be downloaded for the _Inference Client_

[^1]: [ZenML Artifact Store](https://docs.zenml.io/how-to/data-artifact-management/handle-data-artifacts/artifact-versioning)
""")

st.divider()
left_col,mid_col,right_col = st.columns(3,border=True)

with left_col:
    st.image(FIGURE_29, caption="CometML Input Data Store")
with right_col:
    st.image(FIGURE_18, caption="Comet ML Model Store")
with mid_col:
    st.image(FIGURE_24, caption="CometML Model Store")

st.divider()
st.subheader('Sample Dummy Code to Download Model From Registry')
code_snippet= '''
def get_arima_model():
    try:
        api.download_registry_model("xxx", "xxxx-model", output_path="Some_Path" expand=True, stage=None)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_412_PRECONDITION_FAILED, detail=str(e))
'''
st.code(code_snippet, language="python")

