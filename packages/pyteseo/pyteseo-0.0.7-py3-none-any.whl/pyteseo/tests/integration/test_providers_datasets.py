from __future__ import annotations

from datetime import datetime, timedelta

import geopandas as gpd
import pytest
import xarray as xr

from pyteseo.providers.connection import (
    get_provider_dataset,
    preprocess_online_provider,
)

connection_params_opendap_cmems = preprocess_online_provider(
    "cmems", "opendap", "cmems_ibi_hourly"
)
connection_params_opendap_ihcantabria = preprocess_online_provider(
    "ihcantabria", "opendap", "cmems_ibi_hourly"
)
connection_params_wfs = preprocess_online_provider("ihcantabria", "wfs", "noaa_gshhs")

variables = ["uo", "vo"]
bbox = (1.05, 38.55, 1.7, 39.2)
timebox = (
    datetime(2023, 2, 22, 12, 0, 0),
    datetime(2023, 2, 22, 12, 0, 0) + timedelta(days=1),
)


@pytest.mark.slow
@pytest.mark.parametrize(
    "connection_params, variables, bbox, timebox, coord_t, coord_x, coord_y, result_type",
    [
        (connection_params_wfs, None, bbox, None, None, None, None, gpd.GeoSeries),
        (
            connection_params_opendap_ihcantabria,
            None,
            None,
            None,
            None,
            None,
            None,
            xr.Dataset,
        ),
        (
            connection_params_opendap_cmems,
            None,
            None,
            None,
            None,
            None,
            None,
            xr.Dataset,
        ),
        (
            connection_params_opendap_ihcantabria,
            variables,
            None,
            None,
            None,
            None,
            None,
            xr.Dataset,
        ),
        (
            connection_params_opendap_ihcantabria,
            None,
            bbox,
            None,
            None,
            "longitude",
            "latitude",
            xr.Dataset,
        ),
        (
            connection_params_opendap_cmems,
            None,
            None,
            timebox,
            "time",
            None,
            None,
            xr.Dataset,
        ),
        (
            connection_params_opendap_ihcantabria,
            None,
            bbox,
            None,
            None,
            None,
            None,
            ValueError,
        ),
        (
            connection_params_opendap_ihcantabria,
            None,
            None,
            timebox,
            None,
            None,
            None,
            ValueError,
        ),
    ],
)
def test_get_provider_dataset(
    connection_params, variables, bbox, timebox, coord_t, coord_x, coord_y, result_type
):
    if result_type in [ValueError]:
        with pytest.raises(result_type):
            _ = get_provider_dataset(
                connection_params, variables, bbox, timebox, coord_t, coord_x, coord_y
            )
    else:
        data = get_provider_dataset(
            connection_params, variables, bbox, timebox, coord_t, coord_x, coord_y
        )
        assert isinstance(data, result_type)
        if isinstance(data, xr.Dataset):
            assert len(data[list(data.coords)[0]]) > 15
            assert len(data[list(data.coords)[1]]) > 15
            assert len(data[list(data.coords)[2]]) > 15
        elif isinstance(data, gpd.GeoDataFrame):
            assert len(data) > 10
