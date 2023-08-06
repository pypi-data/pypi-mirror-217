import pytest

from pathlib import Path
from shutil import rmtree
from uuid import uuid4
from datetime import datetime, timedelta
from random import randint

from pyteseo.preprocess.teseo_forcing import create_forcings
from pyteseo.preprocess.teseo_domain import create_domain
from pyteseo.wrapper import TeseoWrapper
from pyteseo.plot.animations import animate_particles


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


@pytest.fixture
def now():
    return datetime.now().replace(second=0, microsecond=0)


@pytest.fixture
def bbox():
    return (-10, 43.2, -1, 45)


@pytest.fixture
def duration(now):
    return timedelta(hours=36)


@pytest.fixture
def spill_points(now):
    return [
        {
            "release_time": now + timedelta(minutes=randint(0, 59)),
            "lon": -6,
            "lat": 44,
            "initial_width": 1,
            "initial_length": 1,
            "mass": 5000,
            "substance": "lagunillas",
            "thickness": 0.1,
        }
    ]


@pytest.fixture
def forcings():
    return


@pytest.fixture
def simulation_parameters(duration):
    return {
        "mode": "2d",
        "motion": "forward",
        "substance_type": "oil",
        "duration": duration,
        "timestep": timedelta(minutes=1),
        "use_coastline": True,
    }


@pytest.mark.slow
def test_global_simulation(
    setup_teardown, test_dir, simulation_parameters, forcings, bbox, spill_points
):
    elevation_source = {
        "online_provider": "ihcantabria",
        "service": "opendap",
        "dataset_name": "gebco_2020",
    }
    coastline_source = {
        "online_provider": "ihcantabria",
        "service": "wfs",
        "dataset_name": "noaa_gshhs",
    }
    domain_path, _, _ = create_domain(
        "test_domain",
        elevation_source,
        coastline_source,
        bbox,
        test_dir,
    )

    job = TeseoWrapper(dir_path=test_dir)
    job.load_domain(domain_path)

    bbox = job.grid.extent.bounds

    t_ini = min([spill_point["release_time"] for spill_point in spill_points])
    timebox = (t_ini, t_ini + simulation_parameters["duration"])

    forcings = {
        "currents": {
            "dataset_name": "cmems_ibi_hourly",
            "source": {"online_provider": "ihcantabria", "service": "opendap"},
        },
        "winds": {
            "dataset_name": "dwd_icon_europe",
            "source": {"online_provider": "ihcantabria", "service": "opendap"},
        },
    }
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
        1,
        Path(job.path, "particles_spill_01.gif"),
        False,
    )
    # plot_extents(job.grid.path, job.coastline.path, job.currents.path, job.winds.path, job.waves.path)

    assert Path(job.path, "particles_spill_01.gif").exists()
