# TODO - Install datahubclient
# pip install git+ssh://git@github.com/IHCantabria/datahub.client@v0.9.4 --no-deps

from datahub.products import Products
from datahub.catalog import Catalog
import xarray as xr

from pyteseo.providers import DATASETS


def get_ihcantabria_opendap_urls(dataset_name: str) -> list:
    """obtain opendap urls from datahub for IHCantabria opendap datasets

    Args:
        dataset_name (str): name of the dataset

    Returns:
        list: opendap urls
    """
    datahub_id = DATASETS["opendap"]["ihcantabria"][dataset_name]["id"]
    datahub_username = DATASETS["opendap"]["ihcantabria"][dataset_name]["username"]
    datahub_password = DATASETS["opendap"]["ihcantabria"][dataset_name]["password"]

    return _retrieve_urls_to_datahub(datahub_id, datahub_username, datahub_password)


def get_ihcantabria_wfs_params(dataset_name):
    url = DATASETS["wfs"]["ihcantabria"][dataset_name]["url"]
    version = DATASETS["wfs"]["ihcantabria"][dataset_name]["version"]
    feature = DATASETS["wfs"]["ihcantabria"][dataset_name]["feature"]

    return url, version, feature


def _retrieve_urls_to_datahub(
    datahub_id: int, username: str = None, password: str = None
) -> xr.Dataset:
    """retrieve openadp urls through datahub (IHCantabria)

    Args:
        datahub_id (int): datahub product id.
        username (str, optional): username for restricted product. Defaults to None.
        password (str, optional): password for restricted product. Defaults to None.

    Returns:
        xr.Dataset: complete time-merged dataset
    """
    product = Products().get(datahub_id)
    if product.license == "Restricted":
        c = Catalog(product, {username: password})
    else:
        c = Catalog(product)

    if "opendap_url" in c.datasets[0].__dict__.keys():
        opendap_urls = list(map(lambda dataset: dataset.opendap_url, c.datasets))
        opendap_urls.sort(reverse=True)
        return opendap_urls if len(opendap_urls) > 1 else opendap_urls[0]
