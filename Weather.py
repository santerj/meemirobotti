import time
from dataclasses import dataclass

import requests

import config
import weather_codes_FI

KEY = config.weather_api
# Unique city id's for OpenWeatherMap
TAMPERE = '634964'
TURKU = '633679'


@dataclass
class City:
    name: str
    temp: float = -1.0
    wind: float = -1.0
    weather_id: int = -1


class Weather:

    def __init__(self):

        self.__last_call = 0
        self.__tampere = City('Tampere')
        self.__turku = City('Turku')
        self.__cities = [self.__tampere, self.__turku]

        self.call()  # refresh above members

    def call(self):

        self.__last_call = time.time()
        url_tampere = f"http://api.openweathermap.org/data/2.5/weather?id={TAMPERE}&APPID={KEY}"
        url_turku = f"http://api.openweathermap.org/data/2.5/weather?id={TURKU}&APPID={KEY}"

        json_tampere = requests.get(url_tampere).json()
        json_turku = requests.get(url_turku).json()

        cities = [json_tampere, json_turku]
        for json in cities:
            if json['cod'] != 200:
                # something failed
                return
            else:
                self.refresh(json)

    def refresh(self, json):

        name = json['name']

        temp = json['main']['temp']
        wind = json['wind']['speed']
        weather_id = json['weather'][0]['id']

        for city in self.__cities:
            if name == city.name:
                city.temp = temp
                city.wind = wind
                city.weather_id = weather_id

    def parse(self, city, message=''):

        description = weather_codes_FI.codes[city.weather_id]

        if city.name == 'Tampere':
            message += 'Tampereella '
        elif city.name == 'Turku':
            message += 'Turussa '
        else:
            return ''

        message += description + '. '
        return message

    def get_message(self):
        # Current API gives max of 60 request/hour.
        # Get new request only if previous was over 5 minutes ago,
        # just to be on the safe side.
        if time.time() - self.__last_call > 300:
            self.call()

        msg = self.parse(self.__tampere)
        msg = self.parse(self.__turku, msg)

        return msg
