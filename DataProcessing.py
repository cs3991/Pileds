#!/usr/bin/python3

import pandas as pd
import glob
import matplotlib.pyplot as plt
import numpy as np
import datetime
import os

os.chdir('/home/pi/Scripts/python/')

files = glob.glob(r"temperatures/*/*/*.csv", recursive=True)
li = []

for filename in files:
    df = pd.read_csv(filename,
                     index_col=0,
                     parse_dates=[0],
                     delimiter=';',
                     names=["DateTimeIndex",
                            "Temperature_int", "Temperature_ext"],
                     dtype={"Temperature_int":np.float64, "Temperature_ext":np.float64},
                     decimal=','
                     )
    li.append(df)


dataframe = pd.concat(li, axis='index').sort_index()
dataframe = dataframe.interpolate()
dataframe["Temperature_int"] = dataframe["Temperature_int"].rolling('10min').mean()

# dataframe.plot()
# plt.show()
dataframe.to_csv("complete_data.csv")
df_svg = dataframe[datetime.datetime.now() - pd.Timedelta('1 day'):]
df_svg.plot()
plt.grid(True, which="both", axis="y")
plt.savefig("/var/www/html/last24h.svg")
print("Température intérieure :", int(df_svg.Temperature_int[df_svg.Temperature_int.last_valid_index()]*100)/100, "°C")
print('<br>')
print("Température extérieure :", int(df_svg.Temperature_ext[df_svg.Temperature_ext.last_valid_index()]*100)/100, "°C")
