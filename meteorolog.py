# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Погодный модуль для бота."""

# from sys import path
import datetime
import subprocess
# import typing as tpn
import requests
import datetime as pdate

import functions as func
import prototype
# pylint: disable=wrong-import-position
# path.insert(0, "./")
# path.insert(0, "d:/Work/projects/")

# import owm
# os.system()

WEATHER_COMMANDS = ["погода", "пг", "weather", "wt"]
CHANNEL_LIST_KEY = "meteorolog_chats"  # X
ENABLED_IN_CHATS_KEY = "meteorolog_chats"
HINT = ["метео", "meteo"]
FIND_CITY_URL = "http://api.openweathermap.org/data/2.5/find"
FORECAST_WEATHER_URL = "http://api.openweathermap.org/data/2.5/forecast"


class CMeteorolog(prototype.CPrototype):
    """Класс метеоролога."""

    def __init__(self, pconfig):
        super().__init__()
        self.config = pconfig

    def can_process(self, pchat_title: str, pmessage_text: str) -> bool:
        """Возвращает True, если метеоролог может обработать эту команду"""

        if is_enabled(self.config, pchat_title):

            word_list: list = func.parse_input(pmessage_text)
            return word_list[0] in WEATHER_COMMANDS or word_list[0] in HINT
        return False

    # Проверка наличия в базе информации о нужном населенном пункте
    def get_city_id(self, pcity_name: str, plang: str = "ru"):
        """Возвращает ID города"""
        city_id: int = 0
        try:

            res = requests.get(FIND_CITY_URL,
                               params={'q': pcity_name, 'type': 'like',
                                       'units': 'metric', 'lang': plang,
                                       'APPID': self.config["api_key"]})
            data = res.json()
            cities = ["{} ({})".format(d['name'], d['sys']['country'])
                      for d in data['list']]
            print("city:", cities)
            city_id = data['list'][0]['id']
            print('city_id=', city_id)
        except Exception as ex:
            print("Exception (find):", ex)
            pass
        assert isinstance(city_id, int)
        return city_id

    def get_help(self) -> str:  # noqa
        """Пользователь запросил список команд."""
        command_list: str = ""
        for command in WEATHER_COMMANDS:

            command_list += command + ", "
        command_list = command_list[:-2]
        command_list += "\n"
        return command_list

    def get_hint(self, pchat_title: str) -> str:  # [arguments-differ]
        """Возвращает список команд, поддерживаемых модулем.  """
        assert pchat_title is not None, \
            "Assert: [barman.get_hint] " \
            "No <pchat_title> parameter specified!"

        if self.is_enabled(pchat_title):

            return ", ".join(HINT)
        return ""

    def get_wind_direction(self, pdegree):  # noqa
        """Возвращает направление ветра."""
        directions: list = ['С ', 'СВ', ' В', 'ЮВ', 'Ю ', 'ЮЗ', ' З', 'СЗ']
        result: str = ""
        for i in range(0, 8):

            step = 45.
            min_degree = i * step - 45 / 2.
            max_degree = i * step + 45 / 2.
            if i == 0 and pdegree > 360 - 45 / 2.:

                pdegree = pdegree - 360
            if min_degree <= pdegree <= max_degree:

                result = directions[i]
                break
        return result

    def is_enabled(self, pchat_title: str) -> bool:
        """Возвращает True, если метеоролог разрешен на этом канале."""

        return pchat_title in self.config[ENABLED_IN_CHATS_KEY]

    def meteorolog(self, pchat_title: str, pmessage_text: str) -> str:
        """Процедура разбора запроса пользователя."""

        message = ""
        word_list: list = func.parse_input(pmessage_text)
        if self.can_process(pchat_title, pmessage_text):

            # *** Возможно, запросили меню.
            if word_list[0] in HINT:
                message = self.get_help()

            if word_list[0] in WEATHER_COMMANDS:

                if len(word_list) > 1:

                    city_name = word_list[1]
                    city_id = self.get_city_id(city_name)
                    # parameters = ["ansiweather", "-l", word_list[1], "-s", "true", "-a",
                    #               "false", "-p", "false", "-f", "2"]
                    # print(parameters)
                    # process = subprocess.run(parameters, capture_output=True, text=True, check=True)
                    # print("Ok")
                    message = self.request_forecast(city_id)
                    # message = process.stdout
                    # if message.split(" ")[0] == "ERROR:":
                    #     message = "Нет погоды для этого города."
                else:

                    message = "Какую тебе еще погоду?"

        return message
    def parse_weather(self, pdata: list):
        """Парсит выдачу погоды и формирует однострочный прогноз."""
        message: str = ""
        datetime_mask = "%Y-%m-%d %H:%M"
        now = datetime.datetime.now()
        # today = datetime.date.today()
        tomorrow = now + pdate.timedelta(days=1)
        tomorrow_str = tomorrow.strftime(datetime_mask)
        temperature: list = []  # 2
        wind: list = []  # 3
        # direction:
        for line in pdata:

            items: list = line.split()
        return message

    def reload(self):
        pass

    def request_forecast(self, pcity_id, plang: str = "ru"):
        """Запрос погоды на завтра."""
        message: str = ""
        datetime_mask: str = "%Y-%m-%d %H:%M"
        now: datetime.datetime = datetime.datetime.now()
        tomorrow: datetime.datetime = now + pdate.timedelta(days=1)
        min_temperature: int = 100
        max_temperature: int = 0
        min_pressure: int = 10000
        max_pressure: int = 0
        try:

            res = requests.get(FORECAST_WEATHER_URL,
                               params={'id': pcity_id, 'units': 'metric',
                                       'lang': plang, 'APPID': self.config["api_key"]})
            data = res.json()
            # print('city:', data['city']['name'], data['city']['country'])
            for item in data['list']:

                # 1. Выбираем только завтрашние данные
                data_datetime: datetime.datetime = datetime.datetime.fromtimestamp(item['dt']) # / 1e3)
                if data_datetime.date() == tomorrow.date():

                    main = item['main']
                    # *** Температура
                    if main["temp"] < min_temperature:

                        min_temperature = main["temp"]
                    if main["temp"] > max_temperature:
                        max_temperature = main["temp"]
                    # *** Давление
                    if main["pressure"] < min_pressure:
                        min_pressure = main["pressure"]
                    if main["pressure"] > max_pressure:

                        max_pressure = main["pressure"]
                    # print(data)
                    # break
                    # print((item['dt_txt'])[:16], '{0:+3.0f}'.format(item['main']['temp']),
                    #       '{0:2.0f}'.format(item['wind']['speed']) + " м/с",
                    #       self.get_wind_direction(item['wind']['deg']),
                    #       item['weather'][0]['description'])

            # print(f"Temperature: {round(min_temperature)} - {round(max_temperature})")
            # print(f"Pressure: {min_pressure} - {max_pressure}")
            message = f"Temperature: {round(min_temperature)} - {round(max_temperature)}\n"
            message += f" Pressure: {round(min_pressure*0.75)} - {round(max_pressure*0.75)}"
            # message = self.parse_weather(data)
        except Exception as ex:
            print("Exception (forecast):", ex)
            # pass
        return message
# X
def can_process(pconfig: dict, pchat_title: str, pmessage_text: str) -> bool:
    """Возвращает True, если метеоролог может обработать эту команду"""

    if is_enabled(pconfig, pchat_title):
        word_list: list = func.parse_input(pmessage_text)
        return word_list[0] in WEATHER_COMMANDS

    return False

# X
def help() -> str:
    """Пользователь запросил помощь."""
    command_list: str = ""
    for command in enumerate(WEATHER_COMMANDS):
        command_list += f"{command} "
    return command_list

# X
def is_enabled(pconfig: dict, pchat_title: str) -> bool:
    """Возвращает True, если метеоролог разрешен на этом канале."""

    return pchat_title in pconfig[CHANNEL_LIST_KEY]

# X
def meteorolog(pmessage_text: str) -> str:
    """Процедура разбора запроса пользователя."""

    message = None
    word_list: list = func.parse_input(pmessage_text)
    # *** Возможно, запросили меню.
    if word_list[0] in WEATHER_COMMANDS:

        if len(word_list) > 1:

            parameters = ["ansiweather", "-l", word_list[1], "-s", "true", "-a",
                          "false", "-p", "false", "-f", "2"]
            # print(parameters)
            process = subprocess.run(parameters, capture_output=True, text=True, check=True)
            print("Ok")
            message = process.stdout
            if message.split(" ")[0] == "ERROR:":
                message = "Нет погоды для этого города."
        else:

            message = "Какую тебе еще погоду?"

    return message
