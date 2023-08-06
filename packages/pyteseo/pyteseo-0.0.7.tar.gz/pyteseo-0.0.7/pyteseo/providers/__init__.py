"""Subpackage to provide data from metocean data providers"""

import json
import os
from pathlib import Path
from pydap.cas.get_cookies import setup_session
from requests.sessions import Session


def load_providers_datasets_registry(json_path):
    providers_datasets_json = Path(json_path)
    if providers_datasets_json.exists():
        with open(providers_datasets_json, "r") as file:
            return json.load(file)
    else:
        print(
            f"json file with the configuration of the external datasets not found @ {json_path}. set this path at the env-variable PROVIDERS_DATASETS_PATH"
        )
        return None


providers_registry_path = Path(__file__).parent / "providers_registry.json"
providers_registry_path = (
    os.environ.get("PROVIDERS_REGISTRY_PATH")
    if os.environ.get("PROVIDERS_REGISTRY_PATH")
    else providers_registry_path
)


DATASETS = load_providers_datasets_registry(providers_registry_path)


def get_cmems_session(username: str, password: str) -> Session:
    """login in cmems web and services

    Args:
        username (str): CMEMS username
        password (str): CMEMS password

    Returns:
        Session: active session for CMEMS web and services
    """

    session = setup_session("https://cmems-cas.cls.fr/cas/login", username, password)
    try:
        session.cookies.set("CASTGC", session.cookies.get_dict()["CASTGC"])
    except KeyError:
        raise ValueError("Authentication error, check your username and password")
    print(f"\033[1;32m \n{username} login successful! \U0001F642 \033[0;0m\n")
    return session


CMEMS_SESSION = get_cmems_session(
    os.environ.get("CMEMS_username"), os.environ.get("CMEMS_password")
)
