# -*- coding: utf-8 -*-
# Author: José María Jiménez Manzano

'''
Hourly radiation

In this tool you can get the full data set of solar radiation and other data needed to calculate PV power hour by
hour for long time periods. PVGIS can also perform the hourly PV power calculation. The PV output values from the
PVGIS interface "Hourly data" tool are calculated for a free-standing PV system. The hourly values of PV output from
a building integrated system can be obtained using the Non-interactive service of the said "Hourly data" tool.

Outputs:
This option makes it possible to receive solar irradiance and PV output data for every hour in a multi-year period.
'''

import os
import json
import requests

directory = 'data_out'
if not os.path.exists(directory):
    os.makedirs(directory)

lat = 45
lon = 8
slope = None
aspect = None
pvcalculation = None
startyear = None
endyear = None
components = None

params = {}
url = 'https://re.jrc.ec.europa.eu/api/seriescalc'

if lat is not None:
    params['lat'] = lat

if lon is not None:
    params['lon'] = lon

if slope is not None:
    params['slope'] = slope

if aspect is not None:
    params['aspect'] = aspect

if pvcalculation is not None:
    params['pvcalculation'] = pvcalculation

if startyear is not None:
    params['startyear'] = startyear

if endyear is not None:
    params['endyear'] = endyear

if components is not None:
    params['components'] = components

params['outputformat'] = 'json'

r = requests.get(url, params=params, allow_redirects=True)

url_csv = f'https://re.jrc.ec.europa.eu/api/seriescalc?lat={lat}&lon={lon}&angle={slope}&aspect={aspect}&pvcalculation={pvcalculation}&startyear={startyear}&endyear={endyear}&components={components}'
url_json = f'{url_csv}&outputformat=json'

r = requests.get(url_json, allow_redirects=True)
data = r.json()


with open('data_out/data.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)
