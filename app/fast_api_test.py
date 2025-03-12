import base64

from fastapi.testclient import TestClient
from starlette import status

from app.main import app, ForecastRequest

##urls
base_url="http://127.0.0.1:8000"
hello_url = base_url+"/"
health_url = base_url + "/health/status"
query_forecast_url = base_url + "/test/forecaster_query"
permission_url = base_url + "/permissions"
health_forecast_url = base_url+ "/health/forecast"
health_severity_url = base_url+ "/health/severity"



##https://stackoverflow.com/questions/6999565/python-https-get-with-basic-authentication
def basic_auth(username, password):
    token = base64.b64encode(f"{username}:{password}".encode('utf-8')).decode("ascii")
    return f'Basic {token}'

#https://fastapi.tiangolo.com/tutorial/testing/?h=test#using-testclient
## I just love FastApi docs , no need for a course
client = TestClient(app)

def test_read_main():
    response = client.get(hello_url)
    assert response.status_code == status.HTTP_200_OK
    msg = {"msg": "Welcome to the French Road Accident Project", "opinion": "DataScientest Bootcamp is a scam"}
    assert response.json() == msg

def test_status_endpoint():
    response = client.get(health_url)
    assert response.status_code==status.HTTP_200_OK
    assert response.json() == {"status":"API is running"}

def test_permission_endpoint():
    response = client.get(permission_url, headers={"Authorization": basic_auth('admin','admin')})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'username':'admin'}

def test_permission_bad_username():
    response = client.get(permission_url, headers={"Authorization": basic_auth('hacker','hacker')})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() != {'username':'admin'}

##One can never be too childish for :P
def test_forecast_query():
    response = client.get(query_forecast_url, params={'periods': 69})
    assert response.status_code == status.HTTP_200_OK
    print(response.json())
    assert response.json() == {"periods":69}




