import asyncio
import importlib.util
import json
import logging
import os
import secrets
import sys
from contextlib import asynccontextmanager
from typing import Annotated, Literal
import joblib
import pandas as pd
from comet_ml.api import API
from fastapi import Depends, HTTPException, status
from fastapi import FastAPI, Query
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel, Field
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter, Histogram, Gauge
from prometheus_fastapi_instrumentator import Instrumentator


###Start
logger = logging.getLogger(__name__)

## Some constants
DEFAULT_LAT = 47.149407
DEFAULT_LONG = 2.277096
H3_RESOLUTION = 4
##MACHINE lEARNING
GBC_NAME = "GradientBoostingClassifier"
ARIMA_NAME = "ARIMA"

###PATHS
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
ZENML_FILE_PATH = os.path.join(CURRENT_PATH, 'dummy-retrain.py')

###COMET ML API TODO take this out or atleast disable this
api = API(api_key="Xh1kXXM0IIPgqwAP3wTyChS0R")

##MODEL DIC
model_dic = {}

##Stuff
##Admin Password
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = "admin"

##Metrics for Prometheus
#https://betterstack.com/community/guides/monitoring/prometheus-python-metrics/
MODEL_HEALTH = Gauge(
    'model_health_status',
    'Is the Model Healthy ? (1=healthy, 0=unhealthy)',
    ['model_type']
)


##Pydantic Model
class ForecastRequest(BaseModel):
    periods: int = Field(100, gt=0, le=366)


class ClassifierRequest(BaseModel):
    vehicle_category: Literal['1', '2', '3', '4', '0']
    obstacle_mobile: Literal['1', '2', '3', '0']
    impact_point: Literal['1', '2', '3', '4', '0']
    action: Literal['1', '2', '3', '4', '0']
    safety_equipment: Literal['1', '2', '3', '0']
    road_surface: Literal['1', '2', '3', '0']
    speed_limit: int = Field(50, gt=0, le=200)
    lum: Literal['1', '2', '3', '4', '0']
    weather: Literal['1', '2', '3', '0']
    collision_type: Literal['1', '2', '3', '0']
    accident_hex_count: int = Field(250, gt=0, le=20000)
    latitude: float = Field(DEFAULT_LAT, ge=-90, le=90)
    longitude: float = Field(DEFAULT_LONG, ge=-180, le=180)


# ['vehicle_category' 'obstacle_mobile' 'impact_point' 'action'
#  'safety_equipment' 'road_surface' 'speed_limit' 'lum' 'weather'
#  'collision_type' 'accident_hex_count']

class AdminRequest(BaseModel):
    retrain: bool = Field(False, title="Retraining Trigger")


##TODO implement random choice
def generate_random_classifier_request():
    return ClassifierRequest(vehicle_category='1', obstacle_mobile='2', impact_point='1', action='1',
                             safety_equipment='2', road_surface='1', lum='2', weather='1', collision_type='1',
                             speed_limit=80, accident_hex_count=250, latitude=0.0, longitude=0.0)


####COMET LOAD MODEL and SETUP

def get_gbc_model():
    try:
        api.download_registry_model("fdevi3", "gradientboostingclassifier", output_path=CURRENT_PATH, expand=True,
                                    stage=None)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_412_PRECONDITION_FAILED, detail=str(e))


def get_arima_model():
    try:
        api.download_registry_model("fdevi3", "forecast-arima-model", output_path=CURRENT_PATH, expand=True, stage=None)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_412_PRECONDITION_FAILED, detail=str(e))




## This is basically Start()
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    try:
        gbc_model_path = os.path.join(CURRENT_PATH, f"{GBC_NAME}.pkl")
        arima_model_path = os.path.join(CURRENT_PATH, f"{ARIMA_NAME}.pkl")

        if not os.path.isfile(gbc_model_path):
            get_gbc_model()
        if not os.path.isfile(arima_model_path):
            get_arima_model()

        arima_model = joblib.load(arima_model_path)
        model_dic['arima_model'] = arima_model

        gbc_model = joblib.load(gbc_model_path)
        model_dic['gbc_model'] = gbc_model

        #Since the model loaded set both metrics as 1
        MODEL_HEALTH.labels(model_type='severity').set(1)
        MODEL_HEALTH.labels(model_type='forecast').set(1)

    except Exception as e:
        print(f"Error loading models: {e}")
        MODEL_HEALTH.labels(model_type='severity').set(0) ## Some errror
        MODEL_HEALTH.labels(model_type='forecast').set(0)
    yield
    # Clean up the ML models and release the resources
    model_dic.clear()


###########API #########################
# https://fastapi.tiangolo.com/advanced/security/http-basic-auth/#simple-http-basic-auth
security = HTTPBasic()

app = FastAPI(title="French Road Accidents FAST API Stuff",
              description="Franc's rest api stuff for road accident severity predictions", version="1.0.0",
              lifespan=lifespan, openapi_tags=[{'name': 'test', 'description': 'Just for testing',

                                                }, {'name': 'health', 'description': 'Health Monitoring',

                                                    }, {'name': 'production', 'description': 'Production Ready'},
                                               {'name': 'admin', 'description': 'Admin Only '}])



##Instrumentation
Instrumentator().instrument(app).expose(app)

############ MISC METHODS############
# https://fastapi.tiangolo.com/advanced/security/http-basic-auth/#check-the-username
def authenticate(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    current_username_bytes = credentials.username.encode("utf8")
    current_password_bytes = credentials.password.encode("utf8")

    admin_username_bytes = ADMIN_USERNAME.encode("utf8")
    if secrets.compare_digest(current_username_bytes, admin_username_bytes):
        admin_password_bytes = ADMIN_PASSWORD.encode("utf8")
        if secrets.compare_digest(current_password_bytes, admin_password_bytes):
            return credentials.username

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect Username or Password")


def convert_json_to_dataframe(json_ob=None, expected_feature=None):
    if json_ob is None:
        raise ValueError("Give me a json object")
    ## I will assume that what I get is a BaseModel.model_dump_json
    ## Convert it to a python dic
    json_dic = json.loads(json_ob)
    _df = pd.DataFrame.from_dict([json_dic])  ## Converrted to a dataframe
    ## Since we use Literal for selecttion , we need to convert them back, Can actually use Field for Production
    cat_cols = _df.select_dtypes(include=['object', 'string'])
    for col in cat_cols:
        _df[col] = _df[col].astype(int)

    _df = _df.drop(columns=['latitude', 'longitude'], errors='ignore')
    if expected_feature is None:
        return _df
    return _df[expected_feature]


#########################APP##########################
'''
All of the Fast API Stuff
'''


#############TEST#########

@app.get("/test/classifier_query", tags=['test'])
async def get_query(filter_query: Annotated[ClassifierRequest, Query()]):
    return filter_query


@app.get("/test/forecaster_query", tags=['test'])
async def get_query(filter_query: Annotated[ForecastRequest, Query()]):
    return filter_query


@app.get("/permissions", tags=['test'])
def authorize_user(username: Annotated[str, Depends(authenticate)]):
    _msg = {'username': username}
    logger.info(f"Username: {username} has logged in for testing")
    return _msg


###############PRODUCTION###############
@app.get("/", tags=['production'])
async def read_main():
    msg = {"msg": "Welcome to the French Road Accident Project", "opinion": "DataScientest Bootcamp is a scam"}
    logger.info(f"Saying Hello via msg {msg} ")
    return msg


##Forecasting Endpoint
@app.post("/predict/forecast", tags=['production'])
async def forecast_accidents(request: Annotated[ForecastRequest, Query()]):
    try:
        arima_model = model_dic['arima_model']
        forecast = arima_model.predict(n_periods=request.periods)
        return {"forecast": forecast.tolist()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/predict/severity", tags=['production'])
async def predict_severity(request: Annotated[ClassifierRequest, Query()]):
    try:
        #hex_3 = h3.latlng_to_cell(request.latitude, request.longitude, H3_RESOLUTION)
        # features = [[request.vehicle_category, request.obstacle_mobile, request.impact_point, request.action,
        #              request.safety_equipment, request.road_surface, request.lum, request.weather,
        #              request.collision_type, request.speed_limit, request.accident_hex_count]]

        gbc_model = model_dic['gbc_model']
        _expected_feature_order = list(gbc_model.feature_names_in_)
        if gbc_model is None:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                                detail="Severity Classifier not loaded")

        _json_dump = request.model_dump_json()
        _df = convert_json_to_dataframe(_json_dump, _expected_feature_order)
        prediction = gbc_model.predict(_df)
        probability = gbc_model.predict_proba(_df)[:, 1]
        ##Model is healthy
        MODEL_HEALTH.labels(model_type='severity').set(1)
        return {"prediction": int(prediction[0]), "probability": float(probability[0])}
    except Exception as ex:
        MODEL_HEALTH.labels(model_type='severity').set(0) ## Lets just call any exception as model unhealth
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex))


#############ADMIN#############
#TODO Add background task
#https://fastapi.tiangolo.com/tutorial/background-tasks/#technical-details
@app.post("/admin/retrain", tags=['admin'])
async def retrain_model(username: Annotated[str, Depends(authenticate)], request: Annotated[AdminRequest, Query()]):
    if username != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Only Admin can post, Naughty!!!")
    message = {'message': f"Model Retraining Trigger is {request.retrain}"}
    if bool(request.retrain):
        print("Retraining The Model")
        # await load_file_as_module(name='module.name',location=ZENML_FILE_PATH)
        asyncio.create_task(
            load_file_as_module('module.name', ZENML_FILE_PATH))  ## although blocking is a bit better to avoid overload
    return message


##############HEALTH#########################
@app.get("/health/status", tags=['health'], name="Status Check")
async def health_check():
    _status = {"status": "API is running"}
    logger.info(f" Health Status {_status}")
    return _status


## This is stupid but the sham of a course from Datascientest asks for it ,If they only put the same motivation in designing their course it wont be a scam
@app.get("/health/severity", tags=['health'], name="Severity Classifier Model Check")
async def health_check_severity():
    gbc_model = model_dic['gbc_model']
    _expected_feature_order = list(gbc_model.feature_names_in_)
    if gbc_model is None:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Severity Classifier not loaded")
    try:
        request = generate_random_classifier_request()
        _json_dump = request.json()
        _df = convert_json_to_dataframe(_json_dump, _expected_feature_order)
        gbc_model = model_dic['gbc_model']
        prediction = gbc_model.predict(_df)
        probability = gbc_model.predict_proba(_df)[:, 1]
        _message = {"prediction": int(prediction[0]), "probability": float(probability[0]),
                    "health": "Model is Healthy" if float(probability[0]) > 0.15 else "Model Unhealthy"}

        ## Same logic
        if float(probability[0]) >0.15:
            MODEL_HEALTH.labels(model_type='severity').set(1)
        else:
            MODEL_HEALTH.labels(model_type='severity').set(0)
        return _message
    except Exception as ex:
        MODEL_HEALTH.labels(model_type='severity').set(0)
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(ex))


@app.get("/health/forecast", tags=['health'], name="Forecast Model Check")
async def health_check_forecast():
    arima_model = model_dic['arima_model']
    if arima_model is None:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Forecast Model not loaded")
    try:
        forecast = arima_model.predict(n_periods=69)  ##Some random value
        return {"forecast": forecast.tolist(),
                'health': "Model is Healthy" if len(forecast.tolist()) == 69 else "Model Unhealthy"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


##############RANDOM METHODS###############
##https://stackoverflow.com/questions/3781851/run-a-python-script-from-another-python-script-passing-in-arguments
# https://stackoverflow.com/questions/436198/what-alternative-is-there-to-execfile-in-python-3-how-to-include-a-python-fil/16577427#16577427
# https://stackoverflow.com/questions/67631/how-can-i-import-a-module-dynamically-given-the-full-path
async def load_file_as_module(name='module.name', location=ZENML_FILE_PATH):
    spec = importlib.util.spec_from_file_location(name, location)
    foo = importlib.util.module_from_spec(spec)
    sys.modules[name] = foo
    spec.loader.exec_module(foo)
    foo.hello()


#############REGION##################
##Random stuff
def do_stuff():
    print("Hii")



# TODO Remove this region
if __name__ == "__main__":
    do_stuff()
