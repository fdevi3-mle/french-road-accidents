import logging
import os
import streamlit as st
import pandas as pd
import plotly.express as px
from plotly_resampler import register_plotly_resampler

from src.utils import FIGURE_2, FIGURE_3

st.set_page_config(
    page_title="Severity Classifier",
    page_icon="🌏",
    layout="wide"
)
st.write("# GPS Coordinates to H3 hashes 🌏")


st.image(FIGURE_2, caption="Figure2: Scatter Plot of Road Accidents from 2019-2023")

st.markdown("""
The GPS coordinates prove to be a vital feature and its visualization allows us to see the development and clusters of road accidents in France.(See Figure :2)
We first limit our data to the Mainland of France only and its tiny nearby island (see code snippet below). Then our first goal was to naively cluster regions in France according to their accidents and thus create a cluster map of France . We used simple and a bit advanced geo-spatial clustering techniques in the form of KNN & Hierarchical
Density Based Spatial Clustering (HDBSCAN) [^1]. These naive methods generally provided the main clusters around the metropolitan area of Paris and other large
cities but failed to correctly identify outliers in the coordinate data.

A better alternative was to use an already available spatial clustering system which
would provide much stable and useful results in the form of H3 (Uber) [^2]. It creates a
hierarchical spatial index that would hash out coordinates18 into hexagon clusters
at a desired resolution which dictates the size of the clustered region. It was quite
easy to implement and thus each Point was hashed into a h3[^3] id (See code snippet below).
We were thus able to index mainland France and its nearby territory into
manageable hexagon areas (see Figure 3) where each hexagon represents an area in the spatial index of France.
This indexing is computationally expensive hence a lower resolution of 4 was used
, however a higher resolution (which means more h3 hexagons) would make
sense for inter metropolitan area segmentation especially for Paris.
The h3 index also allowed us to gather up the accident counts per hexagon
which allowed us to keep a tally on h3 hexagons which are more risky (Paris and other metropolitan regions are no surprise given the population density)

[^1]: https://hdbscan.readthedocs.io/en/latest/basic_hdbscan.html
[^2]: https://www.uber.com/en-DE/blog/h3/
[^3]: H3, H3_hash, h3 index, h3 id all refer to the same thing
""")


st.subheader('Map of France converted into H3 hash hexagons')
st.image(FIGURE_3, caption="Figure3: H3")


st.subheader('Limiting GPS Coordinates to Mainland France ')
code_1 = '''
##LAT & LONG : BORDERS
LAT_MIN = 40.0
LAT_MAX = 60.0
LONG_MIN = -10.0
LONG_MAX = 10.0
mask = (data['lat'] >= LAT_MIN) & (data['lat'] <= LAT_MAX) & (data['long'] >= LONG_MIN) & (data['long'] <= LONG_MAX)
data = data[mask]'''
st.code(code_1, language="python")


st.subheader('Converting GPS Coordiantes to H3 hash')
code_2= '''H3_RESOLUTION = 4 # Higher res may cause too many hexs and crashes
    data['h3'] = data.apply(lambda row: h3.latlng_to_cell(row['lat'], row['long'], H3_RESOLUTION), axis=1)'''
st.code(code_2, language="python")