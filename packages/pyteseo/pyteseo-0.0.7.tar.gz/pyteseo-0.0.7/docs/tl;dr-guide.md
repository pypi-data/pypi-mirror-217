# TL;DR guide[^ref]
Short guide with examples to start working with pyTESEO.

[^ref]: [TL;DR](https://en.wikipedia.org/wiki/TL;DR) stands for "Too long; don't read".

---

## Create a TESEO domain
TESEO numerical domain is defined by two main files:
- **Grid-file**: structured grid where node values represents `depth` and by default, *-999* value represents `land` nodes.
- **Coastline-file**: polygon file representing the `coastline polygons` in the numerical domain. Polygons are defined by **(Lon,Lat)** values and **separated by (Nan,Nan)**

To create a domain from online data-providers you can use the function `create_domains` in the submodule {py:mod}`pyteseo.preprocess.teseo_domain` as shows the following example:

```{code-block} python
---
lineno-start: 0
caption: |
    Example script to create a domain using GEBCO bathymetry and GSHHS coastline
---

    from pyteseo.preprocess.teseo_domain import create_doamin

    # Define parameters

    bbox = (1.05, 38.55, 1.7, 39.2)

    elevation_source = {
        "online_provider": "ihcantabria",
        "service": "opendap",
        "dataset_name": "emodnet_2020",
    }

    coastline_source = {
        "online_provider": "ihcantabria",
        "service": "wfs",
        "dataset_name": "noaa_gshhs",
    }

    output_dir = "./"

    # Run the function
    domain_path, domain_bbox, cell_properties = create_domain(
        name,
        elevation_source,
        coastline_source,
        bbox,
        output_dir
    )

```
Results where provided in a new folder located at the `output_dir`, including a figure of the domain that is automatically generated.
![ibiza_domain_figure](../pyteseo/tests/data/ibiza_domain/ibiza_domain.png)

```{important}
- Domain limits will be always equal or larger than the boundary box required by the user
```


---


## Create forcings for TESEO
TESEO numerical forcings (currents, winds, waves) are defined by two kind of files:
1. **lstforcing.pre**: where a list of the forcing filenames are defined (one per forcing timestep)
2. **forcing_000h.txt**: where the (lon, lat u, v) or (lon, lat, hs, dir, tp) values are defined

To create forcings from online data-providers you can use the function `create_forcings` in the submodule {py:mod}`pyteseo.preprocess.teseo_forcing` as shows the following example:

```{code-block} python
---
lineno-start: 0
caption: |
    Example script to create forcings using online connection to metocean data-providers
---

    from pyteseo.preprocess.teseo_forcing import create_forcings
    from datetime import datetime, timedelta

    # Define parameters
    now = datetime.utcnow()

    timebox = (now, now + timedelta(hours=12))

    bbox = (1.05, 38.55, 1.7, 39.2)

    forcings = {
        "currents": {
            "source": {
                "online_provider": "ihcantabria",
                "service": "opendap",
            },
            "dataset_name": "cmems_ibi_hourly",
        },
        "winds": {
            "source": {
                "online_provider": "ihcantabria",
                "service": "opendap",
            },
            "dataset_name": "dwd_icon_europe",
        },
    }

    output_dir = "./"

    # Run the function
    model_timebox = create_forcings(forcings, bbox, timebox, output_dir)

```

Result files will be directly saved in the foder defined at `output_dir`.

```{important}
- Time box limits will be always equal or larger than the time box required by the user
- Data-providers are defined at the following [json-file](../pyteseo/providers/providers_registry.json)
- CMEMS data provider needs user authentication (see [installation](./get-started.md) section)
```

---


## Create a TESEO simulation
To carry out a TESEO simulation (generally speaking, "run TESEO job") it is necessary to create a bunch of input and configuration files in a determinist structure, like this:
``` bash
    /input                  # Input folder
    /input/domain-files     # domain files
    /input/forcings-files   # forcing files
    /teseo.cfg              # configuration file
    /teseo.run              # configuration file
    /teseo                  # model executable
```

In order to generate this structure and the configuration files required by the model, the user can use the classs `TeseoWrapper` located at {py:mod}`pyteseo.wrapper`. See example below:
```{code-block} python
---
lineno-start: 0
caption: |
    Example script to create a 12-hour TESEO simulation at ibiza domain
---

    from pathlib import Path
    from random import randint

    from pyteseo.wrapper import TeseoWrapper
    from pyteseo.tests import __file__


    domain_path = Path(__file__).parent / "data/ibiza_domain"
    now = datetime.utcnow()

    # Define spill_points
    spill_points = [
                {
                    "release_time": now,
                    "lon": 1.3,
                    "lat": 38.8,
                    "initial_width": 1,
                    "initial_length": 1,
                    "mass": 5000,
                    "substance": "lagunillas",
                    "thickness": 0.1,
                },
                {
                    "release_time": now + timedelta(minutes=randint(0, 59)),
                    "lon": 1.5,
                    "lat": 38.9,
                    "initial_width": 1,
                    "initial_length": 1,
                    "mass": 5000,
                    "substance": "tia juana",
                    "thickness": 0.1,
                },
            ]

    # Define forcings
    forcings = {
        "currents": {
            "source": {
                "online_provider": "ihcantabria",
                "service": "opendap",
            },
            "dataset_name": "cmems_ibi_hourly",
        },
        "winds": {
            "source": {
                "online_provider": "ihcantabria",
                "service": "opendap",
            },
            "dataset_name": "dwd_icon_europe",
        },
    }

    # Define simulation parameters
    simulation_params = {
        "mode": "2d",
        "motion": "forward",
        "substance_type": "oil",
        "duration": timedelta(hours=12),
        "timestep": timedelta(minutes=1),
        "use_coastline": True,
    }

    # Define job directory
    job_path = "./job_test

    # Generate job structure
    job = TeseoWrapper(job_path)
    print(job.input_path)               # Automatically generates a input subfolder

    # Load domain
    job.load_domain(domain_path)        # Copy domain-files to job's input subfolder

    # Create forcings at input folder (job.input_path)
    t_ini = min([spill_point["release_time"] for spill_point in spill_points])
    timebox = (t_ini, t_ini + simulation_parameters["duration"])

    forcings_timebox = create_forcings(forcings, bbox, timebox, job.input_dir)

    # set initial time according to your forcings
    simulation_params["forcings_init_time"] = forcings_timebox[0]

    # Load forcings
    job.load_forcings(job.input_path)   # Reads forcings located at input subfolder

    # Setup the simulation
    job.setup(simulation_params)        # Generates TESEO's cfg-file and run-file

    # Run the simulation
    job.run()                           # Execute TESEO model

```
TESEO custom-format results will be created at job.path folder, happy modelling! 😃

```{important}
- Forcing-files should be created before loading them with `job.load_forcings()` method.
- Not all the configuration parameters of the model are showed in this example.
- The user needs to define the path to the TESEO executable previously (see [installation](./get-started.md) section)
```


---


## Export TESEO simulation results to standard formats
TESEO model produce three different kinds of results in custom ascii format (.txt):

1. Particles `*_particles_*.txt`: info about the trajectory and status of the particles.
2. Properties `*_properties_*.txt`: info about the properties of the spill.
3. Export grids `*_grid_*.txt`: info about grided values, as mass per area.

The user can easily transform this custom formats to standards (json, csv, geojson, netcdf...) by means of a couple of functions located in the subpackages {py:mod}`pyteseo.io.results`: `read_particles()`, `read_properties()`, and `read_grids()` to read TESEO results and {py:mod}`pyteseo.export`: `export_particles()`, `export_properties()` and `export_grids()` to generate new files in the standard format required.

```{code-block} python
---
lineno-start: 0
caption: |
    Example script to export TESEO results to geojson, csv and netcdf
---
    from pathlib import Path
    from pyteseo.io.results import read_grids, read_particles, read_properties
    from pyteseo.export import export_particles, export_properties, export_grids

    # Supose results are located in results_dir
    results_dir = Path("./test_simulation")

    # generate folder for postprocessed resutls
    output_dir = Path("./test_simulation/output")
    output_dir.mkdir() if not output_dir.exists() else None

    # Particles
    df = read_particles(results_dir)
    export_particles(df, ["csv", "geojson"], output_dir)

    # Properties
    df = read_properties(results_dir)
    export_properties(df, ["csv"], output_dir)

    # Grids
    df = read_grids(results_dir)
    export_grids(df, ["csv", "netcdf"], output_dir)

```

```{important}
- Exported files are generated with standard filename patterns defined in {py:mod}`pyteseo.defaults`
```

---

## Perform basic plots
pyTESEO also offers a couple of functions to quickly produce some general figures and animations. All these functions are located in the subpackage {py:mod}:`pyteseo.plot`.
See following examples:
```{warning}
⚠️🚧⚠️ - All these plots are under development
```

1. Plot domain
```{code-block} python
---
lineno-start: 0
caption: |
    Example script to plot TESEO domain
---
    from pyteseo.plot.figures import plot_domain

    grid_path = "./test_simulation/grid.dat"
    coastline_path = "./test_simulation/coastline.dat"

    plot_domain(grid_path, coastline_path)

```
will show something like:
![ibiza_domain_figure](../pyteseo/tests/data/ibiza_domain/ibiza_domain.png)

2. Plot simulation extents
```{code-block} python
---
lineno-start: 0
caption: |
    Example script to plot TESEO simulation extents
---
    from pyteseo.plot.figures import plot_domain

    grid_path = "./test_simulation/input/grid.dat"
    coastline_path = "./test_simulation/input/coastline.dat"
    currents_lst_path = "./test_simulation/input/lstcurr.pre"
    winds_lst_path = "./test_simulation/input/lstwinds.pre"
    waves_lst_path = "./test_simulation/input/lstwaves.pre"

    plot_extents(
        grid_path,
        coastline_path,
        currents_lst_path,
        winds_lst_path,
        waves_lst_path,
    )

```
will show something like:
![ibiza_extents_figure](./_static/ibiza_extents.png)


3. Create forcings animation
```{code-block} python
---
lineno-start: 0
caption: |
    Example script to plot TESEO forcings animation
---
    from pyteseo.plot.animation import animate_forcings

    grid_path = "./test_simulation/input/grid.dat"
    coastline_path = "./test_simulation/input/coastline.dat"
    currents_lst_path = "./test_simulation/input/lstcurr.pre"
    winds_lst_path = "./test_simulation/input/lstwinds.pre"

    animate_forcings(
        currents_lst_path,
        winds_lst_path,
        coastline_path,
        grid_path,
        scale=15,
    )

```
will show something like:
![forcings_animation](./_static/forcings.gif)


4. Create particles animation
```{code-block} python
---
lineno-start: 0
caption: |
    Example script to plot TESEO particles animation
---
    from pyteseo.plot.animation import animate_particles

    grid_path = "./test_simulation/input/grid.dat"
    coastline_path = "./test_simulation/input/coastline.dat"
    results_path = "./test_simulation"
    spill_id = 2
    animate_particles(
        results_path,
        coastline_path,
        grid_path,
        spill_id,
    )

```

will show something like:
![particles_animation_002](./_static/particles_spill_01.gif)


5. Create properties plot
```{code-block} python
---
lineno-start: 0
caption: |
    Example script to plot TESEO properties plot
---
    from pyteseo.plot.figures import plot_properties

```

will show something like:
<!-- ![particles_animation_002](./_static/particles_spill_01.gif) -->


6. Create mass superficial density plot
```{code-block} python
---
lineno-start: 0
caption: |
    Example script to plot TESEO grid results
---
    from pyteseo.plot.figures import plot_superficial_mass

```

will show something like:
<!-- ![particles_animation_002](./_static/particles_spill_01.gif) -->
