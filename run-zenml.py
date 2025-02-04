from zenml.client import Client
import logging
from zenml import Model, pipeline

#stps
from src.monolith import data_loader,data_analyser, time_series, predict_plot, \
    save_model, data_processor

##Activate logger and client
logger = logging.getLogger(__name__)
logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)

#Zenml Client
client = Client()
Client().activate_stack(
        "default"
    )



@pipeline(enable_cache=True)  # This function combines steps together
def ml_pipeline():
    logger.info(f"Starting the Dataloader Step")
    dataset = data_loader()

    logger.info(f"Starting the Data processor step")
    data_processed = data_processor(dataset)

    logger.info(f"Starting the Data Analyser step")
    data_analyser(data_processed)

    logger.info(f"Starting the Model Training step")
    model = time_series(data_processed)
    predict_plot(model)

    logger.info(f"Saving the model")
    save_model(model)
    logger.info(f"All steps finished")

if __name__ == "__main__":
    run = ml_pipeline()
    logger.info(f"ML pipeline has been started")