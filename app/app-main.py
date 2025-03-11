import logging
import os
import joblib
from fastapi import FastAPI
from fastapi.security import HTTPBasic
from pydantic import BaseModel

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
class TimeSeriesRequest(BaseModel):
    periods: int




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

@app.get("/")
async def read_main():
    msg = {"msg": "Welcome to the French Road Accident Project"}
    logger.info(f"Saying Hello via msg {msg} ")
    return msg


@app.get("/health",tags=['test'],name="Status Check")
async def health_check():
    _status = {"status": "API is running"}
    logger.info(f" Health Status {_status}")
    return _status



