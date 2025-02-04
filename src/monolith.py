from src.franums import RoadAccidentEnum
from zenml import get_pipeline_context, pipeline, log_metadata, step
from zenml.logger import get_logger
from typing import Optional, Tuple
from typing_extensions import Annotated

##setup the logger
logger = get_logger(__name__)

@step
def data_loader():
    pass

@step
def data_processor():
    pass


@step
def data_analyser():
    pass

@step
def time_series():
    pass

@step
def predict_plot():
    pass

@step
def save_model():
    pass



def main():
    print('Main Function')



if __name__ == '__main__':
    main()