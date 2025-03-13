import logging
import os

from zenml import pipeline
from zenml.client import Client

from src.classifier_monolith import prepare_train_test_split, gradboost_classifier, comet_ml_classifier, \
    evidently_classifier_monitoring
from src.common_monolith import data_loader_common, data_validator, log_dataset, drift_monitor, data_processor, \
    save_model
from src.forecast_monolith import create_time_series_date, train_arima, predict_plot, evidently_forecaster_monitoring, \
    comet_ml_forecaster
from src.utils import ARIMA_NAME, GBC_NAME, NEPTUNE_FORECAST_PROJECT, NEPTUNE_CLASSIFIER_PROJECT, \
    COMET_FORECAST_PROJECT_NAME, COMET_WORKSPACE, EVIDENTLY_PROJECT_FORECAST_ID

##Activate logger and client
logger = logging.getLogger(__name__)
logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)

os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

# Zenml Client
client = Client()
Client().activate_stack("default")


@pipeline(enable_cache=True)
def mega_pipeline():
    logger.info(f"Starting the Dataloader Step")
    dataset = data_loader_common()

    logger.info("Starting the Data Validation Set")
    data_validator(dataset)

    logger.info(f"Logging the Input Datasset as Artifacts")
    log_dataset(dataset)

    logger.info(f"Starting the Data Drifter Step")
    drift_monitor(dataset)

    logger.info(f"Starting the Data processor step")
    data_processed = data_processor(dataset)

    logger.info(f"Starting the Split Step")
    X_train, X_test, y_train, y_test = prepare_train_test_split(data_processed)

    logger.info(f"Starting the Classifier Step")
    gbc_model = gradboost_classifier(X_train, X_test, y_train, y_test)

    logger.info(f"Saving the model")
    _gbc_name = GBC_NAME
    _gbc_filepath = save_model(gbc_model, _gbc_name)

    logger.info("Starting the Comet ML Logging")
    comet_ml_classifier(X_test, y_test, gbc_model, _gbc_filepath)

    logger.info(f"Starting the Time series step")
    ts = create_time_series_date(data_processed)

    logger.info(f"Training the Time series step")
    arima_model, forecast_train, forecast_test = train_arima(ts)

    logger.info(f"Plotting the time series predictions")
    arima_model, name = predict_plot(arima_model, forecast_test)

    logger.info(f"Saving the model")
    _arima_name = ARIMA_NAME
    _arima_filepath = save_model(arima_model, _arima_name)

    logger.info(f"Evidently Classifier")
    evidently_classifier_monitoring(X_train, X_test, y_train, y_test, gbc_model)

    logger.info("Evidently Forecasting")
    evidently_forecaster_monitoring(valid=forecast_test, model=arima_model)

    logger.info("Comet Ml Forcasting Logging")
    comet_ml_forecaster(forecast_test, arima_model, _arima_filepath)


def _dont_use_for_test_only():
    ''' DONT USE THIS.Just a stupid DataScientest scam requirement'''
    ## basically since we need too retrain ,I need to call teh pipeline again. and one way to call it is via load module which
    ## is inherently dumb and unsafe. A more production way is assuming that this is on a server , a listener that triggers an event of retraining
    # where the pipeline trigger shown below has status updates to avoid simulatenous pipeline triggers or seperate workers than can seperately trigger pipelines.
    mega_pipeline()


def print_stuff():
    print(f"NEPTUNE_FORECAST_PROJECT : {NEPTUNE_FORECAST_PROJECT}")
    print(f"COMET_FORECAST_PROJECT_NAME  : {COMET_FORECAST_PROJECT_NAME}")
    print(f"COMET_WORKSPACE   : {COMET_WORKSPACE}")
    print(f"EVIDENTLY_PROJECT_FORECAST_ID   : {EVIDENTLY_PROJECT_FORECAST_ID}")


if __name__ == "__main__":
    print_stuff()

### DEAD CODE
# @pipeline(enable_cache=False)  # This function combines steps together
# def time_series_pipeline():
#     logger.info(f"Starting the Dataloader Step")
#     dataset = data_loader()
#
#     logger.info(f"Starting the Data processor step")
#     data_processed = data_processor(dataset)
#
#     logger.info(f"Starting the Data Analyser step")
#     ts = create_time_series_date(data_processed)
#
#     a, b, c = train_arima(ts)
#     model, name = predict_plot(a, b, c)
#     # print(a.summary())
#
#     # logger.info(f"Starting the Model Training step")
#     # model = time_series(data_processed)
#     # predict_plot(model)
#     #
#     logger.info(f"Saving the model")
#     save_model(model, name)
#     logger.info(f"All steps finished")
#
# @pipeline(enable_cache=False)
# def classifier_pipeline():
#     logger.info(f"Starting the Dataloader Step")
#     dataset = data_loader()
#
#     logger.info(f"Starting the Data processor step")
#     data_processed = data_processor(dataset)
#
#     logger.info(f"Starting the Split Step")
#     X_train,X_test,y_train,y_test = prepare_train_test_split(data_processed)
#
#     logger.info(f"Starting the Classifier Step")
#     model = gradboost_classifier(X_train,X_test,y_train,y_test)
#
#     logger.info(f"Saving the model")
#     save_model(model, "GradientBoostingClassifier")
#
#
# @pipeline(enable_cache=True)
# def data_pipeline():
#     logger.info(f"Starting the Dataloader Step")
#     dataset = data_loader()
#
#     logger.info(f"Starting the Data Drifter Step")
#     drift_monitor(dataset)
#
#     logger.info(f"Starting the Data processor step")
#     data_processed = data_processor(dataset)
#
# @pipeline(enable_cache=True)
# def classifier_pipeline_test():
#
#     data_processed = client.get_artifact_version(
#         name_id_or_prefix="RoadDataProcessed")
#
#     logger.info(f"Starting the Split Step")
#     X_train, X_test, y_train, y_test = prepare_train_test_split(data_processed)
#
#     logger.info(f"Starting the Classifier Step")
#     model = gradboost_classifier(X_train, X_test, y_train, y_test)
#
#     logger.info(f"Saving the model")
#     save_model(model, "GradientBoostingClassifier")
#
#
# @pipeline(enable_cache=True)  # This function combines steps together
# def time_series_pipeline_test():
#     data_processed = client.get_artifact_version(
#         name_id_or_prefix="RoadDataProcessed")
#
#     logger.info(f"Starting the Data Analyser step")
#     ts = create_time_series_date(data_processed)
#
#     a, b, c = train_arima(ts)
#     model, name = predict_plot(a, b, c)
#
#     logger.info(f"Saving the model")
#     save_model(model, name)
#     logger.info(f"All steps finished")
