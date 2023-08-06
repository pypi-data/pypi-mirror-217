"""Definition of default values, keys, parameters and varaible maps"""

from datetime import timedelta

import numpy as np


DIRECTORY_NAMES = {"input": "input", "output": "output"}

FILE_NAMES = {
    "grid": "grid.dat",
    "results_grid": "results_grid.dat",
    "coastline": "costa.dat",  # FIXME - "coastline.dat"
    "currents": "lstcurr.pre",
    "winds": "lstwinds.pre",
    "waves": "lstwaves.pre",
    "currents_depthavg": "lstcurr_depthavg.pre",
    "teseo_grid_coordinates": "grid_coordinates.txt",
}

FILE_PATTERNS = {
    "polygons": "costa_poligono*.dat",
    "currents": "currents_*h.txt",
    "winds": "winds_*h.txt",
    "waves": "waves_*h.txt",
    "cfg": "*.cfg",
    "run": "*.run",
    "teseo_particles": "*_particles_*.txt",
    "teseo_properties": "*_properties_*.txt",
    "teseo_grids": "*_grid_*.txt",
    "export_particles": "particles_*.*",
    "export_properties": "properties_*.*",
    "export_grids": "grids_*.*",
}

# FIXME - DELETE VARIABLE_NAMES. USE FORCINGS VARAIBLES INSTEAD!
VARIABLE_NAMES = {
    "currents": {"coords": ["time", "lon", "lat"], "vars": ["u", "v"]},
    "winds": {"coords": ["time", "lon", "lat"], "vars": ["u", "v"]},
    "waves": {"coords": ["time", "lon", "lat"], "vars": ["hs", "dir", "tp"]},
    "currents_depthavg": {
        "coords": ["time", "lon", "lat"],
        "vars": ["u", "v"],
    },
}
# NOTE - MAYBE I CAN DELETE COORDINATE_NAMES ALSO
COORDINATE_NAMES = {"t": "time", "x": "lon", "y": "lat", "z": "depth"}

DATASETS_VARNAMES = {
    "currents": {"t": "time", "x": "lon", "y": "lat", "u": "u", "v": "v"},
    "winds": {"t": "time", "x": "lon", "y": "lat", "u": "u", "v": "v"},
    "currents_depthavg": {"t": "time", "x": "lon", "y": "lat", "u": "u", "v": "v"},
    "waves": {
        "t": "time",
        "x": "lon",
        "y": "lat",
        "hs": "hs",
        "dir": "dir",
        "tp": "tp",
    },
    "topobathymetry": {"x": "lon", "y": "lat", "elevation": "elevation"},
    "bathymetry": {"x": "lon", "y": "lat", "depth": "depth"},
    "coastline": {"x": "lon", "y": "lat"},
}


RESULTS_MAP = {
    "time (h)": "time",
    "longitude (º)": "lon",
    "latitude (º)": "lat",
    "depth (m)": "depth",
    "status_index (-)": "status_index",
    "spill_id (-)": "spill_id",
    "subspill_id (-)": "subspill_id",
    "centre_of_mass_lon (º)": "centroid_lon",
    "centre_of_mass_lat (º)": "centroid_lat",
    "area (m2)": "area",
    "thickness (m)": "thickness",
    "density (kg/m3)": "density",
    "kinematic_viscosity (cst)": "kinematic_viscosity",
    "surface (kg)": "surface",
    "beached (kg)": "beached",
    "evaporated (kg)": "evaporated",
    "dispersed (kg)": "dispersed",
    "column (kg)": "column",
    "floor (kg)": "floor",
    "emulsified_water (kg)": "emulsified_water",
    "emulsified_beached (kg)": "emulsified_beached",
    "outside (kg)": "outside",
    "balance (%)": "balance_percentage",
    "surface (%)": "surface_percentage",
    "beached (%)": "beached_percentage",
    "evaporated (%)": "evaporated_percentage",
    "dispersed (%)": "dispersed_percentage",
    "column (%)": "column_percentage",
    "floor (%)": "floor_percentage",
    "emulsified (%)": "emulsified_percentage",
    "outside (%)": "outside_percentage",
    "surface_mass_per_area (kg/m2)": "surface_mass_per_area",
    "presence_probability (%)": "presence_probability",
    "particles_per_cell (-)": "particles_count",
    "dissolved_mass_per_area (kg/m2)": "dissolved_mass_per_area",
}

CFG_MAIN_PARAMETERS = {
    "seawater_kinematic_viscosity": 1.004e-6,
    "seawater_temperature": 17,
    "seawater_density": 1025,
    "air_temperature": 15.5,
    "suspended_solid_concentration": 10,
    "water_slope": 0.0005,
    "release_type": "instantaneous",
    "release_duration": timedelta(hours=0),
    "release_timestep": timedelta(minutes=0),
}

CFG_SPILL_POINT_PARAMETERS = {
    "depth": np.nan,
    "initial_width": np.nan,
    "initial_length": np.nan,
    "volume": np.nan,
    "thickness": np.nan,
    "min_thickness": 0.00005,
    "degradation_rate": np.nan,
    "wind_drag_alpha_coefficient": 0.2,
    "wind_drag_beta_coefficient": 0,
    "currents_factor": 1,
    "wave_factor": 1,
    "dispersion_flag": 1,
    "dispersion_coefficient": 2,
    "vertical_dispersion_coefficient": 0.01,
}

CFG_PROCESSES_PARAMETERS = {
    "drifter": {
        "spreading": False,
        "spreading_formulation": "adios2",
        "spreading_duration": timedelta(hours=0),
        "evaporation": False,
        "emulsification": False,
        "vertical_dispersion": False,
        "dissolution": False,
        "volatilization": False,
        "sedimentation": False,
        "biodegradation": False,
    },
    "oil": {
        "spreading": False,
        "spreading_formulation": "adios2",
        "spreading_duration": timedelta(hours=0),
        "evaporation": True,
        "emulsification": True,
        "vertical_dispersion": False,
        "dissolution": False,
        "volatilization": False,
        "sedimentation": False,
        "biodegradation": False,
    },
    "hns": {
        "spreading": True,
        "spreading_formulation": "mohid-hns",
        "spreading_duration": timedelta(hours=0),
        "evaporation": True,
        "emulsification": False,
        "vertical_dispersion": False,
        "dissolution": True,
        "volatilization": True,
        "sedimentation": False,
        "biodegradation": False,
    },
}

RUN_MAIN_PARAMETERS = {
    "environment": "marine",
    "mode": "2d",
    "motion": "forward",
    "near_field_3d": False,
    "input_directory": True,
    "use_coastline": True,
    "beaching_algorithm": "high",
    "n_particles": 1000,
    "use_restart": False,
    "timestep": timedelta(minutes=1),
    "use_time_interpolation_currents": False,
    "use_time_interpolation_winds": False,
    "use_time_interpolation_waves": False,
    "execution_scheme": "euler",
    "particles_save_dt": timedelta(hours=1),
    "properties_save_dt": timedelta(hours=1),
    "grids_save_dt": timedelta(hours=1),
    "save_particles": 1,
    "save_properties": 1,
    "save_grids": 1,
}

CFG_MAIN_MANDATORY_KEYS = [
    "substance_type",
    "forcings_init_time",
    "duration",
    "spill_points",
]

CFG_SPILL_POINT_MANDATORY_KEYS = [
    "lon",
    "lat",
    "release_time",
    "initial_width",
    "initial_length",
]

CFG_KEYS_FOR_TABLE_1 = [
    "hours_to_release",
    "mass",
    "lon",
    "lat",
    "depth",
    "initial_width",
    "initial_length",
    "thickness",
    "min_thickness",
    "volume",
    "refined",
    "density",
    "density_temp_ref",
    "viscosity",
    "viscosity_temp_ref",
    "solubility",
    "solubility_temp_ref",
    "vapour_pressure",
    "vapour_pressure_temp_ref",
    "molecular_weight",
    "organic",
    "evaporation_max",
    "evaporation_min",
    "emulsification_max",
    "seawater_density",
    "seawater_temperature",
    "air_temperature",
]

CFG_KEYS_FOR_TABLE_2 = [
    "suspended_solid_concentration",
    "sorption_coeficient",
    "degradation_rate",
]

CFG_KEYS_FOR_TABLE_3 = [
    "currents_factor",
    "wind_drag_alpha_coefficient",
    "wind_drag_beta_coefficient",
    "waves_factor",
    "dispersion_flag",
    "dispersion_coefficient",
    "vertical_dispersion_coefficient",
    "water_slope",
]
