##Constants & FILEPATHS
import logging
import os

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__)) ## src
ROOT_PATH = os.path.dirname(CURRENT_PATH)
LOG_PATH = os.path.join(ROOT_PATH, 'logs')






## Lets test the normal logger instead of the zenml one
def generate_logger(logpath=LOG_PATH):
    os.makedirs(logpath,exist_ok=True)
    logger = logging.getLogger(__name__)
    print(logpath)
    filename= 'test-logger.txt'
    filepath = os.path.join(logpath, filename)
    logging.basicConfig(filename=filepath, encoding='utf-8', level=logging.DEBUG)
    print(filepath)
    logger.info("Hi")
