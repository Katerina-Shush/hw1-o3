#!/usr/bin/env python3

import argparse
import json
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from scipy.io import netcdf

parser = argparse.ArgumentParser()
parser.add_argument('longitude', metavar='LON', type=float, help='Longitude, deg')
parser.add_argument('latitude',  metavar='LAT', type=float, help='Latitude, deg')

def solver(lon, lat):
    with netcdf.netcdf_file('MSR-2.nc', mmap=False) as netcdf_file:
        variables = netcdf_file.variables
        lat_index = np.searchsorted(variables['latitude'].data, lat)
        lon_index = np.searchsorted(variables['longitude'].data, lon)
        data = variables['Average_O3_column'][:, lat_index, lon_index]

        _dict = get_dict(data, lon, lat)
        save_as_json(_dict)
        save_plot(variables['time'].data, data)

def get_dict(data, lon, lat):
    _data = {
        "coordinates": [lon, lat],
        "jan": {
            "min": float(data[::12].min()),
            "max": float(data[::12].max()),
            "mean": np.mean(data[::12])
        },
        "jul": {
            "min": float(data[6::12].min()),
            "max": float(data[6::12].max()),
            "mean": np.mean(data[6::12])
        },
        "all": {
            "min": float(data.min()),
            "max": float(data.max()),
            "mean": np.mean(data)
        }
    }

    return _data

def save_as_json(data):
    with open('ozon.json', 'w') as fp:
        json.dump(data, fp)

def save_plot(time, data):
    matplotlib.rcParams['font.size'] = 16
    plt.figure(figsize=(30,20))
    plt.xlabel("Time")
    plt.ylabel("Ozone Concentration")
    plt.plot(time[::12], data[::12], label = 'JAN')
    plt.plot(time[6::12], data[6::12], label = 'JUL')
    plt.plot(time, data, '-', label = 'ALL')
    plt.legend()
    plt.savefig('ozon.png')


args = parser.parse_args()
lon = args.longitude
lat = args.latitude
solver(lon, lat)
