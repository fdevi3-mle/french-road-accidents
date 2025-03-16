import streamlit as st

from src.utils import FIGURE_8, FIGURE_11, FIGURE_30

st.set_page_config(
    page_title="Containerization",
    page_icon="🐳",
    layout="wide"
)
st.write("# Containerization 🐳")
st.markdown("""
All the services we added in the previous pages were thus containerized via separate Docker containers and existing on a `common_network` and communicating with each other.
I also added a `test_user` Client to simulate real world requests.
""")
st.write("#####")
l_col,r_col = st.columns(2,border=True)
with l_col:
    st.subheader("Main DockerFile Snippet")
    code_snippet = '''
    FROM python:3.9
WORKDIR /code
COPY requirements.txt /code/requirements.txt
.....
CMD ["fastapi", "run", "app/main.py","--host" , "0.0.0.0", "--port", "8000"]
     '''
    st.code(code_snippet, language="docker")

with r_col:
    st.subheader("Docker Compose with All Service Snippet")
    code_snippet = '''
services:
  fast_api:
    build:
      context: .
      dockerfile: Dockerfile_app
    container_name: fast_api_container
    ports:
      - "8000:8000"
    networks:
      - test_network
  prometheus:
    image: prom/prometheus:latest
    ......
     '''
    st.code(code_snippet, language="yaml")