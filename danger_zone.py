import logging
import os
import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

from src.franums import RoadAccidentEnum
from src.utils import INPUT_PARQUET, MID_LONG, MID_LAT

#Logger
logger = logging.getLogger(__name__)
##Use cpu only
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

#https://towardsdatascience.com/creating-true-multi-page-streamlit-apps-the-new-way-2022-b859b3ea2a15/
## Name & Title
st.set_page_config(
    page_title="Road Accidents in France -- The Danger Zones",
    page_icon="⛑️",
    layout="wide"
)



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

data_load_state = st.text('Loading data...')
data = data_loader()




st.pydeck_chart(
    pdk.Deck(
        map_style=None,
        initial_view_state=pdk.ViewState(
            latitude=MID_LAT,
            longitude=MID_LONG,
            zoom=4,
            min_zoom=3,
            max_zoom=10,
            pitch=40,
            bearing=-20,
        ),
        layers=[
            pdk.Layer(
                "HexagonLayer",
                data=data,
                get_position="[long, lat]",
                radius=200,
                elevation_scale=4,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
            ),
            pdk.Layer(
                "ScatterplotLayer",
                data=data,
                get_position="[long, lat]",
                get_color="[200, 30, 0, 160]",
                get_radius=200,
            ),
        ],
    )
)




# st.subheader('Number of pickups by hour')
# hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
# st.bar_chart(hist_values)
#
# # Some number in the range 0-23
# hour_to_filter = st.slider('hour', 0, 23, 17)
# filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
#
# st.subheader('Map of all pickups at %s:00' % hour_to_filter)
# st.map(filtered_data)