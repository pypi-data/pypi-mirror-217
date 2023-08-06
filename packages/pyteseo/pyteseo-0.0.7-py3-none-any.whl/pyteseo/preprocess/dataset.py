from functools import partial
import xarray as xr
import numpy as np
import pandas as pd
from datetime import timedelta
from pyteseo.preprocess.teseo_standarizations import interp_to_oclock_hours


def get_dataset(
    urls,
    variables: list = None,
    bbox: tuple = None,
    timebox: tuple = None,
    coord_t: str = None,
    coord_x: str = None,
    coord_y: str = None,
    interp_oclock: bool = None,
) -> xr.Dataset:
    if isinstance(urls, list) and len(urls) > 1:
        partial_func = partial(
            dataset_preprocess_pipeline,
            variables=variables,
            bbox=bbox,
            timebox=timebox,
            coord_t=coord_t,
            coord_x=coord_x,
            coord_y=coord_y,
            interp_oclock=interp_oclock,
        )
        ds = (
            xr.open_mfdataset(
                urls,
                combine="nested",
                concat_dim="time",
                parallel=True,
                preprocess=partial_func,
                chunks="auto",
            )
            .drop_duplicates(coord_t)
            .sortby(coord_t)
        )
    else:
        urls = urls[0] if isinstance(urls, list) else urls
        ds = xr.open_dataset(
            urls,
            chunks="auto",
        )
        ds = dataset_preprocess_pipeline(
            ds, variables, bbox, timebox, coord_t, coord_x, coord_y
        )

    return ds


def dataset_preprocess_pipeline(
    ds: xr.Dataset,
    variables: list = None,
    bbox: tuple = None,
    timebox: tuple = None,
    coord_t: str = None,
    coord_x: str = None,
    coord_y: str = None,
):
    ds = ds.squeeze(drop=True)

    if bbox and coord_x is None:
        raise ValueError("If bbox subset, coord_x and coord_y have to be mapped")

    if timebox and coord_t is None:
        raise ValueError("If timebox subset, coord_t has to be mapped")

    if variables:
        ds = ds[variables]

    if coord_x:
        if ds[coord_x].max() > 180:
            print("(*) - Rolling longitudes from (0,360) to (-180,180)")
            # Ensure x_coord: -180 to 180
            ds = ds.assign_coords(
                {coord_x: (((ds[coord_x].values + 180) % 360) - 180)}
            ).sortby(coord_x)
        elif ds[coord_x][0] > ds[coord_x][-1]:
            print("(*) - Sorting longitudes to (-180,180)...")
            ds = ds.sortby(coord_x)

    if coord_y:
        if ds[coord_y][0] > ds[coord_y][-1]:
            print("(*) - Sorting latitudes to (-90,90)...")
            ds = ds.sortby(coord_y)

    if bbox:
        print("Processing spatial subset...")
        ds = _spatial_subset_2d(ds, bbox, coord_x, coord_y)
        print(f"\tuser_bbox:\t{bbox}")
        print(
            (
                f"\tbbox:\t\t{float(ds[coord_x].min()), float(ds[coord_y].min()), float(ds[coord_x].max()), float(ds[coord_y].max())}"
            )
        )

    if timebox:
        print("Preprocessing temporal subset...")
        if all(ds.time.dt.minute != 0):
            print(
                "(*) - Interpolating times to hourly data to pass throgh 00:00 (min:seconds)..."
            )
            ds = _temporal_subset(ds, timebox, coord_t, extra_buffer=True)
            ds = interp_to_oclock_hours(ds)
        ds = _temporal_subset(ds, timebox, coord_t)
        print(f"\tuser_timebox:\t{timebox[0].isoformat(), timebox[1].isoformat()}")
        print(
            f"\ttimebox:\t{pd.Timestamp(ds[coord_t].min().values).to_pydatetime().isoformat(), pd.Timestamp(ds[coord_t].max().values).to_pydatetime().isoformat()}"
        )

    if isinstance(ds, xr.DataArray):
        ds = ds.to_dataset()

    return ds


def _get_dataset_time_resolution(ds: xr.Dataset) -> int:
    time_values = ds.time.values
    time_diff = np.diff(time_values)
    time_resolution = np.mean(time_diff)

    return time_resolution / np.timedelta64(1, "h")


def _spatial_subset_2d(
    ds: xr.Dataset,
    bbox: tuple,
    coord_x: str,
    coord_y: str,
    extra_buffer: bool = False,
) -> xr.Dataset:
    """subset spatially (lon,lat).

    Args:
        ds (xr.Dataset): input dataset.
        bbox (tuple[float, float, float, float]): lon_min, lat_min, lon_max, lat_max coordinates.
        extra_buffer (bool, optional): extends selection to two next outside coordinate points. Defaults to False.

    Returns:
        xr.Dataset: subset dataset
    """
    if extra_buffer:
        dx = max(np.unique(ds[coord_x].diff(coord_x).values))
        dy = max(np.unique(ds[coord_y].diff(coord_y).values))
        buffer_value = max([dx, dy])

        x_ini = ds.sel({coord_x: bbox[0] - buffer_value}, method="ffill")[
            coord_x
        ].values
        y_ini = ds.sel({coord_y: bbox[1] - buffer_value}, method="ffill")[
            coord_y
        ].values
        x_end = ds.sel({coord_x: bbox[2] + buffer_value}, method="bfill")[
            coord_x
        ].values
        y_end = ds.sel({coord_y: bbox[3] + buffer_value}, method="bfill")[
            coord_y
        ].values

    else:
        x_ini = ds.sel({coord_x: bbox[0]}, method="ffill")[coord_x].values
        y_ini = ds.sel({coord_y: bbox[1]}, method="ffill")[coord_y].values
        x_end = ds.sel({coord_x: bbox[2]}, method="bfill")[coord_x].values
        y_end = ds.sel({coord_y: bbox[3]}, method="bfill")[coord_y].values

    ds = ds.sel({coord_x: slice(x_ini, x_end), coord_y: slice(y_ini, y_end)})
    return ds

    # if buffer:
    #     dx = max(np.unique(ds[coord_x].diff(coord_x).values))
    #     dy = max(np.unique(ds[coord_y].diff(coord_y).values))
    #     buffer_value = max([dx, dy])

    #     ds = ds.sel(
    #         {
    #             coord_x: slice(bbox[0] - buffer_value, bbox[2] + buffer_value),
    #             coord_y: slice(bbox[1] - buffer_value, bbox[3] + buffer_value),
    #         }
    #     )
    # else:
    #     ds = ds.sel(
    #         lon=slice(bbox[0], bbox[2]),
    #         lat=slice(bbox[1], bbox[3]),
    #     )

    # return ds


def _temporal_subset(
    ds: xr.Dataset,
    timebox: tuple,
    coord_t: str,
    extra_buffer: bool = False,
) -> xr.Dataset:
    """subset temporally.

    Args:
        ds (xr.Dataset): input dataset.
        time_box (tuple[datetime, datetime]): initial_datetime, end_datetime.
        buffer (timedelta): time to extend selection to the two next outside time-points. Defaults to False.

    Returns:
        xr.Dataset: subset dataset
    """
    # CHECK THIS
    dt_h = _get_dataset_time_resolution(ds)
    buffer_dt = timedelta(hours=dt_h)
    # CHECK THIS
    if extra_buffer:
        t_ini = ds.sel({coord_t: timebox[0] - buffer_dt}, method="ffill")[
            coord_t
        ].values
        t_end = ds.sel({coord_t: timebox[1] + buffer_dt}, method="bfill")[
            coord_t
        ].values
    else:
        t_ini = ds.sel({coord_t: timebox[0]}, method="ffill")[coord_t].values
        t_end = ds.sel({coord_t: timebox[1]}, method="bfill")[coord_t].values

    ds = ds.sel({coord_t: slice(t_ini, t_end)})
    return ds
