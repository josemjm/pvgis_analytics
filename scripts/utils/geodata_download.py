# -*- coding: utf-8 -*-
# Author: José María Jiménez Manzano

import os
import glob
import requests
import geopandas

from datetime import date
from zipfile import ZipFile


def create_gisco_gdf(year: int, srid: int, scale: str, nut_level: int, nut_id: str):
    """
    Function to create a GeoDataFrame from GISCO API: 'https://gisco-services.ec.europa.eu/distribution/v2/'
    :param year: Dataset generation year
    :param srid: Spatial Reference System Identifier
    :param scale: 1:x Scale
    :param nut_level: NUT level code
    :param nut_id: NUT identifier
    :return: GeoDataFrame
    """
    url = 'https://gisco-services.ec.europa.eu/distribution/v2/nuts/nuts-2021-units.json'
    nut_ids = list(requests.get(url).json().keys())

    gdf = geopandas.GeoDataFrame()
    urls = []

    if year not in [2021, 2016, 2013, 2010, 2006, 2003]:
        print('Insert a valid Year: [2021, 2016, 2013, 2010, 2006, 2003]')

    elif srid not in [3035, 3857, 4326]:
        print('Insert a valid NUT Level: [3035, 3857, 4326]')

    elif scale not in ['01m', '03m', '10m', '20m', '60m']:
        print("Insert a valid Scale: ['01m', '03m', '10m', '20m', '60m']")

    elif nut_level not in [0, 1, 2, 3]:
        print('Insert a valid NUT Level: [0, 1, 2, 3]')

    elif nut_id not in nut_ids:
        print("Insert a valid ID.")
        print("Visit website for more information:")
        print("https://ec.europa.eu/eurostat/web/nuts/background")

    else:
        if nut_level == 0:
            if len(nut_id) == 2:
                urls.append(
                    f"https://gisco-services.ec.europa.eu/distribution/v2/nuts/distribution/{nut_id}-region-{scale}-{srid}-{year}.geojson")
            else:
                print("You have to insert a valid NUT ID according to NUT LEVEL")
        elif nut_level == 1:
            if len(nut_id) == 2:
                nut_ids_level1 = [x for x in nut_ids if nut_id in x and len(x) == 3]
                for nut_id_level1 in nut_ids_level1:
                    urls.append(
                        f"https://gisco-services.ec.europa.eu/distribution/v2/nuts/distribution/{nut_id_level1}-region-{scale}-{srid}-{year}.geojson")
            elif len(nut_id) == 3:
                urls.append(
                    f"https://gisco-services.ec.europa.eu/distribution/v2/nuts/distribution/{nut_id}-region-{scale}-{srid}-{year}.geojson")
            else:
                print("You have to insert a valid NUT ID according to NUT LEVEL")
        elif nut_level == 2:
            if len(nut_id) == 3 or len(nut_id) == 2:
                nut_ids_level1 = [x for x in nut_ids if nut_id in x and len(x) == 4]
                for nut_id_level1 in nut_ids_level1:
                    urls.append(
                        f"https://gisco-services.ec.europa.eu/distribution/v2/nuts/distribution/{nut_id_level1}-region-{scale}-{srid}-{year}.geojson")
            elif len(nut_id) == 4:
                urls.append(
                    f"https://gisco-services.ec.europa.eu/distribution/v2/nuts/distribution/{nut_id}-region-{scale}-{srid}-{year}.geojson")
            else:
                print("You have to insert a valid NUT ID according to NUT LEVEL")
        elif nut_level == 3:
            if len(nut_id) == 4 or len(nut_id) == 3 or len(nut_id) == 2:
                nut_ids_level1 = [x for x in nut_ids if nut_id in x and len(x) == 5]
                for nut_id_level1 in nut_ids_level1:
                    urls.append(
                        f"https://gisco-services.ec.europa.eu/distribution/v2/nuts/distribution/{nut_id_level1}-region-{scale}-{srid}-{year}.geojson")
            elif len(nut_id) == 5:
                urls.append(
                    f"https://gisco-services.ec.europa.eu/distribution/v2/nuts/distribution/{nut_id}-region-{scale}-{srid}-{year}.geojson")
            else:
                print("You have to insert a valid NUT ID according to NUT LEVEL")

    if len(urls) > 0:
        for url in urls:
            gdf = gdf.append(geopandas.read_file(url))

    return gdf


def download_ine_secc(directory: str, filename: str):
    """
    Function to download the last INE Cartography of the Censal Sections and Electoral Census Street Map
    :param directory: Foldername of download directory
    :param filename: Filename of download file
    :return: Path of download file
    """

    url = 'https://www.ine.es/prodyser/cartografia/'
    year = date.today().year

    r = requests.get(f'{url}seccionado_{year}.zip')

    downloaded_file = f"{directory}/{filename}"

    # open method to open a file on your system and write the contents
    with open(downloaded_file, "wb") as code:
        code.write(r.content)

    return downloaded_file


def read_zipped_shapefile(download_file: str):
    """
    Function to download the last INE Cartography of the Censal Sections and Electoral Census Street Map
    :param download_file: Path of download file
    :return: GeoDataFrame
    """

    # Create a ZipFile Object and load sample.zip in it
    with ZipFile(download_file, 'r') as zipObj:
        # Extract all the contents of zip file in different directory
        zipObj.extractall('temp')

    # Open shapefile with GeoPandas
    ine_seccionado_gdf = geopandas.read_file(glob.glob('**/*.shp', recursive=True)[0])

    # Remove temp directory
    import shutil
    if os.path.isdir('temp'):
        shutil.rmtree('temp', ignore_errors=True)

    return ine_seccionado_gdf
