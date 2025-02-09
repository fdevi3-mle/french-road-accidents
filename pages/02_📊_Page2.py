import logging
import os
import streamlit as st
import pandas as pd
import plotly.express as px
from plotly_resampler import register_plotly_resampler


from src.franums import RoadAccidentEnum
from src.utils import INPUT_PARQUET, MID_LONG, MID_LAT, IMG_SCATTER_MERGED, PARQUET_2019, PARQUET_2020, PARQUET_2021, \
    PARQUET_2022, PARQUET_2023, MAPBOX_TOKEN, LONG_MAX, LAT_MIN,LAT_MAX,LONG_MIN

#Logger
logger = logging.getLogger(__name__)
##Use cpu only
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

#plotly resampler
register_plotly_resampler(mode='auto')

##dic
year_dic = {
    2019 : PARQUET_2019,
    2020 : PARQUET_2020,
    2021 : PARQUET_2021,
    2022 : PARQUET_2022,
    2023 : PARQUET_2023
}

col_list = []

st.set_page_config(
    page_title="Data Analyis",
    page_icon="📊",
    layout="wide"
)



##Methods
@st.cache_data
def get_columns():
    l = []
    a = RoadAccidentEnum.mega_dictionary()
    for index,value in a.items():
        if a[index][1]:
            l.append(index)
    return l





@st.cache_data
def data_loader(filepath=INPUT_PARQUET, year=2019):
    if filepath is None:
        filepath = INPUT_PARQUET
    if year is None:
        year = 2019
    filepath = year_dic[year]
    df = pd.read_parquet(filepath)
    st.write(f"{year}")
    valid_columns = RoadAccidentEnum.to_dict()
    valid_columns = valid_columns.keys()
    df = df[[col for col in df.columns if col in valid_columns]]

    # ## BLOCKER FOR SAMPLE SIZE
    # if sample_size >0.25:
    #     sample_size = 0.25 ## just a block as streamlit cant handle large data
    # logger.info(f" Creating a Random Sample of {sample_size * 100}% of data")
    # df = df.sample(frac=sample_size, random_state=42)
    return df

### Streamlit

# if 'dataframe' not in st.session_state:
#     # Get the data if you haven't
#     data = data_loader()
#     st.text('Loading data...')
#     # Save the data to session state
#     st.session_state.dataframe = data
# else:
#     data = st.session_state.dataframe
#     st.text('Loaded data...')

if 'col_list' not in st.session_state or len(col_list)<=0:
    col_list = get_columns()

if "selected_year" not in st.session_state:
    st.session_state.selected_year = 2019  # Default year



selected_year = st.sidebar.selectbox(
    "Select Year",
    options=year_dic.keys(),
    key="selected_year",
    on_change=data_loader
)

data = data_loader(year=selected_year)

##Add 2 colims for neat layout
main_col,right_col = st.columns((4, 1))
with main_col:
    st.markdown(f"## Road Accident Data for year {selected_year}")

    # Scatter Mapbox without Plotly Resampler
    fig = px.scatter_mapbox(data,lat="lat",lon="long",zoom=4,mapbox_style="carto-positron",
                            opacity=0.5,animation_group=data['datetime'].dt.year,
                            center = dict(lat=MID_LAT, lon=MID_LONG))

    fig.update_traces(marker=dict(size=2, color='#e57373', opacity=0.3))
    fig.update_layout(mapbox_accesstoken=MAPBOX_TOKEN,
                      map_bounds={"west": LONG_MIN, "east": LONG_MAX, "south": LAT_MAX, "north": LAT_MIN})

    st.plotly_chart(fig, use_container_width=True)


with right_col:
    option = st.selectbox("Select Variable",options=col_list,
        # index=None,
        # placeholder="Select variable..",
        # label_visibility=st.session_state.visibility
    )

    st.write("You selected:", option)







