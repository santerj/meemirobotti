import time
from dataclasses import dataclass
import requests

import config

KEY = config.weather_api
# Unique city id's for OpenWeatherMap
TAMPERE = '634964'
TURKU = '633679'


@dataclass
class City:
    name: str
    temp: float = -1.0
    wind: float = -1.0
    weather_main: str = 'null'
    weather_desc: str = 'null'


class Weather:

    def __init__(self):

        self.__last_call = 0
        self.__tampere = City('Tampere')
        self.__turku = City('Turku')
        self.__cities = [self.__tampere, self.__turku]

        self.call()  # refresh above members

    def call(self):

        self.__last_call = time.time()
        url_tampere = f"http://api.openweathermap.org/data/2.5/forecast?id={TAMPERE}&APPID={KEY}"
        url_turku = f"http://api.openweathermap.org/data/2.5/forecast?id={TURKU}&APPID={KEY}"

        json_tampere = requests.get(url_tampere).json()
        json_turku = requests.get(url_turku).json()

        cities = [json_tampere, json_turku]
        for json in cities:
            if json['cod'] != '200':
                # something failed
                return
            else:
                self.refresh(json)

    def refresh(self, json):

        name = json['city']['name']
        station = json['list'][0]

        temp = station['main']['temp']
        weather_main = station['weather'][0]['main']
        weather_desc = station['weather'][0]['description']
        wind = station['wind']['speed']

        for city in self.__cities:
            if name == city.name:
                city.temp = temp
                city.weather_main = weather_main
                city.weather_desc = weather_desc
                city.wind = wind
