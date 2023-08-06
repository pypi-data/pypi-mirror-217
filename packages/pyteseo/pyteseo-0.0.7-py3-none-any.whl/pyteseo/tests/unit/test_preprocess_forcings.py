import pytest
import xarray as xr
import numpy as np
from pathlib import Path
from shutil import rmtree
from pyteseo.preprocess.teseo_forcing import (
    standarize_dataset_varnames,
    dataset_to_teseo_txt,
)
from pyteseo.defaults import DATASETS_VARNAMES, FILE_PATTERNS, FILE_NAMES


tmp_path = Path(f"./tmp_{__name__}")


@pytest.fixture
def setup_teardown():
    if not tmp_path.exists():
        tmp_path.mkdir()
    yield
    if tmp_path.exists():
        rmtree(tmp_path)


source_ds = xr.open_dataset("pyteseo/tests/data/currents.nc")
source_ds = source_ds.rename(
    {"lon": "longitude", "lat": "latitude", "u": "u_vel", "v": "v_vel"}
)
source_ds["time"] = source_ds["time"] + np.timedelta64(3, "m") + np.timedelta64(33, "s")


def test_forcing_dataset_to_txt(setup_teardown):
    variable_map = {
        "x": "longitude",
        "y": "latitude",
        "t": "time",
        "u": "u_vel",
        "v": "v_vel",
    }
    forcing_type = "currents"
    dataset_to_teseo_txt(source_ds, tmp_path, forcing_type, variable_map)
    assert Path(tmp_path, FILE_NAMES[forcing_type]).exists()
    assert all(
        [
            Path(str(path)).exists()
            for path in Path(tmp_path).glob(FILE_PATTERNS[forcing_type])
        ]
    )


def test_standarize_names():
    variables = {
        "t": "time",
        "x": "longitude",
        "y": "latitude",
        "u": "u_vel",
        "v": "v_vel",
    }
    forcing_type = "currents"

    ds = standarize_dataset_varnames(
        ds=source_ds, dataset_type=forcing_type, variable_map=variables
    )

    assert all(
        [
            value in list(ds.variables)
            for _, value in DATASETS_VARNAMES[forcing_type].items()
        ]
    )


def test_standarize_names_fail():
    variables = {
        "x": "longitude",
        "y": "latitude",
        "v": "v_vel",
    }
    forcing_type = "currents"

    with pytest.raises(ValueError):
        _ = standarize_dataset_varnames(
            ds=source_ds, dataset_type=forcing_type, variable_map=variables
        )
