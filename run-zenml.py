import logging
import os

import joblib
from zenml import pipeline
from zenml.client import Client

# stps
from src.monolith import data_loader, drift_monitor, data_processor, prepare_train_test_split, gradboost_classifier, \
    save_model, create_time_series_date, train_arima, predict_plot, evidently_classifier_monitoring, \
    evidently_forecaster_monitoring, log_dataset, comet_ml_classifier
from src.utils import INPUT_PARQUET, MODEL_PATH, ExtensionMethods

from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import classification_report
from sklearn.metrics import mean_absolute_percentage_error, make_scorer
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.preprocessing import StandardScaler

##Activate logger and client
logger = logging.getLogger(__name__)
logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)

os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

# Zenml Client
client = Client()
Client().activate_stack(
    "default"
)




# def comet_ml_log_classifier(X_test,y_test,model_name):
#     filename= ExtensionMethods.generate_filename_only(model_name,'pkl')
#     filepath = os.path.join(MODEL_PATH,filename)
#
#     if not os.path.exists(filepath):
#         raise FileNotFoundError(f"GBC Model file not found at {filepath}")
#
#     gbc_model = joblib.load(filepath)
#     ## CometML
#     y_pred = gbc_model.predict(X_test)
#     report = classification_report(y_test,y_pred)
#
#     comet_experiment.log_parameters(gbc_model.get_params())
#
#     comet_experiment.log_metrics(report)
#
#     matrix = confusion_matrix(y_test, y_pred)
#     print(matrix)
#
#     # Log the confusion matrix to Comet
#     comet_experiment.log_confusion_matrix(matrix=matrix)
#
#     # Seamlessly log your SKLearn model
#     log_model(comet_experiment, model=gbc_model, model_name="GradientBoostingClassifier")


@pipeline(enable_cache=True)
def mega_pipeline():
    logger.info(f"Starting the Dataloader Step")
    dataset = data_loader()

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
    _gbc_name = "GradientBoostingClassifier"
    save_model(gbc_model,_gbc_name)

    logger.info("Starting the Comet ML Logging")
    comet_ml_classifier(X_test,y_test,gbc_model)

    logger.info(f"Starting the Time series step")
    ts = create_time_series_date(data_processed)

    logger.info(f"Training the Time series step")
    arima_model, forecast_train, forecast_test = train_arima(ts)

    logger.info(f"Plotting the time series predictions")
    arima_model, name = predict_plot(arima_model,forecast_test)

    logger.info(f"Saving the model")
    _arima_name = "ARIMA"
    save_model(arima_model, _arima_name)

    logger.info(f"Evidently Classifier")
    evidently_classifier_monitoring(X_train, X_test, y_train, y_test, gbc_model)

    logger.info("Evidently Forecasting")
    evidently_forecaster_monitoring(valid =forecast_test,model=arima_model)

if __name__ == "__main__":
    mega_pipeline()



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