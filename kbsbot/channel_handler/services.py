from requests import Session
import requests
import os

# COMPOSE_ENGINE = os.environ.get('COMPOSE_ENGINE')
COMPOSE_ENGINE = "http://127.0.0.1:5000"

session = Session()
session.trust_env = False
session.verify = False
session.headers["Accept"] = "application/json"
session.headers["Content-Type"] = "application/json"


def replicate_entry(user, data, method):
    pass


def compose(data):
    url = COMPOSE_ENGINE + "/compose"
    try:
        r = session.get(url, json=data)
        if r.status_code == 200:
            response = r.json()
            print(response)
            return response
    except requests.exceptions.RequestException as e:
        print(e)
