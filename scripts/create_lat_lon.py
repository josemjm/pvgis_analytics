# -*- coding: utf-8 -*-
# Author: José María Jiménez Manzano

# importing libraries
import pandas as pd
import geopandas
import json


def create_lon_lat_df(xmin: float, ymin: float, xmax: float, ymax: float) -> pd.DataFrame:
    """
    Function to create a grid of points according to max/min lat/lon
    :param xmin: Minimum longitude
    :param ymin: Minimum latitude
    :param xmax: Maximum longitude
    :param ymax: Maximum latitude
    :return: DataFrame composed by all points of the grid
    """

    # Create an empty DataFrame and populate
    df = pd.DataFrame(columns=['lat', 'lon'])

    xmin_100 = int(round(xmin * 100))
    ymin_100 = int(round(ymin * 100))
    xmax_100 = int(round(xmax * 100))
    ymax_100 = int(round(ymax * 100))

    for lat in range(ymin_100, ymax_100, 5):
        for lon in range(xmin_100, xmax_100, 5):
            df = df.append({"lat": lat / 100, "lon": lon / 100}, ignore_index=True)

    return df


def create_json_coords(xmin: float, ymin: float, xmax: float, ymax: float, tool_name: str) -> json:
    """
    Function to create a JSON object with PVGIS tool name, latitude and longitude according to max/min lat/lon
    :param xmin: Minimum longitude
    :param ymin: Minimum latitude
    :param xmax: Maximum longitude
    :param ymax: Maximum latitude
    :param tool_name: Name of PVGIS tool
    :return: JSON object
    """

    # Create a dataframe with lon and lat
    df = create_lon_lat_df(xmin, ymin, xmax, ymax)

    # Add the PVGIS tool name
    df['tool_name'] = tool_name

    # Parsed dataframe as JSON object
    result = df[['tool_name', 'lat', 'lon']].to_json(orient="records")
    parsed_json = json.loads(result)

    return parsed_json


def create_gdf(xmin: float, ymin: float, xmax: float, ymax: float, srid: int) -> geopandas.GeoDataFrame:
    """
    Function to create a GeoDataFrame according to max/min lat/lon and SRID
    :param xmin: Minimum longitude
    :param ymin: Minimum latitude
    :param xmax: Maximum longitude
    :param ymax: Maximum latitude
    :param srid: Spatial Reference System Identifier
    :return: GeoDataFrame composed by all points of the grid
    """

    # Create a dataframe with lon and lat
    df = create_lon_lat_df(xmin, ymin, xmax, ymax)

    # Create a GeoDataFrame with shapely.Point object as geometry
    gdf = geopandas.GeoDataFrame(df, geometry=geopandas.points_from_xy(df.lon, df.lat))

    # Set a projection according to EPSG integer code
    gdf = gdf.set_crs(epsg=srid)

    return gdf
