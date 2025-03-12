import importlib.util
import json
import os
import runpy
import sys

import joblib
import pandas as pd

from app.main import ForecastRequest, ClassifierRequest, generate_random_classifier_request

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
ZENML_FILE_PATH = os.path.join(CURRENT_PATH,'dummy-retrain.py')
GBC_MODEL_PATH = os.path.join(CURRENT_PATH,"GradientBoostingClassifier.pkl")


#############REGION##################
##Random stuff
def do_stuff(filepath= ZENML_FILE_PATH):
    if not os.path.isfile(filepath):
        raise FileNotFoundError("Cant find the dummy retraining script")
    print(ZENML_FILE_PATH)
    runpy.run_path(ZENML_FILE_PATH)
    # api = API(api_key="Xh1kXXM0IIPgqwAP3wTyChS0R")
    # api.download_registry_model("fdevi3", "forecast-arima-model", output_path="./", expand=True)

##https://stackoverflow.com/questions/3781851/run-a-python-script-from-another-python-script-passing-in-arguments
#https://stackoverflow.com/questions/436198/what-alternative-is-there-to-execfile-in-python-3-how-to-include-a-python-fil/16577427#16577427
#https://stackoverflow.com/questions/67631/how-can-i-import-a-module-dynamically-given-the-full-path
def load_file_as_module(name='module.name',location=ZENML_FILE_PATH):
    spec = importlib.util.spec_from_file_location(name, location)
    foo = importlib.util.module_from_spec(spec)
    sys.modules[name] = foo
    spec.loader.exec_module(foo)
    foo.hello()

#https://stackoverflow.com/questions/56443966/convert-dictionary-to-python-dataframe?noredirect=1&lq=1
def dummy_request():
    a = generate_random_classifier_request()
    a = a.model_dump_json()
    a_dict = json.loads(a)
    df = pd.DataFrame.from_dict([a_dict])
    cat_cols = df.select_dtypes(include=['object','string'])
    for col in cat_cols:
        df[col]  = df[col].astype(int)

    print(df.info())
    print(df)

def load_model(path=GBC_MODEL_PATH):
    if not os.path.isfile(path):
        raise FileNotFoundError("Noooo fole")

    gbc_model = joblib.load(path)
    expected_features = list(gbc_model.feature_names_in_)
    print("Model expects features:", expected_features)


if __name__ == "__main__":
    load_model()

