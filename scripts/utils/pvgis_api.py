# -*- coding: utf-8 -*-
# Author: José María Jiménez Manzano

"""
Util to get the Photovoltaic Geographical Information System (PVGIS) API using Python Requests

HTTP methods allowed

    API functions accept GET method only. Other methods will return an HTTP status "405 - Method not allowed". HEAD
    method has been kept only to confirm the existence of the desired API function, but will return a "204 - No Content"
    HTTP status to avoid wasting CPU computation time.

API calls rate limit

    API calls have a rate limit of 30 calls/second per IP address. If you exceed this threshold, the service will refuse
    your call and return a "429 - Too Many Requests" HTTP status.

Simultaneous computations tasks limit

    To avoid server slowdowns due to too many simultaneous computations tasks, we introduced a new mechanism to handle
    excessive requests that affect the service availability.

    All the exceeding computation requests that are outside the optimal computation frame, will be suspended for 150/200
    miliseconds before a new try, waiting for just released resource. The number of tries are limited to a cap of 4/5
    seconds, and after that limit the service will return a "529 - Site is overloaded" HTTP status code.

    This status code is used to tell you that you should repeat the request after a while.


For more information visit: "https://ec.europa.eu/jrc/en/PVGIS/docs/noninteractive"
"""

import requests


def pvgis_tool(tool_name: str, **kwargs):
    """
    Function to get the PVGIS APIs
    :param tool_name: str
    :param kwargs: a valid param for each tool
    :return: json
    """

    tool_names =['PVcalc','SHScalc','MRcalc','DRcalc','seriescalc','tmy','printhorizon']

    if tool_name in tool_names:
        url = 'https://re.jrc.ec.europa.eu/api/' + tool_name

        params = kwargs
        params['outputformat'] = 'json'

        r = requests.get(url, params=kwargs, allow_redirects=True)

        if r.status_code != 200:
            print("An error has occurred:", r.text)

            if r.status_code == 400:
                print('To see the valid inputs visit: "https://ec.europa.eu/jrc/en/PVGIS/docs/noninteractive"')
        else:
            return r.json()

    else:
        print("Please insert a valid PVGIS Tool:", tool_names)
