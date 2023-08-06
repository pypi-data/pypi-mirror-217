from pathlib import Path
from uuid import uuid4
from shutil import make_archive, rmtree

import geopandas as gpd
import pandas as pd
from shapely.geometry import Polygon

from pyteseo.defaults import FILE_NAMES, COORDINATE_NAMES
from pyteseo.io.coastline import write_coastline
from pyteseo.io.grid import write_grid, read_grid
from pyteseo.classes import _calculate_cell_properties
from pyteseo.plot.figures import plot_domain
from pyteseo.preprocess.geodataframe import _clip_gdf, _get_n_polygons
from pyteseo.providers.connection import (
    preprocess_online_provider,
    get_provider_dataset,
    get_variable_map,
)
from pyteseo.preprocess.teseo_standarizations import standarize_dataset_varnames
from pyteseo.io.coastline import read_coastline


__all__ = ["load_coastline_from_shapefile", "create_domain"]


def create_domain(
    name,
    elevation_source,
    coastline_source,
    bbox,
    output_dir,
    compress_output: bool = False,
    elevation_variable_map: dict = None,
    elevation_type: str = None,
):
    print("\n")
    print(
        "\n------------------------------ PREPROCESSING TESEO DOMAIN ------------------------------"
    )
    print(
        "------------------------------------------------------------------------------------------\n"
    )
    domain_dir = Path(output_dir, name + "_" + str(uuid4())[-12:])
    domain_dir.mkdir()
    print(
        f"PREPROCESSING ELEVATION [{elevation_source['dataset_name']}] FROM [{elevation_source['online_provider']}]"
    )
    if "online_provider" in elevation_source.keys():
        elevation_variable_map = (
            get_variable_map(
                elevation_source["online_provider"],
                elevation_source["service"],
                elevation_source["dataset_name"],
            )
            if not elevation_variable_map
            else elevation_variable_map
        )
        connection_params = preprocess_online_provider(
            elevation_source["online_provider"],
            elevation_source["service"],
            elevation_source["dataset_name"],
        )

    elif "local_path" in elevation_source.keys():
        if not elevation_variable_map or not elevation_type:
            raise ValueError(
                "Bad definition. 'elevation_type' ('topobathymetry' or 'bathymetry') and 'elevation_variable_map' ({'x': 'lon', 'y': 'lat', 'elevation': 'ground_level'}) have to be defined."
            )
        connection_params = elevation_source["local_path"]

    coord_x = elevation_variable_map["x"]
    coord_y = elevation_variable_map["y"]

    ds = get_provider_dataset(
        connection_params,
        bbox=bbox,
        coord_x=coord_x,
        coord_y=coord_y,
    )
    print("\tWritting TESEO grid-file...")
    _elevation_ds_to_teseo_grid(
        ds,
        domain_dir,
        elevation_type="topobathymetry",
        variable_map=elevation_variable_map,
    )
    print("done!\n")
    new_bbox = (
        float(ds[coord_x].min().values),
        float(ds[coord_y].min().values),
        float(ds[coord_x].max().values),
        float(ds[coord_y].max().values),
    )
    source = (
        coastline_source["online_provider"]
        if "online_provider" in coastline_source
        else coastline_source["file_format"]
    )
    dataset = (
        coastline_source["dataset_name"]
        if "dataset_name" in coastline_source
        else Path(coastline_source["local_path"]).name
    )
    print(f"PREPROCESSING COASTLINE [{dataset}] FROM [{source}]")
    if "online_provider" in coastline_source.keys():
        connection_params = preprocess_online_provider(
            coastline_source["online_provider"],
            coastline_source["service"],
            coastline_source["dataset_name"],
        )
        gdf = get_provider_dataset(connection_params, bbox=new_bbox)
        df = _coastline_gdf_to_coastline_df(gdf)

    elif "local_path" in coastline_source.keys():
        if coastline_source["file_format"] == "shp":
            gdf = load_coastline_from_shapefile(
                coastline_source["local_path"], bbox=new_bbox
            )
            df = _coastline_gdf_to_coastline_df(gdf)

        elif coastline_source["file_format"] == "teseo-txt":
            df = read_coastline(coastline_source["local_path"])
        else:
            raise ValueError(f"Bad file format ({coastline_source['file_format']})")
    print("\tWritting TESEO coastline-file(s)...")
    write_coastline(df, Path(domain_dir, FILE_NAMES["coastline"]))
    print("done!\n")

    cell_properties = _get_grid_cell_properties(domain_dir)

    print("\tPlotting domain figure...")
    fig = plot_domain(
        Path(domain_dir, FILE_NAMES["grid"]),
        Path(domain_dir, FILE_NAMES["coastline"]),
        land_mask=False,
        show=False,
    )
    fig.savefig(domain_dir / f"{name}_domain.png", dpi=600, format="png")
    domain_path = domain_dir

    if compress_output:
        print("\tPacking in zip file...")
        make_archive(domain_dir, "zip", domain_dir)
        rmtree(domain_dir)

        domain_path = domain_dir.with_suffix(".zip")

    return domain_path, new_bbox, cell_properties


def _get_grid_cell_properties(domain_dir):
    df = read_grid(Path(domain_dir, FILE_NAMES["grid"]))
    dx, nx = _calculate_cell_properties(df, COORDINATE_NAMES["x"])
    dy, ny = _calculate_cell_properties(df, COORDINATE_NAMES["y"])
    return dx, dy, nx, ny


def load_coastline_from_shapefile(
    shp_path: str, bbox: tuple = None, in_epsg: int = None, n_max_pol: int = 9
) -> gpd.GeoDataFrame:
    """Load geometry from esri shapefile.

    Args:
        shp_path (str): path to file.
        bbox (tuple, optional): boundary box for clipping if needed. Defaults to None.
        in_epsg (int, optional): to force epsg code of the input if no referece defined. Defaults to None.

    Returns:
        gpd.GeoDataFrame: geometry exploded in geodataframe
    """
    gdf = gpd.read_file(shp_path)
    gdf = gdf["geometry"]
    gdf = gdf.explode(ignore_index=True)

    if gdf.crs.to_epsg() != 4326:
        gdf = gdf.to_crs(4326)
    if in_epsg:
        gdf.set_crs(f"epsg:{in_epsg}")
    if bbox:
        gdf = _clip_gdf(gdf, bbox)
    if n_max_pol:
        gdf = _get_n_polygons(gdf, n_max_pol)

    return gdf


def _elevation_ds_to_teseo_grid(ds, output_dir, elevation_type, variable_map):
    ds = standarize_dataset_varnames(ds, elevation_type, variable_map)
    if elevation_type == "topobathymetry":
        ds["depth"] = ds["elevation"] * -1
    ds["depth"] = ds["depth"].where(ds["depth"] >= 0, drop=False)
    df = ds[["lon", "lat", "depth"]].to_dataframe().reset_index()
    path = Path(output_dir, FILE_NAMES["grid"])
    write_grid(df, path)


def _coastline_gdf_to_teseo_coastline(gdf: gpd.GeoDataFrame, output_dir: str):
    df = _coastline_gdf_to_coastline_df(gdf)
    write_coastline(df, Path(output_dir, FILE_NAMES["coastline"]))


def _coastline_df_to_gdf(df: pd.DataFrame, epsg: str = "4326") -> gpd.GeoDataFrame:
    """convert coastline dataframe[lon,lat,polygon] to geodataframe

    Args:
        df (pd.DataFrame): Dataframe with columns [lon, lat, polygon]
        epsg (str, optional): epsg coordinate code. Defaults to "4326" (WGS84).

    Returns:
        gpd.GeoDataFrame: closed polygons of the coastline
    """

    geometry = [
        Polygon(list(zip(df_["lon"], df_["lat"]))) for _, df_ in df.groupby("polygon")
    ]
    gdf = gpd.GeoDataFrame({"geometry": geometry})
    gdf = gdf.set_crs(epsg)

    return gdf


def _coastline_gdf_to_coastline_df(gdf) -> pd.DataFrame:
    """Convert costaline GeoDataFrame[geometry] to coastline DataFrame [lon, lat, polygon]
    Returns:
        pd.DataFrame: coastlines polygons [polygon, lon, lat]
    """
    multipoints = gdf.geometry.apply(lambda x: list(x.exterior.coords))

    df = pd.DataFrame(
        {
            "polygon": gdf.index.repeat(multipoints.apply(len)),
            "lon": [p[0] for points in multipoints for p in points],
            "lat": [p[1] for points in multipoints for p in points],
        }
    )

    return df.reset_index(drop=True)
