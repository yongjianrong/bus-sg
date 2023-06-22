# -*- coding: utf-8 -*-
from bus import Bus
from mrt import MRT
from file import write_file, read_file, exists
import json
import requests
import pandas as pd
from keys import API_KEY
# 
# b = Bus()
# m = MRT()
"""
Created on Thu Jun 22 14:23:23 2023

@author: Yong Jian Rong
"""

# b.get_stops_for_each_service([98,99])

services_stops_dict = read_file('temp/bus', 'services_stops_dict.json')
all_stops_dict = read_file('temp/bus', 'all_stops_dict.json')

# combined_stops_and_services_dict = b.combine_stops_and_services(services_stops_dict, all_stops_dict)

# mrt_stations = read_file('temp/mrt', 'stations.json')
# combined_mrt = b.add_mrt_data(combined_stops_and_services_dict, mrt_stations)
# write_file(combined_mrt, 'data', 'all')

from datetime import datetime, timezone
from math import floor
def timenow(silent=True):
    localtime = datetime.now(timezone.utc).astimezone()
    printtime = str(localtime)
    if silent is False:
        print("It is now", printtime)
    return localtime


def getBusArrivals(code='28519'):
    localtime = timenow()
    print(f"Information retrieved as of {localtime}.")
    code = str(code)
    url = f"http://datamall2.mytransport.sg/ltaodataservice/BusArrivalv2?BusStopCode={code}"

    payload = {}
    headers = {
      'AccountKey': API_KEY,
      'accept': 'application/json',
      'Acc': ''
    }

    response = requests.request("GET", url, headers=headers, data=payload).text
    # print(f"Response is of the type {type(response)}.\n")
    response_info = json.loads(response)
    # for keys, values in response_info.items():
    #     print(keys,":",values,"\n")
        
    number_of_buses = len(response_info["Services"])
    print(f"There are a total of {number_of_buses} bus services at Bus Stop {code}.")
    for bus in response_info["Services"]:
        service = bus['ServiceNo']
        timing = bus['NextBus']['EstimatedArrival']
        #timeobject = datetime(timing)
        predictedarr = datetime.strptime(timing, "%Y-%m-%dT%H:%M:%S%z")
        print(f"Pred Arr Time for {service}:", predictedarr)
        countdown =  predictedarr - localtime
        #print("Type of countdown;",type(countdown))
        minute = floor(countdown.total_seconds()/60)
        second = int(round(countdown.total_seconds()%60,0))
        if minute > 0:
            print(f"Countdown to {service} arrival: {minute} mins {second} sec.\n")
        elif minute < 0:
            print(f"{service} is late by {minute} mins {second} sec.\n")

        # DEBUG
        # print("Type of 'service' var:", type(service))
        # print("Timing is of the type",type(timing))
        #print(service,timing,"\n")
    
    newdict = {bus['ServiceNo']: bus['NextBus']['EstimatedArrival'] for bus in response_info["Services"]}
    
    return newdict


print("Print dict outputs:")
print(getBusArrivals(28509))


