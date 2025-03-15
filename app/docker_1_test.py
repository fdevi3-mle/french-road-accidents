import base64
import logging
import os
import time

import requests

###URLS
##TODO CHANGE TO base_url="http://fast_api:8000" for production
base_url = "http://fast_api:8000"
hello_url = base_url + "/"
health_url = base_url + "/health/status"
query_forecast_url = base_url + "/test/forecaster_query"
permission_url = base_url + "/permissions"
health_forecast_url = base_url + "/health/forecast"
health_severity_url = base_url + "/health/severity"

## Logger
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
LOG_PATH = os.path.join(CURRENT_PATH, 'logs')

logger = logging.getLogger(__name__)


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


def read_main():
    response = requests.get(hello_url)
    logger.info(f" Docker 1 says : {response.json()} ")


def read_health_status():
    response = requests.get(health_url)
    logger.info(f" Docker 1 pokes health @ {health_url} and receives {response.json()}")
    print(f" Docker 1 pokes health @ {health_url} and receives {response.json()}")


def read_forecast_query():
    params = {'periods': 13}
    response = requests.get(query_forecast_url, params=params)
    logger.info(
        f"Docker 1 pokes @ {query_forecast_url} and receives {response.json()} with status code {response.status_code}")
    print(
        f"Docker 1 pokes @ {query_forecast_url} and receives {response.json()} with status code {response.status_code}")


def read_forecast_health():
    response = requests.get(health_forecast_url)
    logger.info(f"Docker 1 pokes @ {health_forecast_url}  with status code {response.status_code}")
    print(f"Docker 1 pokes @ {query_forecast_url} with status code {response.status_code}")
    print(response.json())


def read_severity_health():
    response = requests.get(health_severity_url)
    logger.info(f"Docker 1 pokes @ {health_severity_url}  with status code {response.status_code}")
    print(f"Docker 1 pokes @ {health_severity_url} with status code {response.status_code}")
    print(response.json())


if __name__ == "__main__":
    generate_logger(filename='docker_1')
    time.sleep(60)  ## sleep till it all starts up
    for i in range(50):
        read_main()
        time.sleep(2)
        read_health_status()
        time.sleep(2)
        read_forecast_query()
        time.sleep(2)
        read_severity_health()
        time.sleep(10)
