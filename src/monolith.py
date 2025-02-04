from typing import Tuple

import joblib
from pmdarima import auto_arima
from sklearn.metrics import mean_absolute_percentage_error, make_scorer
from zenml import step
from zenml.logger import get_logger

from src.franums import RoadAccidentEnum
from src.utils import INPUT_PARQUET, LAT_MIN, LAT_MAX, LONG_MIN, LONG_MAX, TRAIN_DATE_LIMIT, ExtensionMethods, \
    REPORT_PATH, FIGURE_PATH, MODEL_PATH

##setup the logger
logger = get_logger(__name__)

# Concurrency

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


@step
def data_loader(filepath=INPUT_PARQUET):
    if filepath is None:
        filepath = INPUT_PARQUET
    data = pd.read_parquet(filepath)
    valid_columns = RoadAccidentEnum.to_dict()
    valid_columns = valid_columns.keys()
    data = data[[col for col in data.columns if col in valid_columns]]
    logger.info(f'Hey {data.head(1)}')
    return data


# data['accident_hex_count'] = data.groupby('h3')['h3'].transform('count')
# data['date'] = pd.to_datetime(data['datetime']).dt.date

@step
def data_processor(data):
    ##clean missing values
    mega_dic = RoadAccidentEnum.mega_dictionary()
    replacement_dict = {}
    num_cols = []
    cat_cols = []
    for index, value in mega_dic.items():
        if mega_dic[index][1]:
            replacement_dict[index] = value[0]
            cat_cols.append(index)
        else:
            num_cols.append(index)

    ##Num cleaner
    missing_values_num = data[num_cols].isna().sum().sum()
    print("NA values:", missing_values_num)
    if missing_values_num > 0:
        data = data.dropna()

    ##cat cols cleaner
    data[cat_cols] = data[cat_cols].fillna("UNKNOWN")

    ##drop duplicates
    duplicates = data[data.duplicated()]
    num_duplicates = duplicates.shape[0]
    print(f"Number of duplicate rows: {num_duplicates}")
    if num_duplicates > 0:
        data = data.drop_duplicates()

    ##lat lon cleaning # Only Keep mainland france and the tiny island nearby
    mask = (data['lat'] >= LAT_MIN) & (data['lat'] <= LAT_MAX) & (data['long'] >= LONG_MIN) & (data['long'] <= LONG_MAX)
    data = data[mask]

    ##hex count ## Count the number of accidents per h3 hex str
    data['accident_hex_count'] = data.groupby('h3')['h3'].transform('count')

    ## date
    data['date'] = pd.to_datetime(
        data['datetime']).dt.date  ##just incase , the hour processing is too much on the runner

    ##convert to ordinal codes
    data = data.replace(replacement_dict).fillna(0)
    # clean up the stragglers
    for index, value in replacement_dict.items():
        data[index] = pd.to_numeric(data[index])
        data[index] = data[index].replace(-1, 0)

    print(data[cat_cols].head())
    return data


@step
def create_time_series_date(dataset):
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
def train_arima(df) -> Tuple[ARIMA, pd.DataFrame, pd.DataFrame]:
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
def predict_plot(model, train, test) -> Tuple[ARIMA, str]:
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
    # save like txt
    figure_filename = ExtensionMethods.generate_filename('diagnostic_plot', 'png')
    figure_filepath = os.path.join(FIGURE_PATH, figure_filename)
    plt.savefig(figure_filepath, bbox_inches='tight', dpi=300)
    plt.close()

    return model, Path(filename).stem


@step
def save_model(model, model_name='Arima_model'):
    # https://alkaline-ml.com/pmdarima/auto_examples/arima/example_persisting_a_model.html#sphx-glr-auto-examples-arima-example-persisting-a-model-py
    os.makedirs(MODEL_PATH, exist_ok=True)
    filename = ExtensionMethods.generate_filename(model_name, 'pkl')
    filepath = os.path.join(MODEL_PATH, filename)
    joblib.dump(model, filepath, compress=3)
    print(f"Model saved to: {filepath}")
