import numpy as np
import pandas as pd

from pyteseo.defaults import COORDINATE_NAMES


def _check_cte_dt(df):
    dt = np.unique(np.diff(df["time"].unique()))
    if len(dt) > 1:
        print(f"WARNING: Forcing time steps are not constant {dt}")


def _convert_longitude_range(
    df: pd.DataFrame, lon_varname: str = "lon"
) -> pd.DataFrame:
    """convert longitude range to [-180, 180]

    Args:
        df (pd.DataFrame): dataframe
        lon_varname (str, optional): _description_. Defaults to "lon".

    Returns:
        pd.DataFrame: transformed DataFrame
    """
    df["lon"] = df["lon"].apply(lambda x: x - 360 if x > 180 else x)
    return df


def _warn_lonlat_range(df):
    if (
        df.lon.max() > 180
        or df.lon.min() < -180
        or df.lat.max() > 90
        or df.lat.min() < -90
    ):
        print(
            "WARNING: lon and lat values should be inside ranges lon[-180,180] and lat[-90,90]!"
        )


def _warn_lonlat_soting(df):
    if not df[COORDINATE_NAMES["x"]].drop_duplicates().is_monotonic_increasing:
        print(
            f"WARNING: '{COORDINATE_NAMES['x']}' values should be monotonic increasing!"
        )
    if not df[COORDINATE_NAMES["y"]].drop_duplicates().is_monotonic_increasing:
        print(
            f"WARNING: '{COORDINATE_NAMES['y']}' values should be monotonic increasing!"
        )


def _check_varnames(df, vars):
    for varname in vars:
        if varname not in df.keys():
            raise ValueError(f"{varname} not founded in the DataFrame")


def _check_n_vars(df, varnames):
    if df.shape[1] != len(varnames):
        raise ValueError(
            f"DataFrame has {df.shape[1]} columns not equal to vars: {varnames}!"
        )


def _add_default_parameters(d, d_defaults):
    for default_key in d_defaults.keys():
        if default_key not in d.keys():
            d[default_key] = d_defaults[default_key]
    return d
