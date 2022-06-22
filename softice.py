#! /usr/bin/python3
# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Бот для Телеграмма"""

import json
import random
import telebot
from telebot import apihelper
from datetime import datetime

import functions as func
import babbler
import barman
import theolog
import librarian
import mafiozo
import meteorolog


INTERVAL = 0
NON_STOP = True
CONFIG_FILE_NAME = "config.json"

COMMAND_SIGNS = "/!."
HELP_COMMAND = "help"
HELP_MESSAGE = "В настоящий момент я понимаю только следующие команды:"
GREETINGS = ["Здорово", "Хай", "Привет", "Трям", "И те не хворать", "Приветствую",
             "Здравствуйте", "Здоровеньки булы", "Симметрично", "О, привет",
             "Рад видеть", "Я вас категорически приветствую", "О, и ты здесь",
             "Приветище", "Доброго времени суток"]

SMILES = ["8)", "=)", ";)", ":)", "%)", "^_^"]
BOT_NAME = "SoftIceBot"
CONTINUE_RUNNING = 0
QUIT_BY_DEMAND = 1
BOT_STATUS = CONTINUE_RUNNING
LAST_BABBLER_PHRASE_TIME = datetime.now()

class CQuitByDemand(Exception):
    """Исключение выхода."""
    def __init__(self):
        self.message = "Выход по требованию..."
        super().__init__(self.message)


# *** Читаем конфигурацию
with open(CONFIG_FILE_NAME, "r", encoding="utf-8") as config_file:

    BOT_CONFIG = json.load(config_file)

if BOT_CONFIG["proxy"]:

    apihelper.proxy = {'https':BOT_CONFIG["proxy"]}
SoftIceBot = telebot.TeleBot(BOT_CONFIG["token"])


def send_help(pconfig: dict, pmessage: object):
    """По запросу пользователя отправляет подсказки пло всем модулям."""

    barman_message = barman.get_help(pconfig, pmessage.chat.title)
    theolog_message = theolog.get_help(pconfig, pmessage.chat.title)
    librarian_message = librarian.get_help(pconfig, pmessage.chat.title)

    if barman_message or theolog_message or librarian_message:

        SoftIceBot.send_message(pmessage.chat.id, HELP_MESSAGE)
    if barman_message:

        SoftIceBot.send_message(pmessage.chat.id, barman_message)
    if theolog_message:

        SoftIceBot.send_message(pmessage.chat.id, theolog_message)
    if librarian_message:

        SoftIceBot.send_message(pmessage.chat.id, librarian_message)


def babbler_process(pconfig: dict, pchat_id: int, pchat_title: str,
                    puser_title, pmessage_text):
    """По возможности обработать команду болтуном."""
    # print("*** SI:BBLPR:MSGTX ", pmessage_text)
    if babbler.can_process(pconfig, pchat_title, pmessage_text):

        print("*** SI:BBLPR:")
        # *** ... точняк
        # message = barman.barman(pmessage.text, pmessage.from_user.user_name)
        message = babbler.babbler(pmessage_text, puser_title)
        print("*** SI:BBLPR:MSG ", message)
        if message is not None:

            print(" .. ok.")
            SoftIceBot.send_message(pchat_id, message)
            return True
    return False


def barman_process(pconfig: dict, pchat_id: int, pchat_title: str,
                   puser_title, pmessage_text):
    """По возможности обработать команду барменом."""

    if barman.can_process(pconfig, pchat_title, pmessage_text):

        # *** ... точняк
        # message = barman.barman(pmessage.text, pmessage.from_user.user_name)
        message = barman.barman(pmessage_text, puser_title)
        if message is not None:

            print(" .. ok.")
            SoftIceBot.send_message(pchat_id, message)
            return True
    return False


def theolog_process(pconfig: dict, pchat_id: int, pchat_title: str,
                    pmessage_text):
    """По возможности обработать команду теологом"""

    if theolog.can_process(pconfig, pchat_title, pmessage_text):

        # *** как пить дать.
        message = theolog.theolog(pmessage_text)
        if message is not None:

            print(" .. ok.")
            SoftIceBot.send_message(pchat_id, message)
            return True
    return False


def meteorolog_process(pconfig: dict, pchat_id: int, pchat_title: str,
                       pmessage_text: str):
    """По возможности обработать команду метеорологом"""
    if meteorolog.can_process(pconfig, pchat_title, pmessage_text):

        # *** как пить дать.
        message = meteorolog.meteorolog(pmessage_text)
        if message is not None:

            print(" .. ok.")
            SoftIceBot.send_message(pchat_id, message)
            return True
    return False


def librarian_process(pconfig: dict, pchat_id: int, pchat_title: str,
                      puser_title, pmessage_text):
    """ Если это команда библиотекаря... """
    if librarian.can_process(pconfig, pchat_title, pmessage_text):

        # *** как пить дать.
        message = librarian.librarian(pconfig,
                                      puser_title,
                                      pmessage_text)
        if message is not None:

            print(" .. ok.")
            SoftIceBot.send_message(pchat_id, message)
            return True
    return False


def mafiozo_process(pconfig: dict, pchat_id: int, pchat_title: str,
                    puser_id, puser_title: str, pmessage_text):
    """По возможности обработать команду теологом"""

    if mafiozo.can_process(pconfig, pchat_title, pmessage_text):

        message: str = ""
        markup: object = None
        addressant: int = 0
        # *** как пить дать.
        message, addressant, markup = mafiozo.mafiozo(pconfig, pmessage_text, pchat_id, puser_id, puser_title)
        if message is not None:

            print(" .. ok.")
            if markup is None:

                SoftIceBot.send_message(addressant, message)
            else:

                SoftIceBot.send_message(addressant, message, reply_markup=markup)
            return True
    return False


def process_modules(pchat_id: int, pchat_title: str,
                    puser_id: int, puser_title: str,
                    pmessage_text):
    """Пытается обработать команду различными модулями."""

    # if not babbler_process(BOT_CONFIG, pchat_id, pchat_title, puser_title, pmessage_text):

    # *** Проверим, не запросил ли пользователь что-то у бармена...
    if not barman_process(BOT_CONFIG, pchat_id, pchat_title, puser_title, pmessage_text):

        # *** Проверим, не запросил ли пользователь что-то у теолога...
        if not theolog_process(BOT_CONFIG, pchat_id, pchat_title, pmessage_text):

            if not meteorolog_process(BOT_CONFIG, pchat_id, pchat_title, pmessage_text):

                if not librarian_process(BOT_CONFIG, pchat_id,
                                         pchat_title, puser_title, pmessage_text):

                    if not mafiozo_process(BOT_CONFIG, pchat_id, pchat_title,
                                           puser_id, puser_title, pmessage_text):

                        print(" .. fail.")

                # SoftIceBot.send_message(pmessage.chat.id,
                # f"Ну и запросы у вас, {user_name} !")


def bot_command(pmessage: object):
    """Обработка команд бота."""

    result = True
    command = pmessage.text[1:].lower()
    user_title = pmessage.from_user.first_name
    user_name = pmessage.from_user.username
    chat_id = pmessage.chat.id

    if command in  ["привет", "hi"]:

        SoftIceBot.send_message(chat_id,
                                random.choice(GREETINGS) + ", " + user_title)
    elif command == "тевирп":

        SoftIceBot.send_message(chat_id,
                                "Тевирп! Тсссс.... o_O")
    elif command in ["конфиг", "config"]:

        # *** или конфиг
        global BOT_CONFIG
        if user_name == BOT_CONFIG["master"]:

            SoftIceBot.send_message(chat_id, "Обновляю конфигурацию.")
            with open(CONFIG_FILE_NAME, "r", encoding="utf-8") as configuration_file:

                BOT_CONFIG = json.load(configuration_file)
            SoftIceBot.send_message(chat_id, "Конфигурация обновлена.")
        else:

            SoftIceBot.send_message(chat_id, f"Извини, {user_title}, у меня другой хозяин!")
    elif command in ["прощай", "bye"]:

        if user_name == BOT_CONFIG["master"]:

            # SoftIceBot.send_message(chat_id, f"Добби свободен! Прощай, {user_title} !!")
            raise CQuitByDemand()
        SoftIceBot.send_message(chat_id, f"Извини, {user_title}, у меня другой хозяин!")
    else:

        result = False
    return result


@SoftIceBot.callback_query_handler(func=lambda call: True)
def callback_inline(call):

    mafiozo_process(BOT_CONFIG, call.message.chat.id, call.message.chat.title,
                    call.from_user.id, call.from_user.username, call.data)
    #process_callback(pmessage_text: str, puser_id: int, puser_name: str):
    # Если сообщение из чата с ботом
    #'from_user': {'id': 1978360349, 'is_bot': True, 'first_name': 'SoftIce', 'username': 'SoftIceBot', 'last_name': None, 'language_code': None, 'can_join_groups': None, 'can_read_all_group_messages': None, 'supports_inline_queries': None}
    #'chat': {'id': -583831606, 'type': 'group', 'title': 'Ботовка', 'username': None, 'first_name': None, 'last_name': None, 'photo': None, 'bio': None, 'description': None, 'invite_link': None, 'pinned_message': None, 'permissions': None, 'slow_mode_delay': None, 'message_auto_delete_time': None, 'sticker_set_name': None, 'can_set_sticker_set': None, 'linked_chat_id': None, 'location': None},

    #print(call.message)
    #print(call.message.chat.id)
    #print(call.message.message_id)
    #print(call.inline_message_id)
    #print(call.from_user.username)
    #print(call.from_user.id)
    #if call.message:

        #if call.data == "test":

            #SoftIceBot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Пыщь")
    # Если сообщение из инлайн-режима
    #if call.inline_message_id:
        # call.message.chat.id
        # call.message.message_id
        # call.inline_message_id
        #if call.data == "test":

            #SoftIceBot.edit_message_text(inline_message_id=call.inline_message_id, text="Бдыщь")


@SoftIceBot.message_handler(func=lambda message: True, content_types=['text'])
def get_text_messages(pmessage: object):
    """Процедура обработки ввода команд пользователем."""

    word_list: list = func.parse_input(pmessage.text)
    message_text:str = pmessage.text
    user_title: str = pmessage.from_user.first_name
    user_id: int = pmessage.from_user.id
    chat_id: int = pmessage.chat.id
    chat_title: str = pmessage.chat.title

    # *** В начале строки есть знак команды?
    if message_text[0:1] in COMMAND_SIGNS:

        if not bot_command(pmessage):

            print(" ", user_title, "says: \"", message_text, "\"", end="")
            if word_list[0] == HELP_COMMAND:

                send_help(BOT_CONFIG, pmessage)
            else:

                process_modules(chat_id, chat_title, user_id, user_title, message_text)
    # *** Нет. если обращаются к боту...
    else:

        if (")" in message_text) and (word_list[0] == BOT_NAME):

            # *** И это смайлик..
            SoftIceBot.send_message(chat_id, user_title + " " + random.choice(SMILES))
        else:

            # *** В дело вступает болтун!
            global LAST_BABBLER_PHRASE_TIME
            print("*** SI:GTM:MSGTX ", message_text)
            minutes = (datetime.now() - LAST_BABBLER_PHRASE_TIME).total_seconds() / 60
            if minutes > 0:

                babbler_process(BOT_CONFIG, chat_id, chat_title, user_title, message_text)
                LAST_BABBLER_PHRASE_TIME = datetime.now()


if __name__ == "__main__":

    babbler.reload_babbling()
    barman.reload_bar()
    librarian.reload_library()
    try:
        while BOT_STATUS == CONTINUE_RUNNING:

            SoftIceBot.polling(none_stop=NON_STOP, interval=INTERVAL)
            print(f"Bot status = {BOT_STATUS}")

    except CQuitByDemand as ex:

        print(ex.message)
        SoftIceBot.stop_polling()
