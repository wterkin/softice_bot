#! /usr/bin/python3
# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Бот для Телеграмма"""

import json
from datetime import datetime
import telebot
from telebot import apihelper

import babbler
import barman
import theolog
import librarian
import mafiozo
import meteorolog

ALLOWED_CHATS: str = "allowed_chats"
BABBLER_PERIOD: int = 10  # !
BOT_NAME: str = "SoftIceBot"
COMMAND_SIGNS: str = "/!."  # !
CONFIG_FILE_NAME: str = "config.json"
CONFIG_COMMANDS: list = ["конфиг", "config"]  # !
CONTINUE_RUNNING: int = 0
EXIT_COMMANDS: list = ["прощай", "bye"]  # !
HELP_COMMANDS: list = ["помощь", "help"]  # !
HELP_MESSAGE: str = "В настоящий момент я понимаю только следующие команды:"  # !
NON_STOP: bool = True
POLL_INTERVAL: int = 0
QUIT_BY_DEMAND: int = 1
TOKEN_KEY: str = "token"  # !

BOT_STATUS: int = CONTINUE_RUNNING
SMILES: list = ["8)", "=)", ";)", ":)", "%)", "^_^"]


# message.delete()


class CQuitByDemand(Exception):
    """Исключение выхода."""

    def __init__(self):
        self.message = "Выход по требованию..."
        super().__init__(self.message)


# # *** Читаем конфигурацию +++
# with open(CONFIG_FILE_NAME, "r", encoding="utf-8") as config_file:
#     BOT_CONFIG = json.load(config_file)
#
# if BOT_CONFIG["proxy"]:
#     apihelper.proxy = {'https': BOT_CONFIG["proxy"]}
# self.robot = telebot.TeleBot(BOT_CONFIG["token"])


class CSoftIceBot:
    """Универсальный бот для Телеграмма."""

    def __init__(self):
        """Конструктор класса."""
        super().__init__()
        self.config = {}
        self.last_babbler_phrase_time: datetime = datetime.now()
        self.load_config()
        if self.config["proxy"]:
            apihelper.proxy = {'https': self.config["proxy"]}
        self.robot: telebot.TeleBot = telebot.TeleBot(self.config[TOKEN_KEY])
        self.bot_status: int = CONTINUE_RUNNING
        babbler.reload_babbling()
        barman.reload_bar()
        librarian.reload_library()

        @self.robot.message_handler(content_types=['text'])
        def process_message(pmessage):
            """Обработчик сообщений."""

            message_text: str = pmessage.text
            print("*** ", message_text)
            command = pmessage.text[1:].lower()
            chat_id: int = pmessage.chat.id
            chat_title: str = pmessage.chat.title
            user_name = pmessage.from_user.username
            user_title: str = pmessage.from_user.first_name
            user_id: int = pmessage.from_user.id

            # *** Проверим, легитимный ли этот чат
            self.check_is_this_chat_enabled(chat_id, chat_title)

            # *** Боту дали команду?
            if message_text[0:1] in COMMAND_SIGNS:

                if not self.is_reload_config_command_queried(command, chat_id,
                                                             user_name, user_title):

                    if not self.is_quit_command_queried(command, chat_id,
                                                        user_name, user_title):

                        if not self.is_help_command_queried(command, chat_id, chat_title):
                            # *** Передаём введённую команду модулям
                            self.process_modules(chat_id, chat_title, user_id,
                                                 user_title, message_text)
            else:

                self.call_babbler(chat_id, chat_title, message_text)

    def call_babbler(self, pchat_id, pchat_title, pmessage_text):
        """Функция болтуна"""

        minutes = (datetime.now() - self.last_babbler_phrase_time).total_seconds() / BABBLER_PERIOD
        # *** Заданный период времени с последней фразы прошел?
        if minutes > 1:

            # *** Болтун может? болтун может всегда!
            if babbler.can_process(self.config, pchat_title):

                # *** ... точняк
                message = babbler.babbler(pmessage_text)
                if message is not None:

                    print("Babbler answers.", message)
                    if len(message) > 0:
                        self.robot.send_message(pchat_id, message)
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
                self.robot.send_message(pchat_id, message)
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
                self.robot.send_message(pchat_id, message)
                return True
        return False

    def call_mafiozo(self, pchat_id: int, pchat_title: str,
                     puser_id, puser_title: str, pmessage_text):
        """По возможности обработать команду мафиози"""

        if mafiozo.can_process(self.config, pchat_title, pmessage_text):

            message: str
            markup: object
            addressant: int
            # *** как пить дать.
            message, addressant, markup = mafiozo.mafiozo(self.config, pmessage_text, pchat_id,
                                                          puser_id, puser_title)
            if message:

                print("Mafiozo answers.", addressant)
                if markup is None:

                    self.robot.send_message(addressant, message)
                else:

                    self.robot.send_message(addressant, message, reply_markup=markup)
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
                self.robot.send_message(pchat_id, message)
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
                self.robot.send_message(pchat_id, message)
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
                self.robot.send_message(pchat_id, HELP_MESSAGE)

            # *** Помощь от бармена
            if barman_message:
                self.robot.send_message(pchat_id, barman_message)

            # *** Помощь от библиотекаря
            if librarian_message:
                self.robot.send_message(pchat_id, librarian_message)

            # *** Помощь от метеоролога
            if meteorolog_message:
                self.robot.send_message(pchat_id, meteorolog_message)

            # *** Помощь от теолога
            if theolog_message:
                self.robot.send_message(pchat_id, theolog_message)

    def is_quit_command_queried(self, pcommand: str, pchat_id: int,
                                puser_name: str, puser_title: str):
        """Проверка, вдруг была команда выхода."""

        result = False
        if pcommand in EXIT_COMMANDS:

            if puser_name == self.config["master"]:
                self.robot.send_message(pchat_id, "Всем пока!")
                result = True
                raise CQuitByDemand()
            self.robot.send_message(pchat_id, f"Извини, {puser_title}, ты мне не хозяин!")
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
                # self.robot.infinity_polling()
                self.robot.polling(none_stop=NON_STOP, interval=POLL_INTERVAL)
                print(f"Bot status = {BOT_STATUS}")

        except CQuitByDemand as ex:

            print(ex.message)
            self.bot_status = QUIT_BY_DEMAND
            # self.robot.stop_polling()

    def process_modules(self, pchat_id: int, pchat_title: str,
                        puser_id: int, puser_title: str,
                        pmessage_text):
        """Пытается обработать команду различными модулями."""
        # *** Проверим, не запросил ли пользователь что-то у бармена...
        if not self.call_barman(pchat_id, pchat_title, puser_title, pmessage_text):

            if not self.call_librarian(pchat_id,
                                       pchat_title, puser_title, pmessage_text):

                if not self.call_mafiozo(pchat_id, pchat_title,
                                         puser_id, puser_title, pmessage_text):

                    if not self.call_meteorolog(pchat_id, pchat_title, pmessage_text):

                        if not self.call_theolog(pchat_id, pchat_title, pmessage_text):
                            print(" .. fail.")


# @self.robot.callback_query_handler(func=lambda call: True)
# def callback_inline(call):
#     """Процедура обработки кнопок мафии"""
#
#     mafiozo_process(BOT_CONFIG, call.message.chat.id, call.message.chat.title,
#                     call.from_user.id, call.from_user.username, call.data)

if __name__ == "__main__":
    SofticeBot = CSoftIceBot()
    SofticeBot.poll()
