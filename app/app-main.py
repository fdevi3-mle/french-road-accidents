import logging
import os
import joblib
from fastapi import FastAPI
from fastapi.security import HTTPBasic
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
from fastapi import FastAPI, Query
from pydantic import BaseModel, Field
import json
import secrets
from typing import Annotated, Literal,List, Optional

from src.utils import MODEL_PATH, ARIMA_NAME, GBC_NAME

###Start
logger = logging.getLogger(__name__)

##LOCAL ONLY
ARIMA_MODEL_PATH = os.path.join(MODEL_PATH, f"{ARIMA_NAME}.pkl")
GBC_MODEL_PATH = os.path.join(MODEL_PATH, f"{GBC_NAME}.pkl")


try:
    arima_model = joblib.load(ARIMA_MODEL_PATH)
    gbc_model = joblib.load(GBC_MODEL_PATH)
except Exception as e:
    print(f"Error loading models: {e}")


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



####API and SETUP
#https://fastapi.tiangolo.com/advanced/security/http-basic-auth/#simple-http-basic-auth
security = HTTPBasic()

app = FastAPI(
    title="French Road Accidents FAST API Stuff",
    description= "Franc's rest api stuff for road accident severity predictions",
    version="1.0.0",
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


@app.post("/predict/arima",tags=['production'])
async def predict_arima(request:Annotated[ForecastRequest, Query()]):
    try:
        forecast = arima_model.predict(n_periods=request.periods)
        return {"forecast": forecast.tolist()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



##Random stuff
def do_stuff():
    print("Hii")


if __name__ == "__main__":
    do_stuff()

