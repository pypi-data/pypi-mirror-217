from __future__ import annotations

import os
import pytest
from requests.sessions import Session
import xarray as xr

from pyteseo.providers.cmems import (
    get_cmems_opendap_datastore,
    get_cmems_session,
    CMEMS_SESSION,
)


username = os.environ.get("CMEMS_username")
password = os.environ.get("CMEMS_password")

pytestmark = pytest.mark.skipif(
    username is None or password is None, reason="CMEMS login credentials not defined!"
)

dataset_name = "cmems_ibi_hourly"


def test_login():
    assert isinstance(CMEMS_SESSION, Session)
    assert "CASTGC" in CMEMS_SESSION.cookies.get_dict()


def test_get_cmems_datastore():
    datastore = get_cmems_opendap_datastore(dataset_name)
    assert isinstance(datastore, xr.backends.PydapDataStore)


def test_retry_sesion():
    cmems_session = None
    cmems_session = get_cmems_opendap_datastore(dataset_name)
    assert cmems_session


def test_login_error():
    with pytest.raises(ValueError):
        get_cmems_session("bad_username", "bad_password")
