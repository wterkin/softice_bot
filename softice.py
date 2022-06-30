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
        # !!! barman.reload_bar()
        librarian.reload_library()
        self.barman = barman.CBarman(self.config)
        self.babbler = babbler.CBabbler(self.config)
        self.theolog = theolog.CTheolog(self.config)
        @self.robot.message_handler(content_types=['text'])
        def process_message(pmessage):
            """Обработчик сообщений."""

            message_text: str = pmessage.text
            # print("*** ", message_text)
            command = pmessage.text[1:].lower()
            chat_id: int = pmessage.chat.id
            chat_title: str = pmessage.chat.title
            user_name = pmessage.from_user.username
            user_title: str = pmessage.from_user.first_name
            user_id: int = pmessage.from_user.id

            # *** Проверим, легитимный ли этот чат
            if self.check_is_this_chat_enabled(chat_id, chat_title):

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

                    message = self.babbler.babbler(chat_title, message_text)
                    if len(message) > 0:

                        self.robot.send_message(chat_id, message)

    def call_librarian(self, pchat_id: int, pchat_title: str,
                       puser_title, pmessage_text):
        """ Если это команда библиотекаря... """
        assert pchat_id is not None, \
            "Assert: [softice.call_librarian] " \
            "No <pchat_id> parameter specified!"
        assert pchat_title is not None, \
            "Assert: [softice.call_librarian] " \
            "No <pchat_title> parameter specified!"
        assert puser_title is not None, \
            "Assert: [softice.call_librarian] No <puser_title> parameter specified!"
        assert pmessage_text is not None, \
            "Assert: [softice.call_librarian] " \
            "No <pmessage_text> parameter specified!"

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
                     puser_id: int, puser_title: str, pmessage_text: str):
        """По возможности обработать команду мафиози"""
        assert pchat_id is not None, \
            "Assert: [softice.call_mafiozo] " \
            "No <pchat_id> parameter specified!"
        assert pchat_title is not None, \
            "Assert: [softice.call_mafiozo] " \
            "No <pchat_title> parameter specified!"
        assert puser_id is not None, \
            "Assert: [softice.call_mafiozo] No <puser_id> parameter specified!"
        assert puser_title is not None, \
            "Assert: [softice.call_mafiozo] No <puser_title> parameter specified!"
        assert pmessage_text is not None, \
            "Assert: [softice.call_mafiozo] " \
            "No <pmessage_text> parameter specified!"

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
        assert pchat_id is not None, \
            "Assert: [softice.call_meteorolog] " \
            "No <pchat_id> parameter specified!"
        assert pchat_title is not None, \
            "Assert: [softice.call_meteorolog] " \
            "No <pchat_title> parameter specified!"
        assert pmessage_text is not None, \
            "Assert: [softice.call_meteorolog] " \
            "No <pmessage_text> parameter specified!"
        if meteorolog.can_process(self.config, pchat_title, pmessage_text):

            # *** как пить дать.
            message = meteorolog.meteorolog(pmessage_text)
            if message is not None:
                print(" Meteorolog answers.")
                self.robot.send_message(pchat_id, message)
                return True
        return False

    def check_is_this_chat_enabled(self, pchat_id: int, pchat_title: str):
        """Проверяет, находится ли данный чат в списке разрешенных."""
        assert pchat_id is not None, \
            "Assert: [softice.check_is_this_chat_enabled] " \
            "No <pchat_id> parameter specified!"
        assert pchat_title is not None, \
            "Assert: [softice.check_is_this_chat_enabled] " \
            "No <pchat_title> parameter specified!"

        if pchat_title not in self.config[ALLOWED_CHATS]:

            self.robot.send_message(pchat_id, "Вашего чата нет в списке разрешённых. Чао!")
            self.robot.leave_chat(pchat_id)
            print(f"Караул! Меня похитили и затащили в чат {pchat_title}! Но я удрал.")
            return False
        return True

    def is_help_command_queried(self, pcommand: str,
                                pchat_id: int, pchat_title: str):
        """Проверяет, не была ли запрошена подсказка."""
        assert pcommand is not None, \
            "Assert: [softice.is_help_command_queried] " \
            "No <pchat_title> parameter specified!"
        assert pchat_id is not None, \
            "Assert: [softice.is_help_command_queried] " \
            "No <pchat_id> parameter specified!"
        assert pchat_title is not None, \
            "Assert: [softice.is_help_command_queried] " \
            "No <pchat_title> parameter specified!"

        if pcommand in HELP_COMMANDS:

            barman_message = self.barman.get_hint(pchat_title)
            librarian_message = librarian.get_help(self.config, pchat_title)
            meteorolog_message = meteorolog.help()
            theolog_message = self.theolog.get_hint(pchat_title)  #
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
        assert pcommand is not None, \
            "Assert: [softice.is_quit_command_queried] " \
            "No <pchat_title> parameter specified!"
        assert pchat_id is not None, \
            "Assert: [softice.is_quit_command_queried] " \
            "No <pchat_id> parameter specified!"
        assert puser_name is not None, \
            "Assert: [softice.is_quit_command_queried] " \
            "No <puser_name> parameter specified!"
        assert puser_title is not None, \
            "Assert: [softice.is_quit_command_queried] " \
            "No <puser_title> parameter specified!"
        result = False
        if pcommand in EXIT_COMMANDS:

            if puser_name == self.config["master"]:

                self.robot.send_message(pchat_id, "Всем пока!")
                raise CQuitByDemand()
            self.robot.send_message(pchat_id, f"Извини, {puser_title}, ты мне не хозяин!")
        return result

    def is_reload_config_command_queried(self, pcommand: str, pchat_id: int,
                                         puser_name: str, puser_title: str):
        """Проверяет, не является ли поданная команда командой перезагрузки конфигурации."""
        assert pcommand is not None, \
            "Assert: [softice.is_reload_config_command_queried] " \
            "No <pchat_title> parameter specified!"
        assert pchat_id is not None, \
            "Assert: [softice.is_reload_config_command_queried] " \
            "No <pchat_id> parameter specified!"
        assert puser_name is not None, \
            "Assert: [softice.is_reload_config_command_queried] " \
            "No <puser_name> parameter specified!"
        assert puser_title is not None, \
            "Assert: [softice.is_reload_config_command_queried] " \
            "No <puser_title> parameter specified!"

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
            self.robot.stop_polling()

    def process_modules(self, pchat_id: int, pchat_title: str,
                        puser_id: int, puser_title: str,
                        pmessage_text):
        """Пытается обработать команду различными модулями."""
        assert pchat_id is not None, \
            "Assert: [softice.process_modules] No <pchat_id> parameter specified!"
        assert pchat_title is not None, \
            "Assert: [softice.process_modules] No <pchat_title> parameter specified!"
        assert puser_id is not None, \
            "Assert: [softice.process_modules] No <puser_id> parameter specified!"
        assert puser_title is not None, \
            "Assert: [softice.process_modules] No <puser_title> parameter specified!"
        assert pmessage_text is not None, \
            "Assert: [softice.process_modules] No <pmessage_text> parameter specified!"

        # *** Проверим, не запросил ли пользователь что-то у бармена...
        message = self.barman.barman(pchat_title, pmessage_text, puser_title)
        if len(message) > 0:

            self.robot.send_message(pchat_id, message)
        else:

            message = self.theolog.theolog(pchat_title, pmessage_text)
            if len(message) > 0:

                self.robot.send_message(pchat_id, message)
            else:


                if not self.call_librarian(pchat_id,
                                        pchat_title, puser_title, pmessage_text):

                    if not self.call_mafiozo(pchat_id, pchat_title,
                                            puser_id, puser_title, pmessage_text):

                        if not self.call_meteorolog(pchat_id, pchat_title, pmessage_text):

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
