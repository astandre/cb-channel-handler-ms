from requests import Session
import requests
import os

COMPOSE_ENGINE = os.environ.get('COMPOSE_ENGINE')
# COMPOSE_ENGINE = "http://127.0.0.1:5000"

session = Session()
session.trust_env = False
session.verify = False
session.headers["Accept"] = "application/json"
session.headers["Content-Type"] = "application/json"


def compose(data):
    """
    This method connects to the compose engine in order to get the answer for the user.

    Args:
            :param data: A dict containing data to pass to the engine. This dict contains, the user id, the agent, the context and the user input.

    Returns:
        A dict containing the context and the answer for the user.
    """
    url = COMPOSE_ENGINE + "/compose"
    try:
        r = session.get(url, json=data)
        if r.status_code == 200:
            response = r.json()
            print(response)
            return response
    except requests.exceptions.RequestException as e:
        print(e)
