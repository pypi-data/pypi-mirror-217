"""Preprocessing of the connections to carry out the connection to external data providers"""

from xarray.backends.pydap_ import PydapDataStore

from pyteseo.providers.cmems import get_cmems_opendap_datastore
from pyteseo.providers.emodnet import get_emodnet_opendap_urls
from pyteseo.providers.ihcantabria import (
    get_ihcantabria_opendap_urls,
    get_ihcantabria_wfs_params,
)
from pyteseo.preprocess.dataset import get_dataset
from pyteseo.preprocess.geodataframe import get_geodataframe
from pyteseo.providers import DATASETS


def preprocess_online_provider(
    provider: str, service: str, dataset_name: str
) -> tuple:  # ) -> list | str | tuple | PydapDataStore:
    """collection of preprocesses to obtain the requeired parameters to conect to a specific provider-service-dataset

    Args:
        provider (str): name of the external provider
        service (str): data service used for the connection
        dataset_name (str): name of the dataset (defined locally in json file)

    Raises:
        ValueError: if service or provider not found

    Returns:
        list | str | tuple | PydapDataStore: urls, url, wfs_param or datastore to connect to an external provider
    """
    if service == "opendap" and provider == "ihcantabria":
        return get_ihcantabria_opendap_urls(dataset_name)

    elif service == "opendap" and provider == "cmems":
        return get_cmems_opendap_datastore(dataset_name)

    elif service == "opendap" and provider == "emodnet":
        return get_emodnet_opendap_urls(dataset_name)

    elif service == "wfs" and provider == "ihcantabria":
        return get_ihcantabria_wfs_params(dataset_name)

    else:
        raise ValueError(
            f"Provider or Service not found [provider={provider}, service={service}]"
        )


def get_provider_dataset(
    connection_params,
    variables: dict = None,
    bbox: tuple = None,
    timebox: tuple = None,
    coord_t: str = None,
    coord_x: str = None,
    coord_y: str = None,
    interp_oclock: str = None,
) -> object:
    if isinstance(connection_params, tuple):
        return get_geodataframe(*connection_params, bbox)

    elif (
        isinstance(connection_params, str)
        or isinstance(connection_params, list)
        or isinstance(connection_params, PydapDataStore)
    ):
        return get_dataset(
            connection_params,
            variables,
            bbox,
            timebox,
            coord_t,
            coord_x,
            coord_y,
            interp_oclock,
        )

    else:
        raise ValueError(f"Bad connection_params [{connection_params}]")


def get_variable_map(provider: str, service: str, dataset_name: str) -> tuple:
    return DATASETS[service][provider][dataset_name]["variable_map"]
