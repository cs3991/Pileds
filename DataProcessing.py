#!/usr/bin/python3
# coding=utf-8
import matplotlib
import pandas as pd
import glob
import matplotlib.pyplot as plt
import numpy as np
import datetime
import dateutil
import os
import re
import json

from tictoc import *


def generate_complete_data():
    # for testing on windows : switch commented lines
    os.chdir('/home/famille/dev/Pileds/')
    # os.chdir('Z:\Developpement\pyled')

    files = glob.glob(r"temperatures/*/*/*.csv", recursive=True)
    li = []
    # print('files : ', files)
    for filename in files:
        df = pd.read_csv(filename,
                         index_col=0,
                         parse_dates=[0],
                         delimiter=';',
                         names=["DateTimeIndex",
                                "Temperature_int", "Temperature_ext"],
                         dtype={"Temperature_int": np.float64, "Temperature_ext": np.float64},
                         decimal=','
                         )
        li.append(df)

    dataframe = pd.concat(li, axis='index').sort_index()

    # Save last measured temperatures
    indoor_temp = int(dataframe.Temperature_int[dataframe.Temperature_int.last_valid_index()] * 100) / 100
    outdoor_temp = int(dataframe.Temperature_ext[dataframe.Temperature_ext.last_valid_index()] * 100) / 100

    # Interpolate missing samples and smoothing
    dataframe = dataframe.interpolate()
    dataframe["Temperature_int"] = dataframe["Temperature_int"].rolling('20min').mean()
    dataframe["Temperature_ext"] = dataframe["Temperature_ext"].rolling('30min').mean()

    # Save all computed data to a singular file
    dataframe.to_csv("complete_data.csv")

    # Plot data for the last 24 hours
    df_svg = dataframe[datetime.datetime.now() - pd.Timedelta('1 day'):]

    fig, ax1 = plt.subplots()
    # Indoor temperature
    df_svg["Temperature_int"].plot(color='tab:red')
    ax1.tick_params(axis='y', labelcolor='tab:red')
    ax1.set_ylabel('Température intérieure', color='tab:red')
    plt.grid(True, which="both", axis="y")
    # Outdoor temperature
    ax2 = ax1.twinx()
    df_svg["Temperature_ext"].plot(color='tab:blue')
    ax2.tick_params(axis='y', labelcolor='tab:blue')
    ax2.set_ylabel('Température extérieure', color='tab:blue')
    fig.tight_layout()

    # for testing on windows : switch commented lines
    # plt.show()
    plt.savefig("last24h.svg")

    # print("Température intérieure :",indoor_temp , "°C")
    # print('<br>')
    # print("Température extérieure :", outdoor_temp, "°C")
    return indoor_temp, outdoor_temp


def generate_graph():
    os.chdir('/home/famille/dev/Pileds/')
    matplotlib.use('SVG')
    today = datetime.datetime.now()
    filenames = [(today - datetime.timedelta(days=1)).strftime('%Y/%m/%d'), today.strftime('%Y/%m/%d')]
    files = []
    for filename in filenames:
        files.extend(glob.glob(r"temperatures/" + filename + ".csv"))
    li = []
    for filename in files:
        df = pd.read_csv(filename,
                         index_col=0,
                         parse_dates=[0],
                         delimiter=';',
                         names=["DateTimeIndex",
                                "Temperature_int", "Temperature_ext"],
                         dtype={"Temperature_int": np.float64, "Temperature_ext": np.float64},
                         decimal=','
                         )
        li.append(df)
        # print(li)

    df_svg = pd.concat(li, axis='index').sort_index()[datetime.datetime.now() - pd.Timedelta('1 day'):]

    # Save last measured temperatures
    indoor_temp = df_svg.Temperature_int[df_svg.Temperature_int.last_valid_index()]
    outdoor_temp = df_svg.Temperature_ext[df_svg.Temperature_ext.last_valid_index()]

    # Interpolate missing samples and smoothing
    df_svg = df_svg.interpolate()
    df_svg["Temperature_int"] = df_svg["Temperature_int"].rolling('20min').mean().round(2)
    df_svg["Temperature_ext"] = df_svg["Temperature_ext"].rolling('30min').mean().round(2)

    with open('last24h.js', 'w') as f:
        f.write('let temperatures = [\n')
        for k, v in df_svg.T.to_dict().items():
            k = k.replace(tzinfo=dateutil.tz.gettz())
            f.write("{date:" + json.dumps(int(k.timestamp() * 1000)) + ", " + re.sub(r'[{"\']', '', json.dumps(v))+',\n')
        f.write('];')


    # df_svg.to_csv("last24h.csv", float_format='%.1f')

    fig, ax1 = plt.subplots()
    # Indoor temperature
    df_svg["Temperature_int"].plot(color='tab:red')
    ax1.tick_params(axis='y', labelcolor='tab:red')
    ax1.set_ylabel('Température intérieure', color='tab:red')
    plt.grid(True, which="both", axis="y")
    # Outdoor temperature
    ax2 = ax1.twinx()
    df_svg["Temperature_ext"].plot(color='tab:blue')
    ax2.tick_params(axis='y', labelcolor='tab:blue')
    ax2.set_ylabel('Température extérieure', color='tab:blue')
    fig.tight_layout()
    plt.savefig("last24h.svg")
    return indoor_temp, outdoor_temp


def main():
    generate_complete_data()
    # generate_graph()


if __name__ == "__main__":
    main()
