import logging
import os

from zenml import pipeline
from zenml.client import Client

# stps
from src.monolith import data_loader
from src.utils import INPUT_PARQUET

##Activate logger and client
logger = logging.getLogger(__name__)
logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)

os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

# Zenml Client
client = Client()
Client().activate_stack(
    "default"
)

## COMET ML
from comet_ml import Artifact, start

comet_experiment = start(
  api_key="Xh1kXXM0IIPgqwAP3wTyChS0R",
  project_name="french-road-accidents",
  workspace="fdevi3"
)




@pipeline(enable_cache=True)
def mega_pipeline():
    logger.info(f"Starting the Dataloader Step")
    dataset = data_loader()
    log_dataset(dataset)


    # logger.info(f"Starting the Data Drifter Step")
    # drift_monitor(dataset)
    #
    # logger.info(f"Starting the Data processor step")
    # data_processed = data_processor(dataset)
    #
    # logger.info(f"Starting the Split Step")
    # X_train, X_test, y_train, y_test = prepare_train_test_split(data_processed)
    #
    # logger.info(f"Starting the Classifier Step")
    # gbc_model = gradboost_classifier(X_train, X_test, y_train, y_test)
    #
    # logger.info(f"Saving the model")
    # save_model(gbc_model, "GradientBoostingClassifier")
    #
    # logger.info(f"Starting the Time series step")
    # ts = create_time_series_date(data_processed)
    #
    # logger.info(f"Training the Time series step")
    # arima_model, forecast_train, forecast_test = train_arima(ts)
    #
    # logger.info(f"Plotting the time series predictions")
    # arima_model, name = predict_plot(arima_model,forecast_test)
    #
    # logger.info(f"Saving the model")
    # save_model(arima_model, name)
    #
    # logger.info(f"Evidently Classifier")
    # evidently_classifier_monitoring(X_train, X_test, y_train, y_test, gbc_model)
    #
    # logger.info("Evidently Forecasting")
    # evidently_forecaster_monitoring(valid =forecast_test,model=arima_model)



def log_dataset(data):
    artifact = Artifact(name="RoadAccidentInputDataset", artifact_type="dataset")
    artifact.add(local_path_or_data=INPUT_PARQUET)
    comet_experiment.log_artifact(artifact)


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