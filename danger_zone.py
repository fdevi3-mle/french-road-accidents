import logging
import os
import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

from src.franums import RoadAccidentEnum
from src.utils import INPUT_PARQUET, MID_LONG, MID_LAT, FIGURE_1

#Logger
logger = logging.getLogger(__name__)
##Use cpu only
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

#https://towardsdatascience.com/creating-true-multi-page-streamlit-apps-the-new-way-2022-b859b3ea2a15/
## Name & Title
st.set_page_config(
    page_title="Road Accidents in France -- The Danger Zones",
    page_icon="🚑",
    layout="wide"
)

### Methods

@st.cache_data
def data_loader(filepath=INPUT_PARQUET, sample_size=0.075):
    if filepath is None:
        filepath = INPUT_PARQUET
    df = pd.read_parquet(filepath)
    valid_columns = RoadAccidentEnum.to_dict()
    valid_columns = valid_columns.keys()
    df = df[[col for col in df.columns if col in valid_columns]]

    ## BLOCKER FOR SAMPLE SIZE
    if sample_size >0.25:
        sample_size = 0.25 ## just a block as streamlit cant handle large data
    logger.info(f" Creating a Random Sample of {sample_size * 100}% of data")
    df = df.sample(frac=sample_size, random_state=42)
    return df


### Streamlit
st.write("# Road Accidents in France 🚑")

data_load_state = st.text('Loading data...')
data = data_loader()

# Save the data to session state https://discuss.streamlit.io/t/how-can-i-use-dataframes-in-different-pages/34603
st.session_state.dataframe = data

data_load_state.text("Hi!")


st.markdown("""
Road Accidents are the leading cause of death worldwide for children and young adults till aged 30, causing over 1 million deaths annually [WHO](https://www.who.int/news-room/fact-sheets/detail/road-traffic-injuries).
This heavy cost not only incurs a toll on the future of the country but costs an estimated 3% loss of GDP to most countries
The objective of this project was to create a prediction model for accident severity and map out danger zones across France based on traffic accidents data.

### Project Goals
+ Analyze accident data
+ Predict the severity of the Traffic Accidents
+ Forecast accidents in France
+ Visualize the Danger Zones

The analysis was done from the years 2019-2023 and the area was limited to mainland France and its nearby island. We can visualize the accidents
below [^1]. 

[^1]: We have selected a tiny slice of the data as streamlit cant handle large files for viewing.
""")

st.subheader('Road Accident Map of France')

#Map
# st.pydeck_chart(
#     pdk.Deck(
#         map_style=None,
#         initial_view_state=pdk.ViewState(
#             latitude=MID_LAT,
#             longitude=MID_LONG,
#             zoom=4,
#             min_zoom=3,
#             max_zoom=10,
#             pitch=40,
#             bearing=-20,
#         ),
#         layers=[
#             pdk.Layer(
#                 "HexagonLayer",
#                 data=data,
#                 get_position="[long, lat]",
#                 radius=200,
#                 elevation_scale=4,
#                 elevation_range=[0, 1000],
#                 pickable=True,
#                 extruded=True,
#             ),
#             pdk.Layer(
#                 "ScatterplotLayer",
#                 data=data,
#                 get_position="[long, lat]",
#                 get_color="[200, 30, 0, 160]",
#                 get_radius=200,
#             ),
#         ],
#     )
# )

st.subheader('Static Scatter Plot of Road Accidents in France from 2019-2023')
st.image(FIGURE_1, caption="Figure 1: Scatter Plot of Road Accidents in France")

st.markdown("""
As we can see from the map above the French region accidents are cluttered around certain metropolitan areas (eg Paris).If we need to analyze how these
areas influence the likelihood of an accident we need to introduce some sort of clustering
**👈 We do! , see Page 2**
""")


