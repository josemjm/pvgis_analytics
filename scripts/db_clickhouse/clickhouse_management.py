# -*- coding: utf-8 -*-
# Author: José María Jiménez Manzano

## https://clickhouse.com/docs/en/getting-started/tutorial/
## https://pypi.org/project/clickhouse-driver/

from clickhouse_driver import Client
from datetime import datetime
import json


def conn_clickhouse() -> Client:
    """
    Function to create a Client, Database and Table
    :return: Client for Clickhouse executions
    """
    client = Client('localhost')

    client.execute('CREATE DATABASE IF NOT EXISTS pvgis')

    c = client.execute('SHOW DATABASES')

    if len([x for x in c if x[0] == 'pvgis']) > 0:
        client.execute('use pvgis')

        t = client.execute('SHOW TABLES')
        if len([x for x in t if x[0] == 'seriescalc']) == 0:
            client.execute("CREATE table IF NOT EXISTS seriescalc ( "
                           "    latitude Float64, "
                           "    longitude Float64, "
                           "    time DateTime('Europe/Moscow'), "
                           "    global_irradiance Float64, "
                           "    sun_height Float64, "
                           "    air_temperature_2m Float64, "
                           "    total_wind_speed_10m Float64, "
                           "    solar_radiation_value_reconstructed Boolean ) "
                           "ENGINE = MergeTree() ORDER BY (latitude, longitude, time); "
                           )
            print("'seriescalc TABLE CREATED.")

    return client


def generator_rows(data: json):
    """
    Generator to iterate over JSON outputs
    :param data: JSON object
    :return: Iterator object
    """
    latitude = data['inputs']['location']['latitude']
    longitude = data['inputs']['location']['longitude']

    for output in data['outputs']['hourly']:
        yield {
            'latitude': latitude,
            'longitude': longitude,
            'time': int(datetime.timestamp(datetime.strptime(output['time'], '%Y%m%d:%H%M'))),
            'global_irradiance': output['G(i)'],
            'sun_height': output['H_sun'],
            'air_temperature_2m': output['T2m'],
            'total_wind_speed_10m': output['WS10m'],
            'solar_radiation_value_reconstructed': int(output['Int']),
        }

# client.execute("INSERT INTO seriescalc VALUES", (row for row in generator_rows(data)))
