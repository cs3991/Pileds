#!/usr/bin/python3

import os
import subprocess
import re
import time
from datetime import datetime
from datetime import timedelta
import requests

API_KEY = '7339f560987519be7f4ef21a7d2dc1ac'
file_temperature = '/sys/bus/w1/devices/w1_bus_master1/28-3c01a816d8df/w1_slave'
NB_MIN_DELAY_API = 10
NB_MIN_DELAY_SENSOR = 2

print("Python temperature log started: \n" +
      "Sensor logged each" + str(NB_MIN_DELAY_SENSOR) + "min\n" +
      "API fetched each" + str(NB_MIN_DELAY_API) + "min")


def create_dir(path, isFile=False):
    """
    Creates folders that match the given path in current directory
    :param isFile: Bool: is the path for a file
    :param path: str: path of folder to create
    :return: str: file name if isFile is True
    """
    folder_list = path.split('/')
    if isFile:
        file_name = folder_list.pop(-1)
    else:
        file_name = ''
    current_directory = ''
    for folder in folder_list:
        if not os.path.exists(current_directory + folder):
            os.mkdir(current_directory + folder)
        current_directory = current_directory + folder + '/'
    return file_name

def fetch_sensor_temp():
    try:
        out = subprocess.Popen(['cat', file_temperature],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)
        stdout, stderr = out.communicate()
        #print("sensor fetched")
        return float(re.search(r't=(\d{5})', str(stdout)).group(1)) / 1000
    except:
        return ''

def fetch_outdoor_temp():
    try:
        response = requests.get('http://api.openweathermap.org/data/2.5/weather?id=3014728&units=metric&appid=' + API_KEY)
        #print("request sent")
        return float(response.json()['main']['temp'])
    except:
        return ''


past_time_sensor = datetime.now() - timedelta(minutes=30)
past_time_api = datetime.now() - timedelta(minutes=30)
try:
    while 1:
        date = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        if datetime.now() - past_time_sensor > timedelta(minutes=NB_MIN_DELAY_SENSOR):
            in_temp = fetch_sensor_temp()
            past_time_sensor = datetime.now()
        else:
            in_temp = ''
        if datetime.now() - past_time_api > timedelta(minutes=NB_MIN_DELAY_API):
            out_temp = fetch_outdoor_temp()
            past_time_api = datetime.now()

        else:
            out_temp = ''
        try:
            filename = 'temperatures/' + date.split(' ')[0] + '.csv'
            # filename = 'temperatures.csv'
            create_dir(filename, True)
            with open(filename, 'a') as file:
                file.write(date + ';' + str(in_temp).replace('.', ',') + ';' + str(out_temp).replace('.', ',') + '\n')
        except IOError :
            print(datetime.now().strftime("%Y/%m/%d-%H:%M:%S") + " Erreur d'ouverture du fichier")
            pass
        time.sleep(120)

except KeyboardInterrupt:
    exit()
