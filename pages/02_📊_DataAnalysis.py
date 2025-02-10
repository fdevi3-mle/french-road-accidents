import logging
import os
import streamlit as st
import pandas as pd
import plotly.express as px
from plotly_resampler import register_plotly_resampler


from src.franums import RoadAccidentEnum
from src.utils import INPUT_PARQUET, MID_LONG, MID_LAT, PARQUET_2019, PARQUET_2020, PARQUET_2021, \
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
    page_title="Data Analysis",
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

    valid_columns = RoadAccidentEnum.to_dict()
    valid_columns = valid_columns.keys()
    df = df[[col for col in df.columns if col in valid_columns]]
   # df['accident_hex_count'] = df.groupby('h3')['h3'].transform('count') ## too heavy
    df['date'] = pd.to_datetime(df['datetime']).dt.date
    return df


@st.cache_data
def time_loader(df):
    columns_to_keep = ['date', 'accident_id']
    filtered_columns = [col for col in columns_to_keep if col in data.columns]
    time_df = (
        data[filtered_columns]
        .groupby('date')
        .agg({
            'accident_id': 'count'
        })
        .rename(columns={'accident_id': 'accident_count'})
        .reset_index()
    )
    return time_df


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
main_col,right_col = st.columns((5,2),border=True)
with main_col:
    st.markdown(f"## Road Accident Data for year {selected_year}")


    fig = px.scatter_mapbox(data,lat="lat",lon="long",zoom=4,mapbox_style="carto-positron",
                            opacity=0.5,center = dict(lat=MID_LAT, lon=MID_LONG))

    fig.update_traces(marker=dict(size=2, color='#e57373', opacity=0.3))
    fig.update_layout(mapbox_accesstoken=MAPBOX_TOKEN,
                      map_bounds={"west": LONG_MIN, "east": LONG_MAX, "south": LAT_MAX, "north": LAT_MIN})

    st.plotly_chart(fig, use_container_width=True, height=1000)

    ##Add a time series
    time_df = time_loader(data)
    time_fig = px.line(time_df,x='date', y='accident_count')
    st.plotly_chart(time_fig, use_container_width=True,height=700)

with right_col:
    pie_variable = st.selectbox("Select Variable",options=col_list,
        placeholder="Select variable..")

    filtered_data_pie = data[pie_variable]
    filtered_data_pie = filtered_data_pie.replace(-1,"UNKNOWN")
    pie_fig = px.pie(filtered_data_pie,names=pie_variable)
    pie_fig.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(pie_fig, use_container_width=True)

    hist_fig = px.histogram(filtered_data_pie, x=pie_variable,marginal="violin")
    st.plotly_chart(hist_fig, use_container_width=True)


# st.subheader('Data Analysis of Road Accidents')
# st.markdown("""
# The data was selected from the years 2019-2023 from the [Interior Ministry of France](https://www.data.gouv.fr/fr/datasets/53698f4ca3a729239d2036df/).
# The data was divided into 4 main Files namely
# + Users.csv
# + Places.csv
# + Vehicles.csv
# + Characteristics.csv
#
# The data was in french [^1] and once translated and decoded we can visualize the distribution of certain Categorical Variables.
# We can see that some variables are quite imbalanced and this would affect any ML models we build.
#
# [^1]: The DS team should have provided a translation, the translation being present as evident from MC8 SQL : where the same reused and english translated dataset was used.
# """)





