import streamlit as st

from src.utils import FIGURE_8, FIGURE_11, FIGURE_30, FIGURE_31, FIGURE_32

st.set_page_config(
    page_title="Fast API Endpoint",
    page_icon="📨",
    layout="wide"
)
st.write("# Fast API Service 📨")
st.markdown("""
As part of the UD Inference service we built a REST API for Model Inferencing with the help of _FastApi_.
The API was containerized via _Docker_.
The API was divided into multiple Parts

+ Production : The Endpoint for the Users to query predictions/classification services
+ Admin : Endpoint with security clearance for retraining the model if model is "Unhealthy"
+ Health : Enpoint for Health checks
+ Metrics : Metrics gathering and Instrumentation endpoint for Prometheus

""")

st.write("##")
st.image(FIGURE_31, caption="Figure: FAST API Docs", width =1400)
st.divider()
st.markdown("""
We first load the UD Models from the CometML Registry Store at startup before creating the required enpoints. We will look at a few Important ones.
+ Forecast Predictions: The endpoint located at "/predict/forecast" provides a _Response_ with the predictions for the number of queried periods of the future. It expects a `ForecastRequest`
+ Severity Predictions : The endpoint located at "/predict/severity" expecting a `ClassifierRequest` provides a response if the accident was _Major_ or _Minor_
+ Retrain : The endpoint at "/admin/retrain" expecting an `Authenticated` _admin_ with a `AdminRequest` to retrain the models.
""")
st.write("#####")
st.subheader("Code Snippets Forecaster")
l1_col,r1_col = st.columns(2, border=True)

with l1_col:
    code_snippet = '''
    @app.post("/predict/forecast", tags=['production'])
async def forecast_accidents(request: Annotated[ForecastRequest, Query()]):
    try:
        arima_model = model_dic['arima_model']
        forecast = arima_model.predict(n_periods=request.periods)
        .....
    '''
    st.code(code_snippet, language="python")

with r1_col:
    code_snippet = '''
    class ForecastRequest(BaseModel):
    periods: int = Field(100, gt=0, le=366)
    '''
    st.code(code_snippet, language="python")

st.write("#####")
st.subheader("Code Snippets Severity Classifier")
l2_col,r2_col = st.columns(2, border=True)

with l2_col:
    code_snippet = '''
@app.post("/predict/severity", tags=['production'])
async def predict_severity(request: Annotated[ClassifierRequest, Query()]):
    try:
        gbc_model = model_dic['gbc_model']
        prediction = gbc_model.predict(_df)
        ....
    '''
    st.code(code_snippet, language="python")

with r2_col:
    code_snippet = '''
class ClassifierRequest(BaseModel):
    vehicle_category: Literal['1', '2', '3', '4', '0']
    obstacle_mobile: Literal['1', '2', '3', '0']
    impact_point: Literal['1', '2', '3', '4', '0']
    action: Literal['1', '2', '3', '4', '0']
    .....
    '''
    st.code(code_snippet, language="python")

st.write("###")
st.subheader("Authentication")
l3_col,r3_col = st.columns(2, border=True)

with l3_col:
    code_snippet = '''
@app.post("/admin/retrain", tags=['admin'])
async def retrain_model(username: Annotated[str, Depends(authenticate)], request: Annotated[AdminRequest, Query()]):
    '''
    st.code(code_snippet, language="python")

with r3_col:
    st.image(FIGURE_32, caption="Figure: Authentication Screen")
