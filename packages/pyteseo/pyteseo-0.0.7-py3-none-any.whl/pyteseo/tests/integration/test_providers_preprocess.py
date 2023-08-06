from __future__ import annotations

import pytest
from xarray.backends.pydap_ import PydapDataStore

from pyteseo.providers.connection import preprocess_online_provider


@pytest.mark.parametrize(
    "provider, service, dataset, result_type",
    [
        ("ihcantabria", "opendap", "cmems_ibi_hourly", str),
        ("ihcantabria", "opendap", "noaa_gfs_hourly", list),
        ("ihcantabria", "wfs", "noaa_gshhs", tuple),
        ("bad_provider", "wfs", "noaa_gshhs", ValueError),
        ("ihcantabria", "bad_service", "noaa_gshhs", ValueError),
        ("ihcantabria", "wfs", "bad_dataset_name", KeyError),
        ("ihcantabria", "opendap", "bad_dataset_name", KeyError),
        ("cmems", "opendap", "cmems_ibi_hourly", PydapDataStore),
    ],
)
def test_preprocess_providers(provider, service, dataset, result_type):
    if result_type in [ValueError, KeyError]:
        with pytest.raises(result_type):
            _ = preprocess_online_provider(provider, service, dataset)
    else:
        connection_params = preprocess_online_provider(provider, service, dataset)
        assert isinstance(connection_params, result_type)
        assert connection_params
