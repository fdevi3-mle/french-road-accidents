import os


from zenml.client import Client
import logging
from zenml import Model, pipeline

#stps
from src.monolith import data_loader, data_processor, create_time_series_date, time_series_analyser, train_arima, \
    predict_plot, save_model

##Activate logger and client
logger = logging.getLogger(__name__)
logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)

os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

#Zenml Client
client = Client()
Client().activate_stack(
        "default"
    )








@pipeline(enable_cache=False)  # This function combines steps together
def ml_pipeline():
    logger.info(f"Starting the Dataloader Step")
    dataset = data_loader()


    logger.info(f"Starting the Data processor step")
    data_processed = data_processor(dataset)

    logger.info(f"Starting the Data Analyser step")
    ts= create_time_series_date(data_processed)

    a,b,c=train_arima(ts)
    model, name= predict_plot(a,b,c)
    #print(a.summary())

    # logger.info(f"Starting the Model Training step")
    # model = time_series(data_processed)
    # predict_plot(model)
    #
    # logger.info(f"Saving the model")
    save_model(model,name)
    # logger.info(f"All steps finished")

if __name__ == "__main__":
    run = ml_pipeline()
    logger.info(f"ML pipeline has been started")