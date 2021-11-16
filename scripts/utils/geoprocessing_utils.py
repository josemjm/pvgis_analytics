# -*- coding: utf-8 -*-
# Author: José María Jiménez Manzano

# importing libraries
import geopandas
from shapely.geometry import box


def square_grid(gdf: geopandas.GeoDataFrame, side: float) -> geopandas.GeoDataFrame:
    """
    Function to create a square grid from GeoDataFrame of Points
    :param gdf: input GeoDataFrame
    :param side: side of resultant square
    :return: output GeoDataFrame
    """

    buffer_gdf = gdf.copy()
    buffer_gdf['geometry'] = buffer_gdf.apply(lambda row: box(
        row['geometry'].x - side / 2,  # left
        row['geometry'].y - side / 2,  # bottom
        row['geometry'].x + side / 2,  # right
        row['geometry'].y + side / 2  # top
    ), axis=1)

    return buffer_gdf

