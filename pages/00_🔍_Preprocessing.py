import streamlit as st

from src.utils import FIGURE_13, FIGURE_12, FIGURE_14

st.set_page_config(
    page_title="Preprocessing & Feature Engineering",
    page_icon="🔍",
    layout="wide"
)
st.write("# Preprocessing & Feature Engineering 🔍")
st.markdown("""
## Framework of the Data:
+ The Data was from the years 2019-2023 [Ministry of Interior](https://www.data.gouv.fr/fr/datasets/53698f4ca3a729239d2036df/)
+ The data was over 200MB in an uncompressed csv format and consisted of over 500k values .
+ The data was also split into 4 subsets called (users, vehicles, characteristics, places)  which was then merged to make it easier to deal with.
+ The Data was in French with categories encoded without decoding notes [^1]

We first dealt with the `csv` files and their heavy file size by using a `parquet` [^2] which dropped the file size down to a few MB's 
Most time in the beginning was spent in deciphering what these codes stand for. Once deciphered we realized that the variable that was significant was grav which indicated the severity of the accident.
Our first task was to convert the understandable and translated variables into a human readable form. We achieved that by creating a custom Enum class `RoadAccidentEnum` that held the values of the coded variables(See code snippet below)[^3]

######
```
class Old_Road_Accident_Enum(FileTypeEnum):
    '''Collection of all the categories for file type 'RoadAccidentData' '''

    class Num_Acc(CategoryBaseEnum):
        '''The Index/Number of the Crash follows the pattern yyyyxxxxx where yyyy is the year''

    class id_vehicule(CategoryBaseEnum):
        '''The vehicle id  in terms of xxx-xxx'''

    class catv(CategoryBaseEnum):  # catv Vehicle Category
        '''The Category of Vehicle involved in the crash'''
        UNDETERMINED = 0
        BICYCLE = 1
        MOPED_LESS_EQUAL_50CC = 2
        MICROCAR = 3
        TOURISM_VEHICLE = 7
        HEAVY_TRUCK_PTAC_OVER_7_5T = 14
        HEAVY_TRUCK_OVER_3_5T_WITH_TRAILER = 15
        TRACTOR_ONLY = 16
        TRACTOR_WITH_SEMI_TRAILER = 17
        SPECIAL_VEHICLE = 20
        AGRICULTURAL_TRACTOR = 21 ## this goes on and on....
```
######
The translations helped us decide the columns which made the most sense that would influence the target variable of `severity`.
The dataset was of course converted to english variables with decipherable names which would make it easier to perform further EDA[^4] and other visualizations.
```
class severity(CategoryBaseEnum):
        ''' Severity of the accident'''
        UNKNOWN = 0
        NO_INJURY = 1
        KILLED = 2
        INJURED_HOSPITALIZED = 3
        MINOR_INJURY = 4
```
## Pre-processing and feature engineering:
The translations helped dealing with which features could be selected based on common sense. 
The data being merged had over 40 variables and over 500k values and after the common preprocessing and data cleaning techniques we were able to get rid of unclean data [^5]

## Imbalance and Dealing with Categories
The  dataset was quite imbalanced especially the target variable `severity` (see Figures below) and in this case it would be hard to predict the extreme fatalities without sampling methods that address the imbalance.
For columns that had greater categories , the imbalance was quite evident and it made 
sense to group these categories together
and create major categories to help create manageable variables. 
This idea of simplification for the variables led us to create a cluster of categories into manageable formats (See code snippet below). 
For eg, `catv` which represents _Vehicle Category_ shown above(see Figures below and Old enum above)[^6] had over _10+_ categories for every vehicle type and it made sense to group the categories


```
class vehicle_category(CategoryBaseEnum):  
        '''The Category of Vehicle involved in the crash'''
        UNKNOWN = 0
        LIGHT = 1
        MEDIUM = 2
        HEAVY = 3
        MISC = 4
```
Once the recoding was done (See Data Analysis page for visualization) , it was time to move on to what I believe was the most important feature the GPS co-ordinates.
[^1]: Wasteful time was spent decoding this instead of the DS team providing an already available decoded data (See MC 8 SQL and Module : Wands&Biases)
[^2]: https://arrow.apache.org/docs/python/parquet.html
[^3]: Just code testing, I wanted a coded dictionary . A sep `json` file would have worked as well 
[^4]: Exploratory Data Analysis.
[^5]: Eg: Dropping Duplicates, Absurd values, see code for better understanding.
[^6]: KDE plot below(L) is for year 2023 
""")

st.write("#####")
left_col,middle_col,right_col = st.columns(3,border=True)

with left_col:
    st.image(FIGURE_14, caption="Figure : Distribution of Severity of Road Accidents")

with middle_col:
    st.image(FIGURE_13, caption="Figure : Distribution of Old Catv (Vehicle Categories) yr:2023")

with right_col:
    st.image(FIGURE_12, caption="Figure : Reorganized Vehicle Categories yr:all")
