from pathlib import Path
from shutil import rmtree

import pytest

from pyteseo.__init__ import __version__ as v
from pyteseo.export.grids import export_grids
from pyteseo.export.particles import export_particles
from pyteseo.export.properties import export_properties
from pyteseo.io.results import (
    read_grids,
    read_particles,
    read_properties,
)

# data_path = Path(__file__).parent.parent / "data"
# data_path = Path(__file__).parent.parent / "data/drift_simulation"
data_path = Path(__file__).parent.parent / "data/oil_simulation"
# data_path = Path(__file__).parent.parent / "data/hns_simulation"
tmp_path = Path(f"./tmp_pyteseo_{v}_tests")


@pytest.fixture
def setup_teardown():
    if not tmp_path.exists():
        tmp_path.mkdir()
    yield
    if tmp_path.exists():
        rmtree(tmp_path)


@pytest.mark.parametrize(
    "file_format, output_dir, error",
    [
        ("csv", tmp_path, None),
        ("json", tmp_path, None),
        ("geojson", tmp_path, None),
        ("netcdf", tmp_path, "bad_format"),
    ],
)
def test_export_particles(file_format, output_dir, error, setup_teardown):
    df = read_particles(data_path)

    if error == "bad_format":
        with pytest.raises(ValueError):
            export_particles(df, file_format, output_dir)
    else:
        files = export_particles(df, file_format, output_dir)
        assert all([file.exists() for file in files])


@pytest.mark.parametrize(
    "file_format, output_dir, error",
    [
        ("csv", tmp_path, None),
        ("json", tmp_path, None),
        ("nc", tmp_path, "bad_format"),
    ],
)
def test_export_properties(file_format, output_dir, error, setup_teardown):
    df = read_properties(data_path)

    if error == "bad_format":
        with pytest.raises(ValueError):
            export_properties(df, file_format, output_dir)
    elif error == "not_implemented":
        with pytest.raises(NotImplementedError):
            export_properties(df, file_format, output_dir)
    else:
        files = export_properties(df, file_format, output_dir)
        assert all([file.exists() for file in files])


@pytest.mark.parametrize(
    "file_format, output_dir, error",
    [
        ("csv", tmp_path, None),
        ("json", tmp_path, None),
        ("netcdf", tmp_path, "None"),
        ("nc", tmp_path, "None"),
        ("geojson", tmp_path, "bad_format"),
    ],
)
def test_export_grids(file_format, output_dir, error, setup_teardown):
    df = read_grids(data_path)

    if error == "bad_format":
        with pytest.raises(ValueError):
            export_grids(df, file_format, output_dir)
    elif error == "not_implemented":
        with pytest.raises(NotImplementedError):
            export_grids(df, file_format, output_dir)
    else:
        files = export_grids(df, file_format, output_dir)
        assert all([file.exists() for file in files])
