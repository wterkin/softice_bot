# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Погодный модуль для бота."""

import subprocess
# import typing as tpn

import functions as func

# os.system()

CHANNEL_LIST_KEY = "policeman_chats"
READ_ONLY_PERIOD = 600
READ_ONLY_MESSAGE = f"Помолчите {READ_ONLY_PERIOD/60} минут"
	
def set_ro(bot, pchat_id, puser_id):
    bot.restrict_chat_member(pchat_id, puser_id, until_date=time()+READ_ONLY_PERIOD)
    bot.send_message(pchat_id, READ_ONLY_MESSAGE)


def is_enabled(pconfig: dict, pchat_title: str) -> bool:
    """Возвращает True, если метеоролог разрешен на этом канале."""

    return pchat_title in pconfig[CHANNEL_LIST_KEY]


def policeman(pmessage_text: str) -> str:
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
