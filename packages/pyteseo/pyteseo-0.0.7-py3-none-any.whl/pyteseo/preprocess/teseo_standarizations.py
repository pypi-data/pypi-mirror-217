import xarray as xr
from pyteseo.defaults import DATASETS_VARNAMES


def standarize_dataset_varnames(
    ds: xr.Dataset,
    dataset_type: str,
    variable_map: dict,
) -> xr.Dataset:
    """Standarize variable names of the dataset based on the type of dataset, the variable mapping passed and the default variable names defined in DATASET_VARNAMES in pyteseo.defaults.py

    Args:
        ds (xr.Dataset): Dataset to be standarized
        dataset_type (str): Type of dataset, like: "bathymetry".
        variable_map (dict): Name in the original dataset, like: {"x": "lon", "y": "lat", "depth": "depth_msl"}.

    Raises:
        ValueError: Bad dataset_type or Bad variable_map

    Returns:
        xr.Dataset: dataset with TESEO defaults variable names.
    """

    if dataset_type not in DATASETS_VARNAMES.keys():
        raise ValueError(
            f"Bad dataset_type. Implemented dataset types are: {DATASETS_VARNAMES.keys()}"
        )

    vars_map = {
        value: DATASETS_VARNAMES[dataset_type][key]
        for key, value in variable_map.items()
        if key in list(DATASETS_VARNAMES[dataset_type].keys())
    }

    not_mapped = []
    ds = ds.drop(
        [coord for coord in list(ds.coords) if coord not in list(variable_map.values())]
    )
    ds = ds.rename(vars_map)

    not_mapped = [
        value
        for _, value in DATASETS_VARNAMES[dataset_type].items()
        if value not in list(ds.variables)
    ]
    if not_mapped:
        raise ValueError(
            f"Bad variable_map. Mandatory variable(s) ({not_mapped}) not founded in the dataset"
        )

    return ds


def interp_to_oclock_hours(ds: xr.Dataset) -> xr.Dataset:
    """Resample to 00:00 minutes:seconds if necesary (linear interpolation)

    Args:
        ds (xr.Dataset): source dataset

    Returns:
        xr.Dataset: data resample at 00:00 minutes:seconds
    """
    ds = ds.resample(time="1H").interpolate("linear")
    ds = ds.isel(time=slice(1, None))

    return ds
