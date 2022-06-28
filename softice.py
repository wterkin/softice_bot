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

COMMAND_SIGNS: str = "/!."  # !
HELP_COMMAND: str = "help"  # !
HELP_MESSAGE: str = "В настоящий момент я понимаю только следующие команды:"  # !

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
EXIT_COMMANDS: list = ["прощай", "bye"]  # !
HELP_COMMANDS: list = ["помощь", "help"]  # !
BABBLER_PERIOD: int = 10  # !


# message.delete()


class CQuitByDemand(Exception):
    """Исключение выхода."""

    def __init__(self):
        self.message = "Выход по требованию..."
        super().__init__(self.message)


# *** Читаем конфигурацию +++
with open(CONFIG_FILE_NAME, "r", encoding="utf-8") as config_file:
    BOT_CONFIG = json.load(config_file)

if BOT_CONFIG["proxy"]:
    apihelper.proxy = {'https': BOT_CONFIG["proxy"]}
SoftIceBot = telebot.TeleBot(BOT_CONFIG["token"])


class CSoftIceBot:
    """Универсальный бот для Телеграмма."""

    def __init__(self):
        """Конструктор класса."""
        super().__init__()
        self.config = {}
        self.last_babbler_phrase_time: datetime = datetime.now()
        self.load_config()
        self.robot: telebot.TeleBot = telebot.TeleBot(self.config[TOKEN_KEY])
        self.bot_status: int = CONTINUE_RUNNING
        babbler.reload_babbling()
        barman.reload_bar()
        librarian.reload_library()

        # @self.robot.message_handler(commands=["start"])
        @self.robot.message_handler(content_types=['text'])
        def process_message(pmessage):
            """Обработчик сообщений."""

            message_text: str = pmessage.text
            # word_list: list = func.parse_input(pmessage.text)
            print("*** ", message_text)
            command = pmessage.text[1:].lower()
            chat_id: int = pmessage.chat.id
            chat_title: str = pmessage.chat.title
            user_name = pmessage.from_user.username
            user_title: str = pmessage.from_user.first_name
            user_id: int = pmessage.from_user.id

            # *** Проверим, легитимный ли этот чата
            self.check_is_this_chat_enabled(chat_id, chat_title)

            # *** Боту дали команду?
            if message_text[0:1] in COMMAND_SIGNS:

                if not self.is_reload_config_command_queried(command, chat_id,
                                                             user_name, user_title):

                    if not self.is_quit_command_queried(command, chat_id,
                                                        user_name, user_title):

                        if not self.is_help_command_queried(command, chat_id, chat_title):
                            # *** Передаём введённую команду модулям
                            self.process_modules(chat_id, chat_title, user_id, user_title, message_text)
            else:

                self.call_babbler(chat_id, chat_title, message_text)

    def call_babbler(self, pchat_id, pchat_title, pmessage_text):
        """Функция болтуна"""
        print("*****************")
        minutes = (datetime.now() - self.last_babbler_phrase_time).total_seconds() / BABBLER_PERIOD
        # *** Заданный период времени с последней фразы прошел?
        if minutes > 1:

            # *** Бабблер может? болтун может всегда!
            if babbler.can_process(self.config, pchat_title):

                # *** ... точняк
                message = babbler.babbler(pmessage_text)
                if message is not None:

                    print("Babbler answers.", message)
                    if len(message) > 0:
                        SoftIceBot.send_message(pchat_id, message)
                        return True
            self.last_babbler_phrase_time = datetime.now()
        return False

    def call_barman(self, pchat_id: int, pchat_title: str,
                    puser_title, pmessage_text):
        """По возможности обработать команду барменом."""

        if barman.can_process(self.config, pchat_title, pmessage_text):

            # *** ... точняк
            message = barman.barman(pmessage_text, puser_title)
            if message is not None:
                print("Barman answers.")
                SoftIceBot.send_message(pchat_id, message)
                return True
        return False

    def call_librarian(self, pchat_id: int, pchat_title: str,
                       puser_title, pmessage_text):
        """ Если это команда библиотекаря... """
        if librarian.can_process(self.config, pchat_title, pmessage_text):

            # *** как пить дать.
            message = librarian.librarian(self.config,
                                          puser_title,
                                          pmessage_text)
            if message is not None:
                print("Librarian answers.")
                SoftIceBot.send_message(pchat_id, message)
                return True
        return False

    def call_mafiozo(self, pchat_id: int, pchat_title: str,
                     puser_id, puser_title: str, pmessage_text):
        """По возможности обработать команду мафиози"""

        if mafiozo.can_process(self.config, pchat_title, pmessage_text):

            message: str
            markup: object = None
            addressant: int
            # *** как пить дать.
            message, addressant, markup = mafiozo.mafiozo(self.config, pmessage_text, pchat_id,
                                                          puser_id, puser_title)
            if message is not None:

                print("Mafiozo answers.", addressant)
                if markup is None:

                    SoftIceBot.send_message(addressant, message)
                else:

                    SoftIceBot.send_message(addressant, message, reply_markup=markup)
                return True
        return False

    def call_meteorolog(self, pchat_id: int, pchat_title: str,
                        pmessage_text: str):
        """По возможности обработать команду метеорологом"""
        if meteorolog.can_process(self.config, pchat_title, pmessage_text):

            # *** как пить дать.
            message = meteorolog.meteorolog(pmessage_text)
            if message is not None:
                print(" Meteorolog answers.")
                SoftIceBot.send_message(pchat_id, message)
                return True
        return False

    def call_theolog(self, pchat_id: int, pchat_title: str,
                     pmessage_text):
        """По возможности обработать команду теологом"""

        if theolog.can_process(self.config, pchat_title, pmessage_text):

            # *** как пить дать.
            message = theolog.theolog(pmessage_text)
            if message is not None:
                print("Theolog answers.")
                SoftIceBot.send_message(pchat_id, message)
                return True
        return False

    def check_is_this_chat_enabled(self, pchat_id: int, pchat_title: str):
        """Проверяет, находится ли данный чат в списке разрешенных."""
        if pchat_title not in self.config[ALLOWED_CHATS]:
            self.robot.send_message(pchat_id, "Вашего чата нет в списке разрешённых. Чао!")
            self.robot.leave_chat(pchat_id)
            print(f"Караул! Меня похитили и затащили в чат {pchat_title}! Но я удрал.")

    def is_help_command_queried(self, pcommand: str,
                                pchat_id: int, pchat_title: str):
        """Проверяет, не была ли запрошена подсказка."""
        if pcommand in HELP_COMMANDS:
            barman_message = barman.get_help(self.config, pchat_title)
            librarian_message = librarian.get_help(self.config, pchat_title)
            meteorolog_message = meteorolog.help()
            theolog_message = theolog.get_help(self.config, pchat_title)
            if (barman_message or
               librarian_message or
               meteorolog_message or
               theolog_message):
                SoftIceBot.send_message(pchat_id, HELP_MESSAGE)

            # *** Помощь от бармена
            if barman_message:
                SoftIceBot.send_message(pchat_id, barman_message)

            # *** Помощь от библиотекаря
            if librarian_message:
                SoftIceBot.send_message(pchat_id, librarian_message)

            # *** Помощь от метеоролога
            if meteorolog_message:
                SoftIceBot.send_message(pchat_id, meteorolog_message)

            # *** Помощь от теолога
            if theolog_message:
                SoftIceBot.send_message(pchat_id, theolog_message)

    def is_quit_command_queried(self, pcommand: str, pchat_id: int,
                                puser_name: str, puser_title: str):
        """Проверка, вдруг была команда выхода."""

        result = False
        if pcommand in EXIT_COMMANDS:

            if puser_name == BOT_CONFIG["master"]:
                self.robot.send_message(pchat_id, "Всем пока!")
                result = True
                raise CQuitByDemand()
            SoftIceBot.send_message(pchat_id, f"Извини, {puser_title}, ты мне не хозяин!")
        return result

    def is_reload_config_command_queried(self, pcommand: str, pchat_id: int,
                                         puser_name: str, puser_title: str):
        """Проверяет, не является ли поданная команда командой перезагрузки конфигурации."""
        result = False
        if pcommand in CONFIG_COMMANDS:

            # *** Такое запрашивать может только хозяин
            if puser_name == self.config["master"]:

                self.robot.send_message(pchat_id, "Обновляю конфигурацию.")
                self.load_config()
                self.robot.send_message(pchat_id, "Конфигурация обновлена.")
                result = True
            else:

                self.robot.send_message(pchat_id, f"Извини, {puser_title}, ты мне не хозяин!")
        return result

    def load_config(self):
        """Загружает конфигурацию из JSON."""
        with open(CONFIG_FILE_NAME, "r", encoding="utf-8") as json_file:
            self.config = json.load(json_file)

    def poll(self):
        """Функция опроса ботом телеграмма."""
        try:
            while self.bot_status == CONTINUE_RUNNING:
                # SoftIceBot.infinity_polling()
                self.robot.polling(none_stop=NON_STOP, interval=INTERVAL)
                print(f"Bot status = {BOT_STATUS}")

        except CQuitByDemand as ex:

            print(ex.message)
            self.bot_status = QUIT_BY_DEMAND
            # sys.exit()
            # SoftIceBot.stop_polling()

    def process_modules(self, pchat_id: int, pchat_title: str,
                        puser_id: int, puser_title: str,
                        pmessage_text):
        """Пытается обработать команду различными модулями."""
        # *** Проверим, не запросил ли пользователь что-то у бармена...
        print("*** bbbbb")
        if not self.call_barman(pchat_id, pchat_title, puser_title, pmessage_text):

            print("*** lll")
            if not self.call_librarian(pchat_id,
                                       pchat_title, puser_title, pmessage_text):
                if not self.call_mafiozo(pchat_id, pchat_title,
                                         puser_id, puser_title, pmessage_text):
                    print("*** mmm")
                    if not self.call_meteorolog(pchat_id, pchat_title, pmessage_text):

                        print("*** ttt")
                        if not self.call_theolog(pchat_id, pchat_title, pmessage_text):

                            print("*** bbb")
                            if not self.call_babbler(pchat_id, pchat_title, pmessage_text):
                                print(" .. fail.")


NEW_ROBOT = CSoftIceBot()


def send_help(pconfig: dict, pmessage):  # +++
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

    # if command in ["привет", "hi"]:
    #
    #     SoftIceBot.send_message(chat_id,
    #                             random.choice(GREETINGS) + ", " + user_title)
    # if command == "тевирп":
    #
    #     SoftIceBot.send_message(chat_id,
    #                             'Тевирп! Тсссс.... o_O')
    if command in ["конфиг", "config"]:

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


# @SoftIceBot.message_handler(func=lambda message: True, content_types=['text'])
# @NEW_ROBOT.message_handler(func=lambda message: True, content_types=['text'])
def get_text_messages(pmessage):
    """Процедура обработки ввода команд пользователем."""
    # print("### ", pmessage.text)
    # NEW_ROBOT.process_message(pmessage)


"""
    global BOT_CONFIG
    word_list: list = func.parse_input(pmessage.text)
    message_text: str = pmessage.text
    user_title: str = pmessage.from_user.first_name
    user_id: int = pmessage.from_user.id
    chat_id: int = pmessage.chat.id
    chat_title: str = pmessage.chat.title
    # print(chat_id, chat_title)
    # *** Проверка разрешенных каналов
    # print(f"{user_title} в {chat_title} сказал: ", message_text)
    if chat_title not in BOT_CONFIG[ALLOWED_CHATS]:

        # SoftIceBot.send_message(chat_id, "Вашего чата нет в списке разрешённых. Чао!")
        SoftIceBot.leave_chat(chat_id)
        # print(f"Караул! Меня похитили и затащили в чат {chat_title}! Но я удрал.")

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
"""

if __name__ == "__main__":
    # ------------------------
    """
    babbler.reload_babbling()
    # babbler.reload_babling_ext()
    barman.reload_bar()
    librarian.reload_library()
    try:
        while BOT_STATUS == CONTINUE_RUNNING:
            # SoftIceBot.infinity_polling()
            SoftIceBot.polling(none_stop=NON_STOP, interval=INTERVAL)
            print(f"Bot status = {BOT_STATUS}")

    except CQuitByDemand as ex:

        print(ex.message)
        BOT_STATUS = QUIT_BY_DEMAND
        sys.exit()
        # SoftIceBot.stop_polling()
    # -----------------------
    """
    NEW_ROBOT.poll()
