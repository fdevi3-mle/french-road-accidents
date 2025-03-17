import streamlit as st

from src.utils import FIGURE_8, FIGURE_11, FIGURE_30, FIGURE_26

st.set_page_config(
    page_title="Monitoring Service with Prometheus and Grafana",
    page_icon="🎬",
    layout="wide"
)
st.write("# Monitoring Service with Prometheus and Grafana 🎬")
st.markdown("""
To keep track of the Model and monitor the Services of the Inference Endpoint , I created a _Grafana_ Dashboard which scrapes the `Fast_API` service via prometheus and then displays the necessary 
metrics and requests.

+ Prometheus : Using a `prometheus_fastapi_instrumentator` I scrape the _Fast API_ endpoints and `metrics`
+ Grafana : The Prometheus scrapes are then logged into a Dashboard (See below)
""")

st.write("#####")
st.subheader("Prometheus Fast API Instrumentation")
l1_col,r1_col = st.columns(2, border=True)

with l1_col:
    code_snippet = '''
    from prometheus_fastapi_instrumentator import Instrumentator
    Instrumentator().instrument(app).expose(app)
    '''
    st.code(code_snippet, language="python")

with r1_col:
    st.subheader("Prometheus Yaml Config Snippet")
    code_snippet = '''
      - job_name: 'fast_api'
    scrape_interval: 2s
    metrics_path: /metrics
    static_configs:
      - targets: ['fast_api:8000']
    '''
    st.code(code_snippet, language="yaml")
st.divider()
st.write("##")
st.image(FIGURE_26, caption="Figure: Grafana Dashboard", width =1400)

