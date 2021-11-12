# -*- coding: utf-8 -*-
# Author: dotGIS corp

'''
Script que permite hacer una consulta a una base de datos PostgreSQL y generar un archivo JSON.
Configurar credenciales de la base de datos y la salida del JSON según la consulta a realizar.
'''

import logging
import os
import csv
import requests
import math
import time
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

# Set input parameters
name_inputs_csv = 'test'
name_output = 'pvgis_report'

# calc_type seriescalc
pvcalculation = 0
startyear = 2015
endyear = 2015
components = 1
# f'https://re.jrc.ec.europa.eu/api/seriescalc?lat={lat}&lon={lon}&angle={slope}&aspect={aspect}&pvcalculation={pvcalculation}&startyear={startyear}&endyear={endyear}&components={components}'


# calc_type PVcalc
peakpower = 1
loss = 14
# f'https://re.jrc.ec.europa.eu/api/PVcalc?lat={lat}&lon={lon}&peakpower={peakpower}&loss={loss}&angle={slope}&aspect={aspect}'

# Set dirpath
dirpath = os.getcwd()

# Download subfolder
Folder_Reports = dirpath + r'\Reports'
Folder_DownloadsPVGIS = dirpath + r'\DownloadsPVGIS'

# Log file
logging.basicConfig(filename='pvgis_report.log',level=logging.INFO)

def process(data):

    for row in data:
        #print(row)

        #time.sleep(1)
        gid = row["gid"]
        cpro = row["cpro"]
        name_prov = f'"{row["name_prov"]}"'
        rad_dotgis = float(row["radiation"])
        lat = float(row["lat"])
        lon = float(row["long"])
        slope = int(row["slope"])
        if int(row["aspect"]) > 180:
            aspect = int(row["aspect"]) - 360
            aspect = aspect + 180
        else:
            aspect = int(row["aspect"])
            aspect = aspect - 180

        url_csv = f'https://re.jrc.ec.europa.eu/api/seriescalc?lat={lat}&lon={lon}&angle={slope}&aspect={aspect}&pvcalculation={pvcalculation}&startyear={startyear}&endyear={endyear}&components={components}'
        url_json = f'{url_csv}&outputformat=json'

        try:
            # Get and format json
            r = requests.get(url_json, allow_redirects=True)
            json_inputs = r.json()["inputs"]
            elev = json_inputs["location"]["elevation"]
            json_outputs = json_inputs = r.json()["outputs"]
            json_hourly = json_outputs["hourly"]
            Gb_tot = 0
            Gd_tot = 0
            Gr_tot = 0
            for t in json_hourly:
                Gb_tot = Gb_tot + t["Gb(i)"]
                Gd_tot = Gd_tot + t["Gd(i)"]
                Gr_tot = Gr_tot + t["Gr(i)"]
            G_global = Gb_tot + Gd_tot + Gr_tot
            ratio = rad_dotgis / G_global * 100
            line = f"{gid}|{cpro}|{name_prov}|{lon}|{lat}|{elev}|{slope}|{aspect}|{rad_dotgis}|{Gb_tot}|{Gd_tot}|{Gr_tot}|{G_global}|{ratio}"
            t = []
            t.append(line)
            t.append('\n')
            with open(f'{Folder_Reports}\\{name_output}.csv', 'a') as file:
                file.writelines(t)
        except Exception as e:
            print('Error: ', 'gid:', gid, str(e))
            logging.info(f'gid: {gid} - {str(e)}')

        try:
            # Download as CSV file
            r = requests.get(url_csv, allow_redirects=True)
            with open(f'{Folder_DownloadsPVGIS}\\{gid}.csv', 'w', encoding="utf-8") as f:
                f.write(r.text)
        except Exception as e:
            print('Error: ', 'gid:', gid, str(e))
            logging.info(f'gid: {gid} - {str(e)}')



if __name__ == '__main__':

    start = time.time()

    # Write header of the file out
    with open(f'{Folder_Reports}\\{name_output}.csv', 'w', encoding="utf-8") as file:
        file.write('gid|cpro|name_prov|lon|lat|elev|slope|aspect|rad_dotgis|Gb_tot|Gd_tot|Gr_tot|G_global|ratio')
        file.write('\n')

    # Open data
    with open(f'{Folder_Reports}\\{name_inputs_csv}.csv', 'r', encoding="utf-8") as file:
        csv_file = csv.DictReader(file, delimiter='|')
        data = list(csv_file)

    number_of_chunks = 25
    chunk_size = math.ceil(len(data)/25)
    executor = ThreadPoolExecutor(max_workers=number_of_chunks)

    futures = []
    for i in range(number_of_chunks):
        chunk = data[i * chunk_size:(i + 1) * chunk_size]
        futures.append(executor.submit(process, chunk))

    for future in tqdm(concurrent.futures.as_completed(futures), total=number_of_chunks):
        try:
            future.result()
        except Exception as e:
            print('Error: ', str(e))
            logging.info('Error: ', str(e))

    print('Time:', time.time() - start)

    '''
    with multiprocessing.Pool(processes=25) as pool:
        # use the map function of pool to call the function worker() and pass it a raster
        pool.map(process, data)

        pool.close()

        pool.join()
    '''

    '''
    # Write part of the file out
    file = open('rad_test.csv', 'w', encoding="utf-8")
    file.writelines(text)
    file.close()
    # Clear memory
    text.clear()
    del text[:]
    '''


