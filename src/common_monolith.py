## COMET ML
from comet_ml import Artifact, start
from comet_ml.integration.sklearn import log_model




from typing import Tuple,Annotated
import joblib
from imblearn.over_sampling import SMOTE
from pmdarima import auto_arima
from sklearn.base import ClassifierMixin
# GBC
from sklearn.metrics import confusion_matrix
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import classification_report
from sklearn.metrics import mean_absolute_percentage_error, make_scorer
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.preprocessing import StandardScaler
from zenml import step, ArtifactConfig
from zenml.logger import get_logger

from src.franums import RoadAccidentEnum
from src.utils import INPUT_PARQUET, LAT_MIN, LAT_MAX, LONG_MIN, LONG_MAX, TRAIN_DATE_LIMIT, ExtensionMethods, \
    REPORT_PATH, FIGURE_PATH, MODEL_PATH, EVIDENTLY_TOKEN, EVIDENTLY_PROJECT_CLASSIFIER_ID, \
    EVIDENTLY_PROJECT_FORECAST_ID

##setup the logger
logger = get_logger(__name__)

# Neptune AI
import neptune
import neptune.integrations.sklearn as npt_utils


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
from evidently.future.datasets import Dataset, BinaryClassification, Regression
from evidently.future.datasets import DataDefinition

from evidently.future.report import Report
from evidently.future.presets import *
from evidently.ui.workspace.cloud import CloudWorkspace


@step
def data_loader_common(filepath=INPUT_PARQUET)->Annotated[pd.DataFrame, "RoadAccidentInputDataFrame"]:
    if filepath is None:
        filepath = INPUT_PARQUET
    data = pd.read_parquet(filepath)
    valid_columns = RoadAccidentEnum.to_dict()
    valid_columns = valid_columns.keys()
    data = data[[col for col in data.columns if col in valid_columns]]
    logger.info(f'Hey {data.head(1)}')
    return data

@step
def log_dataset(data):
    comet_experiment = start(
        api_key="Xh1kXXM0IIPgqwAP3wTyChS0R",
        project_name="french-road-accidents",
        workspace="fdevi3"
    )
    artifact = Artifact(name="RoadAccidentInputDataset", artifact_type="dataset")
    artifact.add(local_path_or_data=INPUT_PARQUET)
    comet_experiment.log_artifact(artifact)
    comet_experiment.end()

@step
def drift_monitor(data):
    ws = CloudWorkspace(token=EVIDENTLY_TOKEN, url="https://app.evidently.cloud")
    project = ws.get_project(EVIDENTLY_PROJECT_CLASSIFIER_ID)

    mid_point = len(data) // 2
    data1 = data[:mid_point]
    data2 = data[mid_point:]
    eval_data1 = Dataset.from_pandas(
        pd.DataFrame(data1),
        data_definition=DataDefinition()
    )
    eval_data2 = Dataset.from_pandas(
        pd.DataFrame(data2),
        data_definition=DataDefinition()
    )
    report = Report([
        DataSummaryPreset(),
        DataDriftPreset(),
    ],
        include_tests="True")
    my_eval = report.run(eval_data1,eval_data2)
    ws.add_run(project.id, my_eval)


@step
def data_processor(data)->Annotated[pd.DataFrame, "RoadDataProcessed"]:
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
def save_model(model, model_name='Default'):
    # https://alkaline-ml.com/pmdarima/auto_examples/arima/example_persisting_a_model.html#sphx-glr-auto-examples-arima-example-persisting-a-model-py
    os.makedirs(MODEL_PATH, exist_ok=True)
    filename = ExtensionMethods.generate_filename_only(model_name, 'pkl')
    filepath = os.path.join(MODEL_PATH, filename)
    joblib.dump(model, filepath, compress=3)
    print(f"Model saved to: {filepath}")

