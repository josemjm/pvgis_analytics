# -*- coding: utf-8 -*-
# Author: José María Jiménez Manzano

from clickhouse_driver import Client
import pandas as pd


def anual_monthly_series_gi(year: int, client: Client) -> pd.DataFrame():
    """
    Function to create a daraframe of Anual Monthly Series Global Irradiance (KWh/m2)
    :param year: Year
    :param client: Client for Clickhouse driver
    :return: DataFrame
    """

    query = f"WITH sub AS ( " \
            f"  SELECT " \
            f"      latitude, " \
            f"      longitude, " \
            f"      toYear(time) AS year, " \
            f"      toMonth(time) AS month, " \
            f"      ROUND(SUM(global_irradiance / 1000) , 2) AS global_irradiance " \
            f"  FROM seriescalc WHERE toYear(time) = {year} " \
            f"  GROUP BY latitude, longitude, toYear(time), toMonth(time) " \
            f"  ORDER BY toMonth(time)" \
            f") " \
            f"  SELECT year, month, AVG(global_irradiance) AS global_irradiance " \
            f"  FROM sub " \
            f"  GROUP BY year, month" \
            f"  ORDER BY month; "

    df = client.query_dataframe(query)

    return df
