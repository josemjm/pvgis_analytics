# -*- coding: utf-8 -*-
# Author: José María Jiménez Manzano

"""
ETL Script to Extract from PVGIS API, Transform and LOAD to Clickhouse DB (Include Create statements)

Set the name of PVGIS Tool and Bounding Box to collect data

You can download the Responses setting the directory name for processed data
"""

# importing Project Scripts
from db_clickhouse.clickhouse_management import conn_clickhouse, generator_rows
from utils.multiprocessing_functions import run_apply_async_multiprocessing
from create_lat_lon import create_json_coords
from utils.pvgis_api import pvgis_tool

# importing libraries
import time

# Log file
import logging
logging.basicConfig(filename='pvgis_api.log', level=logging.INFO)

'''
import os
import json
from uuid import uuid4
'''

# Set the name of PVGIS Tool
tool_name = 'seriescalc'

# Set the Bounding Box to collect data
xmin = -3.8
ymin = 40.3
xmax = -3.5
ymax = 40.6

'''
# Set the directory name for processed data
directory = 'data_out'

if not os.path.exists(directory):
    os.makedirs(directory)
'''


def process(api_request):
    # Set max one request per second
    time0 = time.time()

    # Create a clickhouse client
    client = conn_clickhouse()

    # Call to PVGIS API
    data = pvgis_tool(**api_request)

    if data is not None:
        '''
        # To save response as JSON file
        uuid = uuid4()
        tool_name = api_request['tool_name']
        filename = f'{directory}/{tool_name}_{uuid}.json'
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        '''
        n = client.execute("INSERT INTO seriescalc VALUES", (row for row in generator_rows(data)))
        logging.info(f"("
                     f"{data['inputs']['location']['latitude']},"
                     f"{data['inputs']['location']['longitude']}"
                     f"): {n} rows inserted.")

    time1 = time.time()

    if time1 - time0 <= 1:
        time.sleep(1)


if __name__ == "__main__":
    start = time.time()
    print("Running ETL...")
    print(f"Start time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    logging.info(f"Start time: {time.strftime('%Y-%m-%d %H:%M:%S')}")

    # Create a list of API Requests
    api_requests = create_json_coords(xmin, ymin, xmax, ymax, tool_name)

    print("Start the asynchronous multiprocessing...")

    # Apply asynchronous multiprocessing according to maximum requests per second
    result_list_tqdm = run_apply_async_multiprocessing(func=process, argument_list=api_requests, num_processes=30)

    logging.info(f"End time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    logging.info(f"Processed on: {time.time() - start} sec.")
    print(f"End time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Processed on: {time.time() - start} sec.")
