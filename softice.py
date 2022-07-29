#! /usr/bin/python3
# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Бот для Телеграмма"""

from sys import platform
import json
import telebot
from telebot import apihelper
from datetime import datetime

import database
import babbler
import barman
import statistic
import theolog
import librarian
import meteorolog

LINUX_DATA_FOLDER_KEY: str = "linux_data_folder"
WINDOWS_DATA_FOLDER_KEY: str = "windows_data_folder"
ENABLED_IN_CHATS_KEY: str = "allowed_chats"
BOT_NAME: str = "SoftIceBot"
COMMAND_SIGNS: str = "/!."
CONFIG_FILE_NAME: str = "config.json"
CONFIG_COMMANDS: list = ["конфиг", "config"]  # !
EXIT_COMMANDS: list = ["прощай", "bye", "!!"]  # !
HELP_COMMANDS: list = ["помощь", "help"]  # !
HELP_MESSAGE: str = "В настоящий момент я понимаю только следующие команды: \n"
NON_STOP: bool = True
POLL_INTERVAL: int = 0
CONTINUE_RUNNING: int = 0
QUIT_BY_DEMAND: int = 1
TOKEN_KEY: str = "token"  # !
BOT_STATUS: int = CONTINUE_RUNNING


# ToDo: реализовать отработку команды reload по всем модулям
# ToDo: и чтоб в каждом модуле шла проверка на то,
#       что команда отдана хозяином.
#  barman, librarian,


class CQuitByDemand(Exception):
    """Исключение выхода."""

    def __init__(self):
        self.message = "Выход по требованию..."
        super().__init__(self.message)


def decode_message(pmessage):
    """Возвращает куски сообщения, $#^^^!!!! """
    return pmessage.text, \
        pmessage.text[1:].lower(), \
        pmessage.chat.id, \
        pmessage.chat.title, \
        pmessage.from_user.username, \
        pmessage.from_user.first_name


# pylint: disable=too-many-instance-attributes
# а что еще делать???
class CSoftIceBot:
    """Универсальный бот для Телеграмма."""

    def __init__(self):
        """Конструктор класса."""
        super().__init__()
        self.config: dict = {}
        self.load_config()
        # *** Нужно ли работать через прокси?
        if self.config["proxy"]:

            apihelper.proxy = {'https': self.config["proxy"]}
        # *** Создаём собственно бота.
        self.robot: telebot.TeleBot = telebot.TeleBot(self.config[TOKEN_KEY])
        self.bot_status: int = CONTINUE_RUNNING
        self.exiting: bool = False
        self.message_text: str = ""
        self.last_chat_id: int = -1
        # *** Где у нас данные лежат?
        if platform in ("linux", "linux2"):

            self.data_path: str = self.config[LINUX_DATA_FOLDER_KEY]
        else:

            self.data_path: str = self.config[WINDOWS_DATA_FOLDER_KEY]
        # *** Открываем БД
        self.database: database.CDataBase = database.CDataBase(self.config, self.data_path)
        if not self.database.exists():

            # *** А нету ещё БД, создавать треба.
            self.database.create()
        # *** Поехали создавать работников =)
        self.barman: barman.CBarman = barman.CBarman(self.config, self.data_path)
        self.babbler: babbler.CBabbler = babbler.CBabbler(self.config, self.data_path)
        self.librarian: librarian.CLibrarian = librarian.CLibrarian(self.config, self.data_path)
        self.meteorolog: meteorolog.CMeteorolog = meteorolog.CMeteorolog(self.config)
        self.statistic: statistic.CStatistic = statistic.CStatistic(self.config, self.database)
        self.theolog: theolog.CTheolog = theolog.CTheolog(self.config, self.data_path)

        # *** Обработчик сообщений
        @self.robot.message_handler(content_types=['text'])
        def process_message(pmessage):
            """Обработчик сообщений."""

            self.message_text, command, chat_id, chat_title, user_name, user_title = \
                decode_message(pmessage)
            answer: str = ""
            # *** Проверим, легитимный ли этот чат
            if self.is_this_chat_enabled(chat_title):

                message_date = pmessage.date
                # *** Да, вполне легитимный. Сообщение не протухло?
                if (datetime.now() - datetime.fromtimestamp(message_date)).total_seconds() < 60:

                    # ***  Боту дали команду?
                    if self.message_text[0:1] in COMMAND_SIGNS:

                        if not self.process_command(command, chat_id, chat_title,
                                                    {"name": user_name, "title": user_title}):

                            # *** Нет. Ну и пусть работники разбираются....
                            answer = self.process_modules(chat_id, chat_title, user_name,
                                                          user_title)
                            if answer:

                                self.last_chat_id = chat_id
                                # self.robot.send_message(chat_id, answer)
                    else:

                        # *** Нет, не команда.. Проапдейтим базу статистика,
                        #     если в этом чате статистик разрешен
                        if self.statistic.is_enabled(chat_title):

                            self.statistic.save_message(pmessage)
                        # *** Болтуну есть что ответить?
                        answer = self.babbler.talk(chat_title, self.message_text)
                    if answer:

                        self.last_chat_id = chat_id
                        self.robot.send_message(chat_id, answer)
                else:

                    # *** Бота привели на чужой канал. Выходим.
                    answer = "Вашего чата нет в списке разрешённых. Чао!"
                    self.robot.send_message(chat_id, "Вашего чата нет в списке разрешённых. Чао!")
                    self.robot.leave_chat(chat_id)
                    print(f"Караул! Меня похитили и затащили в чат {chat_title}! Но я удрал.")

    def is_master(self, puser_name: str) -> bool:
        """Проверяет, хозяин ли отдал команду."""
        return puser_name == self.config["master"]

    def is_this_chat_enabled(self, pchat_title: str):
        """Проверяет, находится ли данный чат в списке разрешенных."""
        assert pchat_title is not None, \
            "Assert: [softice.check_is_this_chat_enabled] " \
            "No <pchat_title> parameter specified!"
        return pchat_title in self.config[ENABLED_IN_CHATS_KEY]

    def poll(self):
        """Функция опроса ботом телеграмма."""
        try:

            while self.bot_status == CONTINUE_RUNNING:

                self.robot.polling(none_stop=NON_STOP, interval=POLL_INTERVAL)
                print(f"Bot status = {BOT_STATUS}")

        except CQuitByDemand as ex:

            print(ex.message)
            self.bot_status = QUIT_BY_DEMAND
            self.robot.stop_polling()

    def process_command(self, pcommand: str, pchat_id: int, pchat_title: str,
                        puser: dict):
        """Обрабатывает системные команды"""
        result: bool = False
        # *** Да, команду. Это команда перезагрузки конфига?
        if pcommand in CONFIG_COMMANDS:

            self.reload_config(pchat_id, puser["name"], puser["title"])
            result = True
        # *** Нет. Запросили выход?
        elif pcommand in EXIT_COMMANDS:

            self.stop_working(pchat_id, puser["name"], puser["title"])
            result = True
        # *** Опять нет. Запросили помощь?
        elif pcommand in HELP_COMMANDS:

            answer: str = self.send_help(pchat_title)
            self.robot.send_message(pchat_id, answer)
            result = True
        return result

    def send_help(self, pchat_title: str):
        """Проверяет, не была ли запрошена подсказка."""
        assert pchat_title is not None, \
            "Assert: [softice.is_help_command_queried] " \
            "No <pchat_title> parameter specified!"
        # *** Собираем ответы работников на запрос помощи
        answer: str = f"""\n{self.barman.get_hint(pchat_title)}
                          \n{self.librarian.get_hint(pchat_title)}
                          \n{self.meteorolog.get_hint(pchat_title)}
                          \n{self.statistic.get_hint(pchat_title)}
                          \n{self.theolog.get_hint(pchat_title)}""".strip()
        # *** Если ответы есть, отвечаем на запрос
        if answer:

            return HELP_MESSAGE + answer
        return answer

    def stop_working(self, pchat_id: int, puser_name: str, puser_title: str):
        """Проверка, вдруг была команда выхода."""
        assert pchat_id is not None, \
            "Assert: [softice.is_quit_command_queried] " \
            "No <pchat_id> parameter specified!"
        assert puser_title is not None, \
            "Assert: [softice.is_quit_command_queried] " \
            "No <puser_title> parameter specified!"
        if self.is_master(puser_name):

            self.robot.send_message(pchat_id, "Всем пока!")
            self.exiting = True
            raise CQuitByDemand()
        self.robot.send_message(pchat_id, f"Извини, {puser_title}, ты мне не хозяин!")

    def reload_config(self, pchat_id: int, puser_name: str, puser_title: str):
        """Проверяет, не является ли поданная команда командой перезагрузки конфигурации."""
        assert pchat_id is not None, \
            "Assert: [softice.is_reload_config_command_queried] " \
            "No <pchat_id> parameter specified!"
        assert puser_title is not None, \
            "Assert: [softice.is_reload_config_command_queried] " \
            "No <puser_title> parameter specified!"
        # *** Такое запрашивать может только хозяин
        if self.is_master(puser_name):

            self.robot.send_message(pchat_id, "Обновляю конфигурацию.")
            self.load_config()
            self.robot.send_message(pchat_id, "Конфигурация обновлена.")
        else:

            self.robot.send_message(pchat_id, f"Извини, {puser_title}, ты мне не хозяин!")

    def load_config(self):
        """Загружает конфигурацию из JSON."""
        with open(CONFIG_FILE_NAME, "r", encoding="utf-8") as json_file:

            self.config = json.load(json_file)

    def process_modules(self, pchat_id: int, pchat_title: str,
                        puser_name: str, puser_title: str):
        """Пытается обработать команду различными модулями."""
        assert pchat_title is not None, \
            "Assert: [softice.process_modules] No <pchat_title> parameter specified!"
        assert puser_title is not None, \
            "Assert: [softice.process_modules] No <puser_title> parameter specified!"
        # *** Проверим, не запросил ли пользователь что-то у бармена...
        answer: str = self.barman.barman(pchat_title, self.message_text, puser_title).strip()
        if not answer:

            # *** ... или у теолога...
            answer = self.theolog.theolog(pchat_title, self.message_text).strip()
        if not answer:

            # *** ... или у библиотекаря...
            answer = self.librarian.librarian(pchat_title, puser_name,
                                              puser_title, self.message_text).strip()
        if not answer:

            # *** ... или у метеоролога...
            answer = self.meteorolog.meteorolog(pchat_title, self.message_text).strip()
        if not answer:

            # *** ... или у статистика...
            answer = self.statistic.statistic(pchat_id, pchat_title,
                                              puser_title, self.message_text).strip()
        if not answer:

            answer = self.babbler.babbler(pchat_title, self.message_text).strip()
        if not answer:

            # *** Незнакомая команда.
            print(" .. fail.")
        return answer


# @self.robot.callback_query_handler(func=lambda call: True)
# def callback_inline(call):
#     """Процедура обработки кнопок мафии"""
#
#     mafiozo_process(BOT_CONFIG, call.message.chat.id, call.message.chat.title,
#                     call.from_user.id, call.from_user.username, call.data)

if __name__ == "__main__":

    SofticeBot: CSoftIceBot = CSoftIceBot()
    try:

        SofticeBot.poll()
    finally:

        if not SofticeBot.exiting:

            if SofticeBot.last_chat_id >= 0:
                SofticeBot.robot.send_message(SofticeBot.last_chat_id,
                                              "Ой, матушки, падаю!")
