## COMET ML
from comet_ml import Artifact, start
from comet_ml.integration.sklearn import log_model

comet_classifier_experiment = start(
  api_key="Xh1kXXM0IIPgqwAP3wTyChS0R",
  project_name="french-road-accidents",
  workspace="fdevi3"
)



from typing import Tuple,Annotated
import joblib
from imblearn.over_sampling import SMOTE
from sklearn.base import ClassifierMixin
# GBC
from sklearn.metrics import confusion_matrix
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.preprocessing import StandardScaler
from zenml import step, ArtifactConfig
from zenml.logger import get_logger

from src.franums import RoadAccidentEnum
from src.utils import INPUT_PARQUET, LAT_MIN, LAT_MAX, LONG_MIN, LONG_MAX, ExtensionMethods, \
    REPORT_PATH, MODEL_PATH, EVIDENTLY_TOKEN, EVIDENTLY_PROJECT_CLASSIFIER_ID

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

import os
import pandas as pd

# stats model

os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
##

#evidenly
from evidently.future.datasets import Dataset, BinaryClassification
from evidently.future.datasets import DataDefinition

from evidently.future.report import Report
from evidently.future.presets import *
from evidently.ui.workspace.cloud import CloudWorkspace




@step
def data_loader(filepath=INPUT_PARQUET)->Annotated[pd.DataFrame, "RoadAccidentInputDataFrame"]:
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
    artifact = Artifact(name="RoadAccidentInputDataset", artifact_type="dataset")
    artifact.add(local_path_or_data=INPUT_PARQUET)
    comet_classifier_experiment.log_artifact(artifact)

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


# data['accident_hex_count'] = data.groupby('h3')['h3'].transform('count')
# data['date'] = pd.to_datetime(data['datetime']).dt.date

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


#region GBC
@step
def prepare_train_test_split(data)->Tuple[Annotated[pd.DataFrame,"X_train"], Annotated[pd.DataFrame,"X_test"],Annotated[pd.Series,"y_train"],Annotated[pd.Series,"y_test"]]:
    features = ['vehicle_category', 'obstacle_mobile', 'impact_point', 'action', 'safety_equipment',
                'road_surface', 'speed_limit', 'lum', 'weather', 'collision_type',
                'accident_hex_count']
    target = 'severity'
    #seperate the minor and mjor
    mask = data[target] > 1  # get rid of no injury
    data = data[mask]
    X = data[features]
    y = data[target]
    y = y.map(lambda r: 1 if r >= 3 else 0) # Major {Major+Killed}

    ordinal_features = ['vehicle_category', 'obstacle_mobile', 'impact_point', 'action',
                        'safety_equipment', 'road_surface',  'lum', 'weather',
                        'collision_type']
    for col in ordinal_features:
        X[col] = X[col].replace(-1, 0).astype(int)


    ##Smote for minority class
    smote = SMOTE()
    X_resampled, y_resampled = smote.fit_resample(X, y)
    X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.2,
                                                        random_state=random_state)
    ##scaling
    scaler = StandardScaler()
    num_features = ['speed_limit', 'accident_hex_count']
    X_train[num_features] = scaler.fit_transform(X_train[num_features])
    X_test[num_features] = scaler.transform(X_test[num_features])

    return X_train, X_test, y_train, y_test

@step
def gradboost_classifier(X_train, X_test, y_train, y_test)->Annotated[ClassifierMixin,ArtifactConfig(name="GradientBoostingClassifier",tags=['classifier','gbc'])]:

    #setup neptune
    run = neptune.init_run(
        project="France-Road-Accidents-Test/SeverityClassifier",
        api_token="eyJhcGlfYWRkcmVzcyI6Imh0dHBzOi8vYXBwLm5lcHR1bmUuYWkiLCJhcGlfdXJsIjoiaHR0cHM6Ly9hcHAubmVwdHVuZS5haSIsImFwaV9rZXkiOiI0ZmQ1NTFlMi02ZTc0LTQyOTgtOTZjZC1kNGU5ODllOWM0ODEifQ==",
    )
    ##kinda stupid to put the api token in code but its the neptune ai instructions

    params = {
        'n_estimators': [1,2,3], ##change for higher iter , it can take over 30 mins for more than 200, and other learning rates, beware
        'max_depth': [5,7,10],
        'learning_rate': [0.01,0.1,0.5,1],
        'max_features': ['auto', 'sqrt', 'log2']
    }
    ##CV=5 takes too long 
    random_search = RandomizedSearchCV(GradientBoostingClassifier(random_state=random_state), cv=3, n_jobs=-1, verbose=2, param_distributions=params)
    random_search.fit(X_train, y_train)
    print(f"The best parameters: {random_search.best_params_}")
    run["parameters"] = random_search.best_params_

    best_est = random_search.best_estimator_
    y_pred = best_est.predict(X_test)

    report = classification_report(y_test, y_pred, output_dict=True)
    _df = pd.DataFrame(report).transpose()

    #where to save
    xls_filename = ExtensionMethods.generate_filename("GradientBoostingClassifier", 'xls')
    xls_filepath = os.path.join(REPORT_PATH, xls_filename)
    _df.to_csv(xls_filepath, index=True)



    run["classifier"] = npt_utils.create_classifier_summary(
        best_est, X_train, X_test, y_train, y_test)
    run.stop()
    return best_est


@step
def evidently_classifier_monitoring(X_train, X_test, y_train, y_test, model):
    ws = CloudWorkspace(token=EVIDENTLY_TOKEN, url="https://app.evidently.cloud")
    project = ws.get_project(EVIDENTLY_PROJECT_CLASSIFIER_ID)

    X_train['prediction'] = model.predict(X_train)
    X_train['target'] = y_train

    train_data = Dataset.from_pandas(
        pd.DataFrame(X_train),
        data_definition=DataDefinition(classification=[BinaryClassification(target="target", prediction_labels="prediction")])
    )

    X_test['prediction'] = model.predict(X_test)
    X_test['target'] = y_test

    test_data = Dataset.from_pandas(
        pd.DataFrame(X_test),
        data_definition=DataDefinition(
            classification=[BinaryClassification(target="target", prediction_labels="prediction")])
    )

    report = Report([
        DataSummaryPreset(),
        DataDriftPreset(),
        ClassificationPreset(),

    ])
    my_eval = report.run(train_data,test_data)
    ws.add_run(project.id, my_eval)


@step
def comet_ml_classifier(X_test,y_test,gbc_model):
    y_pred = gbc_model.predict(X_test)
    report = classification_report(y_test,y_pred,output_dict=True)
    comet_classifier_experiment.log_parameters(gbc_model.get_params())
    comet_classifier_experiment.log_metrics(report)
    matrix = confusion_matrix(y_test, y_pred)
    comet_classifier_experiment.log_confusion_matrix(matrix=matrix)
    log_model(comet_classifier_experiment, model=gbc_model, model_name="GradientBoostingClassifier")

    #register model
    comet_classifier_experiment.register_model(model_name="GradientBoostingClassifier")
