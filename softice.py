#! /usr/bin/python3
# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Бот для Телеграмма"""

import sys
import json
import random
from datetime import datetime
import telebot
from telebot import apihelper

import functions as func
import babbler
import barman
import theolog
import librarian
import mafiozo
import meteorolog


INTERVAL: int = 0
NON_STOP: bool = True
CONFIG_FILE_NAME: str = "config.json"

COMMAND_SIGNS: str = "/!."
HELP_COMMAND: str = "help"
HELP_MESSAGE: str = "В настоящий момент я понимаю только следующие команды:"
#GREETINGS = ["Здорово", "Хай", "Привет", "Трям", "И те не хворать", "Приветствую",
             #"Здравствуйте", "Здоровеньки булы", "Симметрично", "О, привет",
             #"Рад видеть", "Я вас категорически приветствую", "О, и ты здесь",
             #"Приветище", "Доброго времени суток"]

SMILES: list = ["8)", "=)", ";)", ":)", "%)", "^_^"]
BOT_NAME: str = "SoftIceBot"
CONTINUE_RUNNING: int = 0
QUIT_BY_DEMAND: int = 1
BOT_STATUS: int = CONTINUE_RUNNING
LAST_BABBLER_PHRASE_TIME = datetime.now()
ALLOWED_CHATS: str = "allowed_chats"
BOT_CONFIG = None

TOKEN_KEY: str = "token"  # !
CONFIG_COMMANDS: list = ["конфиг", "config"]  # !
EXIT_COMMANDS: list = ["прощай", "bye"]
BABBLER_PERIOD: int = 10
# message.delete()

class CQuitByDemand(Exception):
    """Исключение выхода."""
    def __init__(self):
        self.message = "Выход по требованию..."
        super().__init__(self.message)


# *** Читаем конфигурацию
# global BOT_CONFIG
with open(CONFIG_FILE_NAME, "r", encoding="utf-8") as config_file:

    BOT_CONFIG = json.load(config_file)

if BOT_CONFIG["proxy"]:

    apihelper.proxy = {'https': BOT_CONFIG["proxy"]}
SoftIceBot = telebot.TeleBot(BOT_CONFIG["token"])


class CSoftIceBot():
    """Универсальный бот для Телеграмма."""

    def __init__(self):
        """Конструктор класса."""
        super().__init__()
        self.config = {}
        self.last_babbler_phrase_time: datetime = datetime.now()
        self.robot = telebot.TeleBot(self.config[TOKEN_KEY])

    def load_config(self):
        """Загружает конфигурацию из JSON."""
        with open(CONFIG_FILE_NAME, "r", encoding="utf-8") as config_file:

            self.config = json.load(config_file)

    def check_if_this_chat_enabled(pchat_id: int, pchat_title: str):
        """Проверяет, находится ли данный чат в списке разрешенных."""
        if pchat_title not in self.config[ALLOWED_CHATS]:

            self.robot.send_message(pchat_id, "Вашего чата нет в списке разрешённых. Чао!")
            self.robot.leave_chat(chat_id)
            print(f"Караул! Меня похитили и затащили в чат {chat_title}! Но я удрал.")

    def process_message(self, pmessage):
        """Обработчик сообщений."""

        message_text: str = pmessage.text
        word_list: list = func.parse_input(message.text)
        chat_id: int = pmessage.chat.id
        chat_title: str = pmessage.chat.title
        user_title: str = pmessage.from_user.first_name
        user_id: int = pmessage.from_user.id

        # *** Проверим, легитимный ли этот чата
        check_if_this_chat_enabled(chat_id, chat_title)

        # *** Боту дали команду?
        if message_text[0:1] in COMMAND_SIGNS:

            if not bot_command(pmessage):

                # print(" ", user_title, "says: \"", message_text, "\"", end="")
                if word_list[0] == HELP_COMMAND:

                    send_help(BOT_CONFIG, pmessage)
                else:

                    process_modules(chat_id, chat_title, user_id, user_title, message_text)

    def is_this_service_command(self, pmessage):
        """Обработка команд бота."""

        result = True
        command = pmessage.text[1:].lower()
        user_title = pmessage.from_user.first_name
        user_name = pmessage.from_user.username
        chat_id = pmessage.chat.id
        # *** Это не команда перечитать конфиг?
        if command in CONFIG_COMMANDS:


            # *** Такое запрашивать мож ет только хозяин
            if user_name == self.config["master"]:


                self.robot.send_message(chat_id, "Обновляю конфигурацию.")
                self.load_config()
                self.robot.send_message(chat_id, "Конфигурация обновлена.")
            else:

                self.robot.send_message(chat_id, f"Извини, {user_title}, ты мне не хозяин!")
            # *** Или это команда выхода?
            elif command in EXIT_COMMANDS:

                if user_name == BOT_CONFIG["master"]:

                    self.robot.send_message(chat_id, "Всем пока!")
                    raise CQuitByDemand()
                SoftIceBot.send_message(chat_id, f"Извини, {user_title}, ты мне не хозяин!")
            else:

                result = False
            return result

    def babbler(self):
        """Функция болтуна"""
        minutes = (datetime.now() - self.last_babbler_phrase_time).total_seconds() BABBLER_PERIOD
        # *** Заданный период времени с последней фразы прошел?
        if minutes > 1:

            # *** Бабблер может? болтун может всегда!
            if babbler.can_process(pconfig, pchat_title):

                # *** ... точняк
                message = babbler.babbler(pmessage_text)
                if message is not None:

                    print(" .. ok.", message)
                    if len(message) > 0:

                        SoftIceBot.send_message(pchat_id, message)
                        return True
            return False
            self.last_babbler_phrase_time = datetime.now()

def send_help(pconfig: dict, pmessage):
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
                    pmessage_text):
    """По возможности обработать команду болтуном."""
    # print("*** SI:BBLPR:MSGTX ", pmessage_text)
    if babbler.can_process(pconfig, pchat_title):

        # print("*** SI:BBLPR:")
        # *** ... точняк
        # message = barman.barman(pmessage.text, pmessage.from_user.user_name)
        message = babbler.babbler(pmessage_text)
        # print("*** SI:BBLPR:MSG ", message)
        if message is not None:

            print(" .. ok.", message)
            if len(message) > 0:

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

        message: str
        markup: object = None
        addressant: int
        # *** как пить дать.
        message, addressant, markup = mafiozo.mafiozo(pconfig, pmessage_text, pchat_id,
                                                      puser_id, puser_title)
        if message is not None:

            print(" .. ok.", addressant)
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


def bot_command(pmessage):
    """Обработка команд бота."""

    result = True
    command = pmessage.text[1:].lower()
    user_title = pmessage.from_user.first_name
    user_name = pmessage.from_user.username
    chat_id = pmessage.chat.id

    if command in ["привет", "hi"]:

        SoftIceBot.send_message(chat_id,
                                random.choice(GREETINGS) + ", " + user_title)
    elif command == "тевирп":

        SoftIceBot.send_message(chat_id,
                                'Тевирп! Тсссс.... o_O')
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

            SoftIceBot.send_message(chat_id, "Всем пока!")
            raise CQuitByDemand()
        SoftIceBot.send_message(chat_id, f"Извини, {user_title}, у меня другой хозяин!")
    else:

        result = False
    return result


@SoftIceBot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    """Процедура обработки кнопок мафии"""

    mafiozo_process(BOT_CONFIG, call.message.chat.id, call.message.chat.title,
                    call.from_user.id, call.from_user.username, call.data)


@SoftIceBot.message_handler(func=lambda message: True, content_types=['text'])
def get_text_messages(pmessage):
    """Процедура обработки ввода команд пользователем."""

    global BOT_CONFIG
    word_list: list = func.parse_input(pmessage.text)
    message_text: str = pmessage.text
    user_title: str = pmessage.from_user.first_name
    user_id: int = pmessage.from_user.id
    chat_id: int = pmessage.chat.id
    chat_title: str = pmessage.chat.title
    # print(chat_id, chat_title)
    # *** Проверка разрешенных каналов
    print(f"{user_title} в {chat_title} сказал: ", message_text)
    if chat_title not in BOT_CONFIG[ALLOWED_CHATS]:

        SoftIceBot.send_message(chat_id, "Вашего чата нет в списке разрешённых. Чао!")
        SoftIceBot.leave_chat(chat_id)
        print(f"Караул! Меня похитили и затащили в чат {chat_title}! Но я удрал.")

    # *** В начале строки есть знак команды?
    if message_text[0:1] in COMMAND_SIGNS:

        if not bot_command(pmessage):

            # print(" ", user_title, "says: \"", message_text, "\"", end="")
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
            minutes = (datetime.now() - LAST_BABBLER_PHRASE_TIME).total_seconds() / 10
            # print("*** SI:GTM:SEC ", minutes)
            if minutes > 1:

                babbler_process(BOT_CONFIG, chat_id, chat_title, message_text)  # , user_title
                LAST_BABBLER_PHRASE_TIME = datetime.now()


if __name__ == "__main__":

    babbler.reload_babbling()
    # babbler.reload_babling_ext()
    barman.reload_bar()
    librarian.reload_library()
    try:
        while BOT_STATUS == CONTINUE_RUNNING:
            SoftIceBot.infinity_polling()
            # SoftIceBot.polling(none_stop=NON_STOP, interval=INTERVAL)
            print(f"Bot status = {BOT_STATUS}")

    except CQuitByDemand as ex:

        print(ex.message)
        BOT_STATUS = QUIT_BY_DEMAND
        sys.exit()
        # SoftIceBot.stop_polling()
