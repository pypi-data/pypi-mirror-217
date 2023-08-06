from pathlib import Path
from shutil import rmtree
from uuid import uuid4

import pytest

from pyteseo.defaults import FILE_NAMES
from pyteseo.preprocess.teseo_domain import create_domain


bbox_ibiza = (1.05, 38.55, 1.7, 39.2)
bbox_bay_of_santander = (-3.9, 43.39, -3.7, 43.5)
bbox_cantabrian_sea = (-11.5, 43.25, -1, 45)
bbox_bay_of_biscay = (-11, 43, -1, 48.5)


data_path = Path(__file__).parent.parent / "data"


@pytest.fixture
def test_dir():
    return Path(f"./tmp_pyteseo_tests_{str(uuid4())[-12:]}")


@pytest.fixture
def setup_teardown(test_dir):
    if not test_dir.exists():
        test_dir.mkdir()
    yield
    if test_dir.exists():
        rmtree(test_dir)


@pytest.mark.slow
@pytest.mark.parametrize(
    "name, elevation_source, coastline_source, bbox, compress_output",
    [
        (
            "bay_of_santander",
            {
                "online_provider": "ihcantabria",
                "service": "opendap",
                "dataset_name": "emodnet_2020",
            },
            {
                "local_path": Path(data_path, "shapefile_cantabria/Cantabria.shp"),
                "file_format": "shp",
            },
            bbox_bay_of_santander,
            False,
        ),
        (
            "ibiza",
            {
                "online_provider": "ihcantabria",
                "service": "opendap",
                "dataset_name": "emodnet_2020",
            },
            {
                "online_provider": "ihcantabria",
                "service": "wfs",
                "dataset_name": "noaa_gshhs",
            },
            bbox_ibiza,
            False,
        ),
        (
            "ibiza",
            {
                "online_provider": "ihcantabria",
                "service": "opendap",
                "dataset_name": "emodnet_2020",
            },
            {
                "online_provider": "ihcantabria",
                "service": "wfs",
                "dataset_name": "noaa_gshhs",
            },
            bbox_ibiza,
            True,
        ),
    ],
)
def test_create_domain(
    setup_teardown,
    name,
    elevation_source,
    coastline_source,
    bbox,
    test_dir,
    compress_output,
):
    domain_path, domain_bbox, cell_properties = create_domain(
        name,
        elevation_source,
        coastline_source,
        bbox,
        test_dir,
        compress_output,
    )

    if compress_output:
        assert Path(domain_path).exists()
        # TODO - unzip file

    assert Path(domain_path, FILE_NAMES["grid"])
    assert Path(domain_path, FILE_NAMES["coastline"])

    assert domain_bbox[0] <= bbox[0]
    assert domain_bbox[1] <= bbox[1]
    assert domain_bbox[2] >= bbox[2]
    assert domain_bbox[3] >= bbox[3]

    assert len(cell_properties) == 4
