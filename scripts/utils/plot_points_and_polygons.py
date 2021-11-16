# -*- coding: utf-8 -*-
# Author: José María Jiménez Manzano

import geopandas
from matplotlib import pyplot as plt


def plot_points_and_countries(points_gdf: geopandas.GeoDataFrame):
    """
    Function to plot points on its Censal Sections INE
    :param points_gdf: GeoDataFrame of points
    :return: Open matplotlib
    """

    world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))

    gdf_iso_a3 = points_gdf.sjoin(world[['geometry', 'iso_a3']], how="left")

    iso_a3s = list(gdf_iso_a3['iso_a3'].unique())

    # We restrict to Spain.
    ### !! BETTER MAKE INTERSECT TO GET THE CODES
    ax = world[world['iso_a3'].isin(iso_a3s)].plot(color='white', edgecolor='black')

    # We can now plot our ``GeoDataFrame``.
    points_gdf.plot(ax=ax, color='red')

    plt.show()

    return


def plot_points_and_ine_municipalities(points_gdf: geopandas.GeoDataFrame, ine_seccionado_gdf: geopandas.GeoDataFrame):
    """
    Function to plot points on its Censal Sections INE
    :param points_gdf: GeoDataFrame of points
    :param ine_seccionado_gdf: GeoDataFrame of polygons
    :return: Open matplotlib
    """

    if ine_seccionado_gdf.crs.to_epsg() != points_gdf.crs.to_epsg():
        ine_seccionado_gdf = ine_seccionado_gdf.to_crs(points_gdf.crs.to_epsg())

    gdf_cumun = points_gdf.sjoin(ine_seccionado_gdf[['geometry', 'CUMUN']], how="left")

    cumuns = list(gdf_cumun['CUMUN'].unique())

    # We restrict to Spain.
    ### !! BETTER MAKE INTERSECT TO GET THE CODES
    ax = ine_seccionado_gdf[ine_seccionado_gdf['CUMUN'].isin(cumuns)].plot(color='white', edgecolor='black')

    # We can now plot our ``GeoDataFrame``.
    points_gdf.plot(ax=ax, color='red')

    plt.show()

    return

