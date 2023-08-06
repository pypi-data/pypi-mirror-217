from __future__ import annotations

from requests.sessions import Session
from webob import exc

import os
import xarray as xr

from pydap.client import open_url
from pyteseo.providers import DATASETS, CMEMS_SESSION, get_cmems_session


def get_cmems_opendap_datastore(dataset_name, cmems_session: Session = CMEMS_SESSION):
    cmems_dataset_url = _collect_cmems_url(dataset_name)
    return _get_cmems_datastore(cmems_dataset_url, cmems_session)


def _collect_cmems_url(dataset):
    cmems_url = DATASETS["opendap"]["cmems"][dataset]["url"]
    return cmems_url


def _get_cmems_datastore(
    cmems_dataset_url: str,
    cmems_session: Session = CMEMS_SESSION,
):
    try:
        dataset = open_url(url=cmems_dataset_url, session=cmems_session)
        return xr.backends.PydapDataStore(dataset)
    except exc.HTTPError:
        retry = 0
        if retry == 0:
            print("\nlogin to CMEMS...")
            retry += 1
            CMEMS_SESSION = get_cmems_session(
                os.environ.get("CMEMS_username"), os.environ.get("CMEMS_password")
            )
            dataset = open_url(url=cmems_dataset_url, session=CMEMS_SESSION)
            return xr.backends.PydapDataStore(dataset)
        if retry >= 1:
            raise ValueError("CMEMS login fails (try later...)")
    except ValueError as e:
        raise e
