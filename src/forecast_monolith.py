## COMET ML
from comet_ml import start
from comet_ml.integration.sklearn import log_model

# comet_forecast_experiment = start(
#   api_key="Xh1kXXM0IIPgqwAP3wTyChS0R",
#   project_name="french-forecaster",
#   workspace="fdevi3"
# )
#


from typing import Tuple,Annotated
import joblib
from pmdarima import auto_arima
# GBC
from sklearn.metrics import mean_absolute_percentage_error, make_scorer
from zenml import step
from zenml.logger import get_logger

from src.franums import RoadAccidentEnum
from src.utils import INPUT_PARQUET, LAT_MIN, LAT_MAX, LONG_MIN, LONG_MAX, TRAIN_DATE_LIMIT, ExtensionMethods, \
    REPORT_PATH, FIGURE_PATH, MODEL_PATH, EVIDENTLY_TOKEN, EVIDENTLY_PROJECT_FORECAST_ID

##setup the logger
logger = get_logger(__name__)

# Neptune AI
import neptune

#  Warnings
import warnings

warnings.filterwarnings('ignore')

# Set random state
random_state = 42

import matplotlib.pyplot as plt
import os
from pathlib import Path
import pandas as pd

# stats model
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller

os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
##
from pmdarima import ARIMA

#evidenly
from evidently.future.datasets import Dataset, Regression
from evidently.future.datasets import DataDefinition

from evidently.future.report import Report
from evidently.future.presets import *
from evidently.ui.workspace.cloud import CloudWorkspace


@step
def create_time_series_date(dataset)->Annotated[pd.DataFrame,"TimeSeriesDataFrame"]:
    columns_to_keep = ['date', 'accident_id', 'road_surface', 'weather', 'lum']
    filtered_columns = [col for col in columns_to_keep if col in dataset.columns]

    ## groups the accidents and selects some features which I want to use as regressors depending on hr or daily check
    df = (
        dataset[filtered_columns]
        .groupby('date')
        .agg({
            'accident_id': 'count',
            'road_surface': 'max',
            'lum': 'mean',
            'weather': 'max',
        })
        .rename(columns={'accident_id': 'accident_count'})
        .reset_index()
    )

    ##rename as prophet and other time series analysers like it as ds and y
    df = df.rename(columns={'accident_count': 'y', 'date': 'ds'})
    df['ds'] = pd.to_datetime(df['ds'], format='%Y-%m-%d', errors='coerce')

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

    print(df.columns)
    print(df.head())
    return df


@step
def time_series_analyser(df):
    ##TODO: Dont need it for the pipeline . Add later to autocreate graphs and pngs
    model_dic = {}
    data = df[['ds', 'y']]
    data = data.set_index('ds')

    ##Perform stationary check
    result = adfuller(data['y'], autolag='AIC')
    print(f'ADF Statistic: {result[0]}')
    print(f'p-value: {result[1]}')
    print(f"  - Stationary: {'Yes' if result[1] < 0.05 else 'No'}")
    model_dic['Stationary'] = result[1] < 0.05

    ## perform seasonal decompose and save png
    decompose = seasonal_decompose(data, model='additive')
    model_dic['additive'] = float(decompose.resid.var())
    decompose = seasonal_decompose(data, model='multiplicative')
    model_dic['multiplicative'] = float(decompose.resid.var())
    print(model_dic)


@step
def train_arima(df) -> Tuple[Annotated[ARIMA,"ARIMA"], pd.DataFrame, pd.DataFrame]:
    '''Check the best arima model to predict& forecast'''
    df['ds'] = pd.to_datetime(df['ds'], format='%Y-%m-%d', errors='coerce')
    df = df[['ds', 'y']]

    ##date https://stackoverflow.com/questions/51474263/typeerror-cannot-compare-type-timestamp-with-type-date
    end_date = TRAIN_DATE_LIMIT
    mask = df['ds'] <= end_date
    train = df[mask]
    val = df[~mask]

    # scorer
    mape_scorer = make_scorer(mean_absolute_percentage_error, greater_is_better=False)
    model_arima = auto_arima(train[['y']], start_p=1, start_q=1, test='adf',
                             seasonal=True, m=12, seasonal_test='ocsb',
                             d=None, D=1,
                             trace=True,
                             error_action='ignore',
                             suppress_warnings=True,
                             stepwise=True,
                             maxiter=1,##change higher for real
                             start_P=0, n_jobs=-1, random_state=42, scoring=mape_scorer)

    return model_arima, train, val


@step
def predict_plot(model, test) -> Tuple[ARIMA, str]:
    ##neptune
    run = neptune.init_run(
        project="fdevi3-time/RoadAcccidentForecast",
        api_token="eyJhcGlfYWRkcmVzcyI6Imh0dHBzOi8vYXBwLm5lcHR1bmUuYWkiLCJhcGlfdXJsIjoiaHR0cHM6Ly9hcHAubmVwdHVuZS5haSIsImFwaV9rZXkiOiJkZTIwYzE5My1mYTY1LTQ4OTQtYjRjYy0yNDMwNzliOTQzODAifQ==",
    )  # your credentials

    forecast = model.predict(n_periods=len(test))
    mape_score = mean_absolute_percentage_error(test['y'], forecast)
    print(f"MAPE for time series score: {mape_score}")

    ##save results
    os.makedirs(REPORT_PATH, exist_ok=True)
    os.makedirs(FIGURE_PATH, exist_ok=True)
    filename = ExtensionMethods.generate_filename('forecast_arima_results', 'log')
    filepath = os.path.join(REPORT_PATH, filename)

    with open(filepath, 'w') as f:
        f.write(f"MAPE for time series score: {mape_score}\n\n")
        f.write("Model Summary:\n")
        f.write(model.summary().as_text())

        ##save images
    plt.figure(figsize=(20, 20))
    plt.plot(test['ds'], test['y'], label='Actual', color='blue')
    plt.plot(test['ds'], forecast, label='Forecast', color='red')
    plt.title('Actual vs. Forecasted Accidents')
    plt.xlabel('Date')
    plt.ylabel('No')
    plt.legend()
    # save the plot

    figure_filename = ExtensionMethods.generate_filename('diagnostic_plot', 'png')
    figure_filepath = os.path.join(FIGURE_PATH, figure_filename)
    plt.savefig(figure_filepath, bbox_inches='tight', dpi=300)
    plt.close()

    run["plots/time_series_plot"].upload(figure_filepath)

    ##Log model stuff
    run['model/dic'] = model.to_dict()
    ##Log the mape score
    run["score/mape_score"] = mape_score

    ##Stop neptune
    run.stop()

    return model, Path(filename).stem


@step
def evidently_forecaster_monitoring(valid, model):
    evi_ws = CloudWorkspace(token=EVIDENTLY_TOKEN, url="https://app.evidently.cloud")
    project = evi_ws.get_project(EVIDENTLY_PROJECT_FORECAST_ID)
    cols = ['ds','y']
    valid = valid[cols]

    ## Regression test stuff for the future forecast
    valid['y'] = valid['y'].astype(float)
    valid['prediction'] = model.predict(n_periods=len(valid))
    valid['prediction'] = valid['prediction'].astype(float)

    definition = DataDefinition(
        numerical_columns=['y','prediction'],
        datetime_columns=['ds'],
        timestamp='ds',
        regression=[Regression(target='y', prediction='prediction')]
    )

    valid_data = Dataset.from_pandas(valid,
        data_definition=definition
    )
    report = Report([
        RegressionPreset()
    ])
    _eval = report.run(valid_data)
    evi_ws.add_run(project.id, _eval)


@step
def comet_ml_forecaster(valid,arima_model):
    comet_forecast_experiment = start(
        api_key="Xh1kXXM0IIPgqwAP3wTyChS0R",
        project_name="french-forecaster",
        workspace="fdevi3"
    )
    cols = ['ds', 'y']
    valid = valid[cols]

    ## Regression test stuff for the future forecast
    valid['y'] = valid['y'].astype(float)
    forecast = arima_model.predict(n_periods=len(valid))

    mape_score = mean_absolute_percentage_error(valid['y'], forecast)
    print(f"MAPE for time series score: {mape_score}")

    comet_forecast_experiment.log_metric("mape_score",mape_score)

    log_model(
        experiment=comet_forecast_experiment,
        model_name="Forecast-Arima-Model",
        model=arima_model,
    )


    # register model
    comet_forecast_experiment.register_model(model_name="Forecast-Arima-Model")
    comet_forecast_experiment.end()