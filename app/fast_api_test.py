import base64

from fastapi.testclient import TestClient
from starlette import status

from app.main import app

##urls
base_url="http://127.0.0.1:8000"
hello_url = base_url+"/"
health_url = base_url + "/health"

##https://stackoverflow.com/questions/6999565/python-https-get-with-basic-authentication
def basic_auth(username, password):
    token = base64.b64encode(f"{username}:{password}".encode('utf-8')).decode("ascii")
    return f'Basic {token}'

#https://fastapi.tiangolo.com/tutorial/testing/?h=test#using-testclient
## I just love FastApi docs , no need for a course
client = TestClient(app)

def test_read_main():
    response = client.get(hello_url)
    assert response.status_code == 200
    msg = {"msg": "Welcome to the French Road Accident Project", "opinion": "DataScientest Bootcamp is a scam"}
    assert response.json() == msg

