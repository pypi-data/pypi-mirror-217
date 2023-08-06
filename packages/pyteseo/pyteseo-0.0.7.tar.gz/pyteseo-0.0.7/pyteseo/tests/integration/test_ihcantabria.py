import pytest
from pyteseo.providers.ihcantabria import (
    get_ihcantabria_opendap_urls,
    _retrieve_urls_to_datahub,
)


def test_get_any_opendap_urls_from_datahub():
    datahub_id = 57

    opendap_urls = _retrieve_urls_to_datahub(
        datahub_id=datahub_id,
    )
    assert len(opendap_urls) > 1


@pytest.mark.parametrize(
    "dataset_name, returned_class", [("noaa_gfs_hourly", list), ("gebco_2020", str)]
)
def test_get_ihcantabria_opendap_urls(dataset_name, returned_class):
    urls = get_ihcantabria_opendap_urls(dataset_name)
    assert isinstance(urls, returned_class)
