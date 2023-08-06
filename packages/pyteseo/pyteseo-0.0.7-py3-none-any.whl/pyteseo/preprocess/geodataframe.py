import geopandas as gpd
from owslib.wfs import WebFeatureService


# WFS SERVICE
def get_geodataframe(
    wfs_url,
    wfs_version: str,
    feature_name: str,
    bbox: tuple = None,
    n_max_pol: int = 9,
) -> gpd.GeoDataFrame:
    """Create connection to WFS service of a Geoserver and request a feature.
    Optionally, a bbox can be passed to select features inside and instersected by the box.
    Args:
        wfs_url (str): Url of the WFS service.
        wfs_version (str): version of the WFS service.
        feature_name (str): Name of the feature requested.
        bbox (tuple, optional): boundary box (Xmin, Ymin, Xmax, Ymax). Defaults to None.
        n_max_pol (int): maximum number of polygons desired. Defaults to None.
    Raises:
        FeatureNameError: Custom error for invalid feature names.
    Returns:
        gpd.GeoDataFrame: Geopandas DataFrame in WGS84 (4326)
    """

    wfs = WebFeatureService(url=wfs_url, version=wfs_version)
    response = wfs.getfeature(typename=feature_name, bbox=bbox, outputFormat="json")
    gdf = gpd.read_file(response)
    gdf = gdf = gdf.explode(ignore_index=True)

    if gdf.crs.to_epsg() != 4326:
        gdf = gdf.to_crs(epsg=4326)
    if bbox:
        gdf = _clip_gdf(gdf, bbox)
    if n_max_pol:
        gdf = _get_n_polygons(gdf, n_max_pol)
    return gdf


def _get_n_polygons(gdf, n_max_pol=None):
    # project to cartesian to sort areas and filter small polygons then transform back to ellipsoidal
    if len(gdf) > n_max_pol:
        gdf = gdf.to_crs(3857)
        indexes = gdf.area.sort_values()[-n_max_pol:].index
        gdf = gdf[indexes].reset_index(drop=True)
        gdf = gdf.to_crs(4326)
    return gdf


def _clip_gdf(gdf, bbox):
    gdf = gdf.clip_by_rect(*bbox)
    if any(gdf[gdf.geometry.type == "MultiPolygon"]):
        gdf = gdf.explode(ignore_index=True)
    return gdf
