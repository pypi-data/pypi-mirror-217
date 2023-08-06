# from datetime import datetime, timedelta

# import numpy as np
# import pytest
# import xarray as xr

# from pyteseo.providers.ihcantabria import get_ihcantabria_opendap_urls
# from pyteseo.providers.opendap import dataset_preprocess_pipeline


# bbox = (1.05, 38.55, 1.7, 39.2)
# now = datetime.utcnow().replace(hour=11, minute=0, second=0, microsecond=0)
# timebox = (now, now + timedelta(hours=12))


# @pytest.fixture()
# def input_ds():
#     urls = get_ihcantabria_opendap_urls("cmems_ibi_hourly")
#     if isinstance(urls, str):
#         return xr.open_dataset(urls, chunks="auto")
#     else:
#         return (
#             xr.open_mfdataset(
#                 urls, combine="nested", concat_dim="time", parallel=True, chunks="auto"
#             )
#             .drop_duplicates("time")
#             .sortby("time")
#         )


# @pytest.mark.parametrize(
#     "variables, bbox, timebox, t_coord, x_coord, y_coord",
#     [
#         (["uo", "vo"], None, None, None, None, None),
#         (None, bbox, None, None, "longitude", "latitude"),
#         (None, None, timebox, "time", None, None),
#     ],
# )
# def test_dataset_preprocess_pipeline(
#     input_ds, variables, bbox, timebox, t_coord, x_coord, y_coord
# ):

#     ds = dataset_preprocess_pipeline(
#         input_ds, variables, bbox, timebox, t_coord, x_coord, y_coord
#     )
#     if bbox:
#         assert ds.longitude.min().values < bbox[0]
#         assert ds.latitude.min().values < bbox[1]
#         assert ds.longitude.max().values > bbox[2]
#         assert ds.latitude.max().values > bbox[3]

#     if timebox:
#         assert ds.time.min() < np.datetime64(timebox[0])
#         assert ds.time.max() > np.datetime64(timebox[1])

#     if variables:
#         assert all(
#             [
#                 variable in ds.variables
#                 for variable in variables
#                 if variable in ds.variables
#             ]
#         )
