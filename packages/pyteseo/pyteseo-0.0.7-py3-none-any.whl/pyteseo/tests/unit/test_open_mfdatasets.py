# from matplotlib import pyplot as plt
# import xarray as xr


# # PILE NETCDFS WITH TIME OVERLAPINGS AND DIFFERENT REFERENCE TIMES
# def test_merge():
#     paths = ["Global_2023061518.nc", "Global_2023061506.nc"]
#     ds1 = xr.open_dataset(paths[0])
#     ds2 = xr.open_dataset(paths[1])
#     ds = (
#         xr.open_mfdataset(paths, combine="nested", concat_dim="time")
#         .drop_duplicates(dim="time")
#         .sortby("time")
#     )

#     (figure, ((ax0, ax1, ax2, ax3), (ax4, ax5, ax6, ax7))) = plt.subplots(2, 4)

#     ds1["u-component_of_wind_height_above_ground"].isel(time=0).plot(ax=ax0)
#     ds2["u-component_of_wind_height_above_ground"].sel(time=ds1.time[0]).plot(ax=ax1)
#     ds["u-component_of_wind_height_above_ground"].sel(time=ds1.time[0]).plot(ax=ax2)
#     (
#         ds1["u-component_of_wind_height_above_ground"].isel(time=0)
#         - ds["u-component_of_wind_height_above_ground"].sel(time=ds1.time[0])
#     ).plot(ax=ax3)

#     ds1["u-component_of_wind_height_above_ground"].isel(time=24).plot(ax=ax4)
#     ds2["u-component_of_wind_height_above_ground"].sel(time=ds1.time[24]).plot(ax=ax5)
#     ds["u-component_of_wind_height_above_ground"].sel(time=ds1.time[24]).plot(ax=ax6)
#     (
#         ds1["u-component_of_wind_height_above_ground"].isel(time=24)
#         - ds["u-component_of_wind_height_above_ground"].sel(time=ds1.time[24])
#     ).plot(ax=ax7)

#     # plt.show()

#     assert len(ds1.time) == len(ds2.time)
#     assert len(ds1.time) + len(ds2.time) > len(ds.time)
#     assert ds1.time[-1] != ds2.time[-1]
#     assert ds.time[0] == ds2.time[0]
#     assert ds.time[-1] == ds1.time[-1]
