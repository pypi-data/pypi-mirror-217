from datetime import datetime, timedelta
from pathlib import Path
from random import randint
from shutil import rmtree
from uuid import uuid4

import pytest

from pyteseo.preprocess.teseo_forcing import create_forcings
from pyteseo.wrapper import TeseoWrapper
from pyteseo.plot.animations import animate_particles

# TODO - SET UP SIMULATIONS FOR IBIZA MOCKUP DOMAIN, DRIFTER, OIL AND HNS


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


now = datetime.utcnow().replace(microsecond=0, second=0)


@pytest.fixture
def domain_path():
    return Path(__file__).parent.parent / "data/ibiza_domain"


@pytest.fixture
def simulation_parameters():
    return {
        "mode": "2d",
        "motion": "forward",
        "substance_type": None,
        "duration": timedelta(hours=12),
        "timestep": timedelta(minutes=1),
        "use_coastline": True,
    }


@pytest.fixture
def forcings():
    return {
        "currents": {
            "dataset_name": "cmems_ibi_hourly",
            "source": {"online_provider": "ihcantabria", "service": "opendap"},
        },
        "winds": {
            "dataset_name": "dwd_icon_europe",
            "source": {"online_provider": "ihcantabria", "service": "opendap"},
        },
    }


@pytest.mark.slow
@pytest.mark.parametrize(
    "substance_type, spill_points",
    [
        (
            "drifter",
            [
                {
                    "release_time": now,
                    "lon": 1.3,
                    "lat": 38.8,
                    "initial_width": 1,
                    "initial_length": 1,
                },
                {
                    "release_time": now + timedelta(minutes=randint(0, 59)),
                    "lon": 1.5,
                    "lat": 38.9,
                    "initial_width": 1,
                    "initial_length": 1,
                },
            ],
        ),
        (
            "oil",
            [
                {
                    "release_time": now,
                    "lon": 1.29,
                    "lat": 38.8,
                    "initial_width": 1,
                    "initial_length": 1,
                    "mass": 5000,
                    "substance": "lagunillas",
                    "thickness": 0.1,
                },
                {
                    "release_time": now + timedelta(minutes=randint(0, 59)),
                    "lon": 1.4,
                    "lat": 38.8,
                    "initial_width": 1,
                    "initial_length": 1,
                    "mass": 5000,
                    "substance": "tia juana",
                    "thickness": 0.1,
                },
            ],
        ),
        (
            "hns",
            [
                {
                    "release_time": now,
                    "lon": 1.29,
                    "lat": 38.8,
                    "initial_width": 1,
                    "initial_length": 1,
                    "mass": 5000,
                    "substance": "acetona",
                    "thickness": 0.1,
                },
                {
                    "release_time": now + timedelta(minutes=randint(0, 59)),
                    "lon": 1.5,
                    "lat": 38.8,
                    "initial_width": 1,
                    "initial_length": 1,
                    "mass": 5000,
                    "substance": "benceno",
                    "thickness": 0.1,
                },
            ],
        ),
    ],
)
def test_simulation_from_online_inputs(
    setup_teardown,
    test_dir,
    domain_path,
    simulation_parameters,
    forcings,
    substance_type,
    spill_points,
):
    simulation_parameters["substance_type"] = substance_type

    job = TeseoWrapper(dir_path=test_dir)
    job.load_domain(domain_path)

    bbox = job.grid.extent.bounds

    t_ini = min([spill_point["release_time"] for spill_point in spill_points])
    timebox = (t_ini, t_ini + simulation_parameters["duration"])

    forcings_timebox = create_forcings(
        forcings, bbox, timebox, output_dir=job.input_dir
    )
    job.load_forcings()
    simulation_parameters["forcings_init_time"] = forcings_timebox[0]
    user_parameters = simulation_parameters
    user_parameters["spill_points"] = spill_points
    job.setup(user_parameters)
    job.run()
    animate_particles(
        job.path,
        job.coastline.path,
        job.grid.path,
        2,
        Path(job.path, "particles_spill_01.gif"),
        False,
    )
    assert Path(job.path, "particles_spill_01.gif").exists()
    assert Path(job.path, "grid_coordinates.txt").exists()
    assert (
        len([str(path) for path in list(Path(job.path).glob("*_particles_*.txt"))]) > 0
    )
    assert len([str(path) for path in list(Path(job.path).glob("*_grid_*.txt"))]) > 0
    assert (
        len([str(path) for path in list(Path(job.path).glob("*_properties_*.txt"))]) > 0
    )


# @pytest.mark.slow
# @pytest.mark.parametrize(
#     "name, elevation_source, coastline_source, bbox, compress_output",
#     [
#         (
#             "ibiza",
#             {
#                 "online_provider": "ihcantabria",
#                 "service": "opendap",
#                 "dataset_name": "emodnet_2020",
#             },
#             {
#                 "online_provider": "ihcantabria",
#                 "service": "wfs",
#                 "dataset_name": "noaa_gshhs",
#             },
#             bbox_ibiza,
#         ),
#     ],
# )
# def test_simulation_from_local_inputs():
#     pass
