from pathlib import Path
from shutil import rmtree

import pandas as pd
import pytest

from pyteseo.__init__ import __version__ as v
from pyteseo.io.results import (
    read_grids,
    read_particles,
    read_properties,
)

# data_path = Path(__file__).parent.parent / "data"
# data_path = Path(__file__).parent.parent / "data/drift_simulation"
# data_path = Path(__file__).parent.parent / "data/oil_simulation"
data_path = Path(__file__).parent.parent / "data/hns_simulation"
tmp_path = Path(f"./tmp_pyteseo_{v}_tests")


@pytest.fixture
def setup_teardown():
    if not tmp_path.exists():
        tmp_path.mkdir()
    yield
    if tmp_path.exists():
        rmtree(tmp_path)


@pytest.mark.parametrize("error", [(None), ("no_match")])
def test_read_particles_results(error):
    if error == "no_match":
        with pytest.raises(FileNotFoundError):
            df = read_particles(dir_path="data_path")

    df = read_particles(dir_path=data_path)
    assert isinstance(df, pd.DataFrame)


@pytest.mark.parametrize("error", [(None), ("no_match")])
def test_read_properties_results(error):
    if error == "no_match":
        with pytest.raises(FileNotFoundError):
            df = read_properties(dir_path="data_path")

    df = read_properties(dir_path=data_path)
    assert isinstance(df, pd.DataFrame)


@pytest.mark.parametrize("error", [(None), ("no_match")])
def test_read_grids_results(error):
    if error == "no_match":
        with pytest.raises(FileNotFoundError):
            df = read_grids(dir_path="data_path")

    df = read_grids(dir_path=data_path)
    assert isinstance(df, pd.DataFrame)
