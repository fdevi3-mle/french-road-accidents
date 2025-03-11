import logging
import os
from typing import Annotated, Literal
from contextlib import asynccontextmanager
import h3
import joblib
from fastapi import FastAPI, Query
from fastapi import HTTPException, status
from fastapi.security import HTTPBasic
from pydantic import BaseModel, Field
from comet_ml.api import API
###Start
logger = logging.getLogger(__name__)

## Some constants
DEFAULT_LAT = 47.149407
DEFAULT_LONG = 2.277096
H3_RESOLUTION = 4
##MACHINE lEARNING
GBC_NAME = "GradientBoostingClassifier"
ARIMA_NAME = "ARIMA"



##COMET ML
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))

api = API(api_key="Xh1kXXM0IIPgqwAP3wTyChS0R")



# try:
#     api.download_registry_model("fdevi3", "gradientboostingclassifier", output_path=CURRENT_PATH, expand=True, stage=None)
#     api.download_registry_model("fdevi3", "forecast-arima-model", version='latest', output_path=CURRENT_PATH, expand=True,
#                                 stage=None)
#
#     arima_model = joblib.load(ARIMA_MODEL_PATH)
#     gbc_model = joblib.load(GBC_MODEL_PATH)
# except Exception as e:
#     print(f"Error loading models: {e}")
#
#
model_dic = {}



##Pydantic Model
class ForecastRequest(BaseModel):
    periods: int = Field(100, gt=0, le=366)

class ClassifierRequest(BaseModel):
    vehicle_category: Literal['1','2','3','4','0']
    obstacle_mobile: Literal['1','2','3','0']
    impact_point: Literal['1','2','3','4','0']
    action: Literal['1','2','3','4','0']
    safety_equipment: Literal['1','2','3','0']
    road_surface: Literal['1','2','3','0']
    lum: Literal['1','2','3','4','0']
    weather: Literal['1','2','3','0']
    collision_type: Literal['1','2','3','0']
    speed_limit:int = Field(50, gt=0, le=200)
    accident_hex_count:int = Field(250, gt=0, le=20000)
    latitude: float = Field(DEFAULT_LAT, ge=-90, le=90)
    longitude: float = Field(DEFAULT_LONG, ge=-180, le=180)



####API and SETUP

def get_gbc_model():
    try:
        api.download_registry_model("fdevi3", "gradientboostingclassifier", output_path=CURRENT_PATH, expand=True,
                                    stage=None)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_412_PRECONDITION_FAILED,detail=str(e))

def get_arima_model():
    try:
        api.download_registry_model("fdevi3", "forecast-arima-model", output_path=CURRENT_PATH,
                                    expand=True,
                                    stage=None)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_412_PRECONDITION_FAILED,detail=str(e))


##Startup new
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
    except Exception as e:
        print(f"Error loading models: {e}")
    yield
    # Clean up the ML models and release the resources
    model_dic.clear()


#https://fastapi.tiangolo.com/advanced/security/http-basic-auth/#simple-http-basic-auth
security = HTTPBasic()

app = FastAPI(
    title="French Road Accidents FAST API Stuff",
    description= "Franc's rest api stuff for road accident severity predictions",
    version="1.0.0",
    lifespan=lifespan,
    openapi_tags=[
        {
            'name':'test',
            'description': 'Stuff for Testing',

        },
        {
            'name': 'production',
            'description': 'Production Ready'
        }
    ]
)


##Startup
# @app.on_event("startup")
# async def startup_event():
#     try:
#         api.download_registry_model("fdevi3", "gradientboostingclassifier", output_path=CURRENT_PATH, expand=True,
#                                     stage=None)
#         api.download_registry_model("fdevi3", "forecast-arima-model", output_path=CURRENT_PATH,
#                                     expand=True,
#                                     stage=None)
#
#         gbc_model_path = os.path.join(CURRENT_PATH, f"{GBC_NAME}.pkl")
#         arima_model_path = os.path.join(CURRENT_PATH, f"{ARIMA_NAME}.pkl")
#
#         arima_model = joblib.load(arima_model_path)
#         model_dic['arima_model'] = arima_model
#
#         gbc_model = joblib.load(gbc_model_path)
#         model_dic['gbc_model'] = gbc_model
#     except Exception as e:
#         print(f"Error loading models: {e}")


@app.get("/",tags=['production'])
async def read_main():
    msg = {"msg": "Welcome to the French Road Accident Project"}
    logger.info(f"Saying Hello via msg {msg} ")
    return msg


@app.get("/health",tags=['test'],name="Status Check")
async def health_check():
    _status = {"status": "API is running"}
    logger.info(f" Health Status {_status}")
    return _status



@app.get("/test/classifier_query",tags=['test'])
async def get_query(filter_query: Annotated[ClassifierRequest, Query()]):
    return filter_query

@app.get("/test/forecaster_query",tags=['test'])
async def get_query(filter_query: Annotated[ForecastRequest, Query()]):
    return filter_query

######REGION################

##Forecasting Endpoint
@app.post("/predict/forecast",tags=['production'])
async def forecast_accidents(request:Annotated[ForecastRequest, Query()]):
    try:
        arima_model = model_dic['arima_model']
        forecast = arima_model.predict(n_periods=request.periods)
        return {"forecast": forecast.tolist()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict/severity",tags=['production'])
async def predict_severity(request:Annotated[ClassifierRequest, Query()]):
    try:
        hex_3 = h3.latlng_to_cell(request.latitude, request.longitude, H3_RESOLUTION)
        features = [[
            request.vehicle_category, request.obstacle_mobile, request.impact_point,
            request.action, request.safety_equipment, request.road_surface,
            request.lum, request.weather, request.collision_type, request.speed_limit,request.accident_hex_count
        ]]

        gbc_model = model_dic['gbc_model']
        prediction = gbc_model.predict(features)
        probability = gbc_model.predict_proba(features)[:, 1]

        return {"prediction": int(prediction[0]), "probability": float(probability[0])}

    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=str(ex))



#############REGION##################
##Random stuff
def do_stuff():
    print("Hii")


if __name__ == "__main__":
    do_stuff()

