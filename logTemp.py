#!/usr/bin/python3
import glob
import os
import subprocess
import re
import time
from datetime import datetime
from datetime import timedelta
import requests

API_KEY = '7339f560987519be7f4ef21a7d2dc1ac'
file_temperature = '/sys/bus/w1/devices/{}/temperature'
DELAY_API = 10  # Number of minutes to wait between two calls to the api
DELAY_SENSOR = 2  # Number of minutes to wait between two measures of the sensor


def update_sensors_list():
    ids = [e.split('/')[-1] for e in glob.glob('/sys/bus/w1/devices/*')]
    final_ids = []
    for id in ids:
        if os.path.exists(file_temperature.format(id)):
            final_ids.append(id)
    if len(final_ids) == 0:
        print('No sensor connected')
    return final_ids


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


def fetch_sensor_temp(id):
    try:
        out = subprocess.Popen(['cat', file_temperature.format(id)],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)
        stdout, stderr = out.communicate()
        in_temp = float(re.search(r'(\d{5})', str(stdout)).group(1)) / 1000
        print(f"Sensor {id} fetched: {in_temp} °C")
        return in_temp
    except:
        print('Error getting indoor temperature')
        return ''


def fetch_sensors_list(ids_list):
    """
    Measure and average temperature from a list of sensor ids
    """
    in_temp = 0
    for id in ids_list:
        in_temp += fetch_sensor_temp(id)
    in_temp /= len(ids_list)
    return in_temp


def fetch_all_sensors():
    """
    Measure and average all sensors currently connected to the raspberry pi
    """
    return fetch_sensors_list(update_sensors_list())


def fetch_outdoor_temp():
    try:
        response = requests.get(
            'https://api.openweathermap.org/data/2.5/weather?id=3017879&units=metric&appid=' + API_KEY)
        # print("request sent")
        ex_temp = float(response.json()['main']['temp'])
        print('Outdoor temp fetched:', ex_temp)
        return ex_temp
    except:
        print('Error communicating with API')
        return ''


def fetch_network_sensor_temp(argument):
    # try:
    out = subprocess.Popen(
        ['ssh', 'pi@192.168.0.16', '/home/pi/ProgrammationAttiny85/ErsatzDeServeur/get_temp.sh', argument],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    stdout, stderr = out.communicate()
    temp = float(re.search(r'T=(-?[0-9]+\.?[0-9]*)\/', str(stdout)).group(1))
    print(f"Network sensor {argument} fetched: {temp} °C")
    return temp
    # except:
    #     print(f'Error getting network sensor {argument} temperature')
    #     return ''


def get_last_temps():
    today = datetime.now()
    filenames = [today.strftime('%Y/%m/%d'), (today - timedelta(days=1)).strftime('%Y/%m/%d')]
    files = []
    for filename in filenames:
        files.extend(glob.glob(r"temperatures/" + filename + ".csv"))
    files.sort()
    with open(files[-1], 'r') as file:
        line = file.readline(-1)
    line_split = line.split(';')
    indoor_temp = float(line_split[1].replace(',', '.'))
    outdoor_temp = float(line_split[2].replace(',', '.'))
    return indoor_temp, outdoor_temp


def main():
    ids_list = update_sensors_list()
    past_time_sensor = datetime.now() - timedelta(minutes=30)
    past_time_api = datetime.now() - timedelta(minutes=30)
    print("Python temperature log started: \n" +
          "  - Sensor logged every " + str(DELAY_SENSOR) + " min\n" +
          "  - API fetched every " + str(DELAY_API) + " min")

    try:
        while 1:
            date = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            if datetime.now() - past_time_sensor > timedelta(minutes=DELAY_SENSOR):
                in_temp_1 = round(fetch_all_sensors(), ndigits=2)
                in_temp_2 = round(fetch_network_sensor_temp('int'), 2)
                out_temp_2 = round(fetch_network_sensor_temp('ext'), 2)
                past_time_sensor = datetime.now()
            else:
                in_temp_1 = ''
                in_temp_2 = ''
                out_temp_2 = ''
            if datetime.now() - past_time_api > timedelta(minutes=DELAY_API):
                out_temp_1 = round(fetch_outdoor_temp(), ndigits=2)
                past_time_api = datetime.now()

            else:
                out_temp_1 = ''
            try:
                filename = 'temperatures/' + date.split(' ')[0] + '.csv'
                create_dir(filename, True)
                with open(filename, 'a') as file:
                    file.write(
                        f"{date};{str(in_temp_1).replace('.', ',')};{str(out_temp_1).replace('.', ',')};"
                        f"{str(out_temp_2).replace('.', ',')};{str(in_temp_2).replace('.', ',')}\n")
            except IOError:
                print(datetime.now().strftime("%Y/%m/%d-%H:%M:%S") + " Erreur d'ouverture du fichier")
                pass
            time.sleep(min(DELAY_API, DELAY_SENSOR) * 60)

    except KeyboardInterrupt:
        exit()


if __name__ == '__main__':
    main()
