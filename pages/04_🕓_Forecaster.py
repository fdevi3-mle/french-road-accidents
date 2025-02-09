import streamlit as st

from src.utils import FIGURE_4, FIGURE_5, FIGURE_6, FIGURE_7

st.set_page_config(
    page_title="Forecaster",
    page_icon="☯️",
    layout="wide"
)
st.write("# Time Series Forecaster 🕓")
st.markdown("""
Given the limited computation resources and the prototype nature of the classifier
, I preferred to use a forecaster to predict the annual cycle of accidents . This Time Series
analysis could actually provide spatio-temporal insights into traffic flow control
over the period of the year and coupled with weather and other variables give live
traffic flow control allowing for decrease of fatal accidents.
 The time series models would take into account seasonal changes and the effects of
summer, winter, spring, autumn as well as the effects of weekends and holidays
to see the trend of accidents over time. (see code snippet to encode the seasons)
The forecasting model would take into account these variables to predict the
number of accidents per annual cycle and would be able to create a future
forecast for a user defined period.  All of the data was quite regular except 2020 ,
which can be explained due to the COVID pandemic which occurred during that
period.

```
##Add seasonality and events
# https://neuralprophet.com/how-to-guides/application-examples/energy_tool.html
df["summer"] = 0
df.loc[df["ds"].dt.month.isin([6, 7, 8]), "summer"] = 1
df["winter"] = 0
df.loc[df["ds"].dt.month.isin([12, 1, 2]), "winter"] = 1
df["fall"] = 0
df.loc[df["ds"].dt.month.isin([9, 10, 11]), "fall"] = 1
df["spring"] = 0
df.loc[df["ds"].dt.month.isin([3, 4, 5]), "spring"] = 1

# https://stackoverflow.com/questions/71339576/select-data-based-on-weekday-and-weekend-pandas
df['weekend'] = 0
df.loc[df['ds'].dt.dayofweek.isin([5, 6]), "weekend"] = 1
```
I experimented with two main models as suggested by the literature overview in the form of NeuralProphet and AutoArima with seasonality.
Once we clean, filter and adapt the data we can decompose the data to see its trends, residuals and seasons (see Figure 4)

""")

st.image(FIGURE_4, caption="Figure4: Decomposition of Road Accident data via mode mul ")

left_col,right_col = st.columns(2,border=True)

with left_col:
    st.subheader("Auto Arima with Seasonality")
    st.markdown("""
    The ARIMA model can be summarized by the following code snippet below where the necessary parameters can be seen
        
```
# scorer
mape_scorer = make_scorer(mean_absolute_percentage_error, greater_is_better=False)
model_arima = auto_arima(train[['y']],  test='adf',
                             seasonal=True, m=12, seasonal_test='ocsb',
                             d=None, D=1, n_jobs=-1, random_state=42, scoring=mape_scorer)
```
The model performed relatively well with a Mean Absolute Percentage Error (MAPE) score of under 20 percent which indicates a decent enough forecast
We can see (Figure 5) the real vs forecasted values. The model did a decent job but was scared to tackle the predictions. 
""")
    st.image(FIGURE_5, caption="Figure5: Actual vs Forecasted Accident Predictions Auto Arima")

with right_col:
    st.subheader("Neural Prophet")
    st.markdown("""
    The second and significantly better choice was the NP(“NeuralProphet”) model
which not only had easier features for adding seasonality and regressors but one
could also add holidays to the model for consideration.
The model is constructed as below(just a snippet), where the parameters could be tweaked as
per the score achieved by the forecaster.

```
#https://neuralprophet.com/how-to-guides/application-examples/energy_solar_pv.html
m = NeuralProphet(
        n_changepoints=10,seasonality_mode='multiplicative',
        yearly_seasonality=True,weekly_seasonality=True,
        daily_seasonality=False,
        n_lags=25 )
m = m.add_country_holidays(country_name="FR")
m.add_seasonality(name="summer", period=7, fourier_order=14, condition_name="summer")
m.add_seasonality(name="winter", period=7, fourier_order=14, condition_name="winter")

##Incomplete : See Forecasting-Road-Accident-Notebook
```
The neural prophet on the other hand had a better forecasting fit as seen as from
below (see Figure 6 ). It to achieved a comparable MAPE score of 14-16 percent . One can also see how the other factors influenced the forecaster (see Figure 7)
    """)
    st.image(FIGURE_6, caption="Figure 6: Neural Prophet Predicted vs Actual Road Accidents")
    st.image(FIGURE_7, caption="Figure 7: Neural Prophet Parameters and influence of weekend and holidays")
