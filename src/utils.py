import os.path
from datetime import datetime
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

############ LOAD DOTENV ############
# Load environment variables from the .env file
load_dotenv()

# Evidently
EVIDENTLY_TOKEN = os.getenv("EVIDENTLY_TOKEN")
EVIDENTLY_PROJECT_CLASSIFIER_ID = os.getenv("EVIDENTLY_PROJECT_CLASSIFIER_ID")
EVIDENTLY_PROJECT_FORECAST_ID = os.getenv("EVIDENTLY_PROJECT_FORECAST_ID")

######## COMET ML
# Common
COMET_WORKSPACE = "fdevi3"
COMET_MY_API_KEY = os.getenv("COMET_MY_API_KEY")

# CLASSIFIER
COMET_CLASSIFIER_PROJECT_NAME = "french-road-accident-classifier"

# Comet Data
COMET_DATASET_PROJECT_NAME = "french-road-accidents"

# Comet Forecaster
COMET_FORECAST_PROJECT_NAME = "french-forecaster"

##########NEPTUNE AI
# CLASSIFIER
NEPTUNE_CLASSIFIER_PROJECT = "France-Road-Accidents-Test/SeverityClassifier"
NEPTUNE_CLASSIFIER_API_TOKEN = os.getenv("NEPTUNE_CLASSIFIER_API_TOKEN")

##fORECASTER
NEPTUNE_FORECAST_PROJECT = "fdevi3-time/RoadAcccidentForecast"
NEPTUNE_FORECAST_API_TOKEN = os.getenv("NEPTUNE_FORECAST_API_TOKEN")

##Constants & FILEPATHS
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))  ## src
ROOT_PATH = os.path.dirname(CURRENT_PATH)
DATA_PATH = os.path.join(ROOT_PATH, 'data')
MODEL_PATH = os.path.join(ROOT_PATH, 'models')
NOTEBOOK_PATH = os.path.join(ROOT_PATH, 'notebooks')
SRC_PATH = os.path.join(ROOT_PATH, 'src')

##DATA FILE
INPUT_PATH = os.path.join(DATA_PATH, 'input')
INPUT_PARQUET = os.path.join(INPUT_PATH, 'merged.parquet')
PARQUET_2019 = os.path.join(INPUT_PATH, '2019.parquet')
PARQUET_2020 = os.path.join(INPUT_PATH, '2020.parquet')
PARQUET_2021 = os.path.join(INPUT_PATH, '2021.parquet')
PARQUET_2022 = os.path.join(INPUT_PATH, '2022.parquet')
PARQUET_2023 = os.path.join(INPUT_PATH, '2023.parquet')

##MACHINE lEARNING
GBC_NAME = "GradientBoostingClassifier"
ARIMA_NAME = "ARIMA"

##BAD IDEA
MAPBOX_TOKEN = "pk.eyJ1IjoiZnJhbi10ZXN0LTMiLCJhIjoiY202eHRzOGo2MTFqZzJzczZhb3VtNHpteCJ9.vW4EOk0IJTaR-pZ0fATSuQ"

OUTPUT_PATH = os.path.join(DATA_PATH, 'output')
# REPORT path
REPORT_PATH = os.path.join(ROOT_PATH, 'report')
FIGURE_PATH = os.path.join(REPORT_PATH, 'figures')
LOG_PATH = os.path.join(ROOT_PATH, 'logs')

##Figures
FIGURE_1 = os.path.join(FIGURE_PATH, 'fig1.png')
FIGURE_2 = os.path.join(FIGURE_PATH, 'fig2.png')
FIGURE_3 = os.path.join(FIGURE_PATH, 'fig3.png')
FIGURE_4 = os.path.join(FIGURE_PATH, 'fig4.png')
FIGURE_5 = os.path.join(FIGURE_PATH, 'fig5.png')
FIGURE_6 = os.path.join(FIGURE_PATH, 'fig6.png')
FIGURE_7 = os.path.join(FIGURE_PATH, 'fig7.png')
FIGURE_8 = os.path.join(FIGURE_PATH, 'fig8.png')
FIGURE_9 = os.path.join(FIGURE_PATH, 'fig9.png')
FIGURE_10 = os.path.join(FIGURE_PATH, 'fig10.png')
FIGURE_11 = os.path.join(FIGURE_PATH, 'fig11.png')
FIGURE_12 = os.path.join(FIGURE_PATH, 'fig12.png')
FIGURE_13 = os.path.join(FIGURE_PATH, 'fig13.png')
FIGURE_14 = os.path.join(FIGURE_PATH, 'fig14.png')
FIGURE_15 = os.path.join(FIGURE_PATH, 'fig15.png')
FIGURE_16 = os.path.join(FIGURE_PATH, 'fig16.png')
FIGURE_17 = os.path.join(FIGURE_PATH, 'fig17.png')
FIGURE_18 = os.path.join(FIGURE_PATH, 'fig18.png')
FIGURE_19 = os.path.join(FIGURE_PATH, 'fig19.png')
FIGURE_20 = os.path.join(FIGURE_PATH, 'fig20.png')
FIGURE_21 = os.path.join(FIGURE_PATH, 'fig21.png')
FIGURE_22 = os.path.join(FIGURE_PATH, 'fig22.png')
FIGURE_23 = os.path.join(FIGURE_PATH, 'fig23.png')
FIGURE_24 = os.path.join(FIGURE_PATH, 'fig24.png')
FIGURE_25 = os.path.join(FIGURE_PATH, 'fig25.png')
FIGURE_26 = os.path.join(FIGURE_PATH, 'fig26.png')
FIGURE_27 = os.path.join(FIGURE_PATH, 'fig27.png')
FIGURE_28 = os.path.join(FIGURE_PATH, 'fig28.png')





CSV_EXTENSION = '.csv'
PARQUET_EXTENSION = '.parquet'
HTML = '.html'
PNG = '.png'
JPG = '.jpg'

##LAT & LONG : BORDERS
LAT_MIN = 40.0
LAT_MAX = 60.0
LONG_MIN = -10.0
LONG_MAX = 10.0

# Paris coordinates (latitude, longitude)
MID_LAT = 47.149407
MID_LONG = 2.277096
H3_RESOLUTION = 4

##DATE
TRAIN_DATE_LIMIT = pd.Timestamp('2023-06-30')

VERSION = '0.0.0'
import logging


class ExtensionMethods:
    @staticmethod
    def generate_filename(filename=None, extension=None):
        current_datetime = datetime.now()
        f = current_datetime.strftime("%Y_%m_%d_%H%M")
        if (filename is None) or (extension is None):
            return str(f)
        else:
            stitched_f = str(filename) + "_" + str(f) + "." + str(extension)
            return str(stitched_f)

    @staticmethod
    def get_file_name_without_extension(filename):
        if filename is None:
            return "Provide a file"
        return Path(filename).stem

    @staticmethod
    def generate_filename_only(filename=None, extension=None):
        if (filename is None) or (extension is None):
            return str("Dummy.txt")
        else:
            stitched_f = str(filename) + "." + str(extension)
            return str(stitched_f)

    @staticmethod
    def get_all_files(dirpath=DATA_PATH, extension='.parquet'):
        _all_files = {}
        file_list = os.listdir(dirpath)
        for file in file_list:
            filepath = os.path.join(dirpath, file)
            if file.endswith(extension):
                _all_files[file] = filepath

        return _all_files

    @staticmethod
    def create_parquet(data=None, filename='', filepath=OUTPUT_PATH):
        if data is None:
            raise ValueError("Data can't be None for Parquet Creation")
        obj_cols = data.select_dtypes(include=['object', 'categorical']).columns
        for col in obj_cols:
            data[col] = data[col].astype(str)
        if not os.path.exists(filepath):
            os.makedirs(filepath)  ## a bit of cheating
        _full_path = os.path.join(filepath, filename)
        data.to_parquet(filepath, engine='pyarrow', compression="zstd", compression_level=10, index=False)
        print(f"\n Finished Saving parquet to: {filepath}")


## Lets test the normal logger instead of the zenml one
def generate_logger(logpath=LOG_PATH):
    logger = logging.getLogger(__name__)
    filename = ExtensionMethods.generate_filename('logger', 'log')
    filepath = os.path.join(logpath, filename)
    logging.basicConfig(filename=filepath, encoding='utf-8', level=logging.DEBUG)
    logger.info("Hi")


if __name__ == "__main__":
    print(f"ROOT_PATH: {ROOT_PATH}")
    print(f"CURRENT_PATH: {CURRENT_PATH}")
    print(f"DATA_PATH: {DATA_PATH}")
    print(f"VERSION: {VERSION}")
    print(f"SRC_PATH: {SRC_PATH}")
    print(f"OUTPUT_PATH: {OUTPUT_PATH}")
    print(f"FileName generated {ExtensionMethods.generate_filename("test", 'jpg')}")
    print(f"FileName generated {ExtensionMethods.get_all_files(INPUT_PATH)}")
    generate_logger(LOG_PATH)
