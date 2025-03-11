import importlib.util
import os
import runpy
import sys

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
ZENML_FILE_PATH = os.path.join(CURRENT_PATH,'dummy-retrain.py')


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


if __name__ == "__main__":
    load_file_as_module(ZENML_FILE_PATH)

