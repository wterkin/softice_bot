# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Погодный модуль для бота."""

import subprocess
# import typing as tpn

import functions as func

# os.system()

WEATHER_COMMANDS = ["weather", "wt", "погода", "пг", "п"]
CHANNEL_LIST_KEY = "meteorolog_chats"


def can_process(pconfig: dict, pchat_title: str, pmessage_text: str) -> bool:
    """Возвращает True, если метеоролог может обработать эту команду"""

    if is_enabled(pconfig, pchat_title):

        word_list: list = func.parse_input(pmessage_text)
        return word_list[0] in WEATHER_COMMANDS

    return False


def help() -> str:
    """Пользователь запросил помощь."""
    command_list: str = ""
    for command in enumerate(WEATHER_COMMANDS):

        command_list += f"{command} "
    return command_list


def is_enabled(pconfig: dict, pchat_title: str) -> bool:
    """Возвращает True, если метеоролог разрешен на этом канале."""

    return pchat_title in pconfig[CHANNEL_LIST_KEY]


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
