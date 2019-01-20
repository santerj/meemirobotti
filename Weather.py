import requests
import time

import config

KEY = config.weather_api
# Unique city id's for OpenWeatherMap
TAMPERE = '634964'
TURKU = '633679'


class Weather:

    def __init__(self):

        self.__last_call = 0
        self.__tampere = ''
        self.__turku = ''
        self.call()

    def call(self):

        url_tampere = f"http://api.openweathermap.org/data/2.5/forecast?id={TAMPERE}&APPID={KEY}"
        url_turku = f"http://api.openweathermap.org/data/2.5/forecast?id={TURKU}&APPID={KEY}"

        self.__tampere = requests.get(url_tampere).json()
        self.__turku = requests.get(url_turku).json()
        self.__last_call = time.time()


def main():

    thing = Weather()

main()