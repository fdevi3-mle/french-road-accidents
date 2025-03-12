import base64
import logging
import os
import time

import requests

###URLS
##TODO CHANGE TO base_url="http://fast_api:8000" for production
base_url = "http://127.0.0.1:8000"
hello_url = base_url + "/"
health_url = base_url + "/health/status"
query_forecast_url = base_url + "/test/forecaster_query"
permission_url = base_url + "/permissions"
health_forecast_url = base_url + "/health/forecast"
health_severity_url = base_url + "/health/severity"
admin_retrain_url = base_url + "/admin/retrain"

## Logger
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
LOG_PATH = os.path.join(CURRENT_PATH, 'logs')

logger = logging.getLogger(__name__)


### SIMULATES A NORMAL USER

##MISC Methods
##https://stackoverflow.com/questions/6999565/python-https-get-with-basic-authentication
def basic_auth(username, password):
    token = base64.b64encode(f"{username}:{password}".encode('utf-8')).decode("ascii")
    return f'Basic {token}'


def generate_logger(_logpath=LOG_PATH, filename="default"):
    os.makedirs(LOG_PATH, exist_ok=True)
    filename = f'{filename}.log'
    filepath = os.path.join(_logpath, filename)
    logging.basicConfig(filename=filepath, encoding='utf-8', level=logging.DEBUG)
    logger.info(f"Hi, Logger Fired Up  for {filename}!!")


##Simulate ADMIN USER

def read_main():
    response = requests.get(hello_url)
    logger.info(f" Docker 2 says : {response.json()} ")


def read_health_status():
    response = requests.get(health_url)
    logger.info(f" Docker 2 pokes health @ {health_url} and receives {response.json()}")
    print(f" Docker 2 pokes health @ {health_url} and receives {response.json()}")


def read_permission():
    auth = basic_auth('admin', 'admin')
    response = requests.get(permission_url, headers={"Authorization": auth})
    logger.info(
        f"Docker 2 pokes @ {permission_url} and receives {response.json()} with status code {response.status_code}")
    print(f"Docker 2 pokes @ {permission_url} and receives {response.json()} with status code {response.status_code}")


def do_retraining(retrain=False):
    auth = basic_auth('admin', 'admin')
    params = {"retrain": retrain}
    response = requests.post(admin_retrain_url, params=params, headers={"Authorization": auth})
    logger.info(
        f"Docker 2 pokes @ {admin_retrain_url} and receives {response.json()} with status code {response.status_code}")
    print(
        f"Docker 2 pokes @ {admin_retrain_url} and receives {response.json()} with status code {response.status_code}")


### MAIN

if __name__ == "__main__":
    generate_logger(filename='docker_2')
    time.sleep(30)  ## sleep till it all starts up
    for i in range(3):
        read_main()
        time.sleep(1)
        read_health_status()
        time.sleep(1)
        read_permission()
        time.sleep(1)
    do_retraining(True)  ## Do iit once only

#
# ###OLD CODE
# def read_forecast_query():
#     def get_v1_sentiment_bob():
#         auth = basic_auth('bob', 'builder')
#         response = requests.get(v1_sentiment_url, params={'query': "I love chocolate and oranges"},
#                                 headers={"Authorization": auth})
#         logger.info(
#             f"Docker 2 pokes @ {v1_sentiment_url} and receives {response.json()} with status code {response.status_code}")
#         print(f"User got a response status code of {response.status_code} and response {response.json()}")
