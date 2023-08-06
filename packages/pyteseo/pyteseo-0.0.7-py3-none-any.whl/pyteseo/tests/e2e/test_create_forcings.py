from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path
from shutil import rmtree
from uuid import uuid4

import pytest

from pyteseo.defaults import FILE_NAMES
from pyteseo.preprocess.teseo_forcing import create_forcings

data_path = Path(__file__).parent.parent / "data"

# SPATIAL AND TEMPORAL DEFINITION
bbox = (1.05, 38.55, 1.7, 39.2)

# PROVIDERS CASES
user_t_ini = datetime.utcnow().replace(second=0, microsecond=0)
forcing_t_ini = user_t_ini.replace(minute=0, hour=0)

duration1 = timedelta(hours=6) + user_t_ini - forcing_t_ini
timebox1 = (forcing_t_ini, forcing_t_ini + duration1)

# LOCAL_PATH CASES
duration2 = timedelta(hours=5)
timebox2 = (datetime(2023, 5, 14, 6, 0, 0), datetime(2023, 5, 14, 6, 0, 0) + duration2)

currents_txt = [str(path) for path in Path(data_path).glob("currents_*.txt")]
currents_txt.sort()
winds_txt = [str(path) for path in Path(data_path).glob("winds_*.txt")]
winds_txt.sort()

duration3 = timedelta(hours=3)
timebox3 = (datetime(2023, 5, 14, 6, 0, 0), datetime(2023, 5, 14, 6, 0, 0) + duration3)


@pytest.fixture
def output_dir():
    return Path(f"./tmp_pyteseo_tests_{str(uuid4())[-12:]}")


@pytest.fixture
def setup_teardown(output_dir):
    if not output_dir.exists():
        output_dir.mkdir()
    yield
    if output_dir.exists():
        rmtree(output_dir)


@pytest.mark.slow
@pytest.mark.parametrize(
    "forcings, timebox",
    [
        (
            {
                "currents": {
                    "source": {
                        "local_path": currents_txt,
                        "file_format": "teseo_txt",
                    },
                    "dataset_name": "corrientes_german_txt",
                    "dt_h": 1,
                    "variable_map": {
                        "t": "time",
                        "x": "lon",
                        "y": "lat",
                        "u": "u",
                        "v": "v",
                    },
                },
                "winds": {
                    "source": {
                        "local_path": winds_txt,
                        "file_format": "teseo_txt",
                    },
                    "dataset_name": "vientos_german_txt",
                    "dt_h": 1,
                    "variable_map": {
                        "t": "time",
                        "x": "lon",
                        "y": "lat",
                        "u": "u",
                        "v": "v",
                    },
                },
            },
            timebox3,
        ),
        (
            {
                "currents": {
                    "source": {
                        "local_path": [Path(data_path, "currents.nc")],
                        "file_format": "netcdf",
                    },
                    "dataset_name": "corrientes_german",
                    "dt_h": 1,
                    "variable_map": {
                        "t": "time",
                        "x": "lon",
                        "y": "lat",
                        "u": "u",
                        "v": "v",
                    },
                },
                "winds": {
                    "source": {
                        "local_path": [Path(data_path, "winds.nc")],
                        "file_format": "netcdf",
                    },
                    "dataset_name": "vientos_german",
                    "dt_h": 1,
                    "variable_map": {
                        "t": "time",
                        "x": "lon",
                        "y": "lat",
                        "u": "u",
                        "v": "v",
                    },
                },
            },
            timebox2,
        ),
        (
            {
                "currents": {
                    "source": {
                        "online_provider": "ihcantabria",
                        "service": "opendap",
                    },
                    "dataset_name": "cmems_global_hourly",
                    "variable_map": None,
                },
                "winds": {
                    "source": {
                        "online_provider": "ihcantabria",
                        "service": "opendap",
                    },
                    "dataset_name": "dwd_icon_global",
                    "variable_map": None,
                },
            },
            timebox1,
        ),
        (
            {
                "currents": {
                    "source": {
                        "online_provider": "cmems",
                        "service": "opendap",
                    },
                    "dataset_name": "cmems_ibi_15min",
                    # "variable_map": None,
                },
                "winds": {
                    "source": {
                        "online_provider": "ihcantabria",
                        "service": "opendap",
                    },
                    "dataset_name": "dwd_icon_europe",
                    # "variable_map": None,
                },
            },
            timebox1,
        ),
    ],
)
def test_forcing_from_provider(setup_teardown, output_dir, forcings, timebox):

    model_timebox = create_forcings(forcings, bbox, timebox, output_dir)

    assert all(
        [
            Path(output_dir, FILE_NAMES[forcing_type]).exists()
            for forcing_type in forcings.keys()
        ]
    )
    assert model_timebox[0] <= timebox[0]
    assert model_timebox[1] >= timebox[1]
