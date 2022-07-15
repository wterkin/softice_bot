#! /usr/bin/python3
# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Бот для Телеграмма"""

from sys import platform
import json
import telebot
from telebot import apihelper

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
CONTINUE_RUNNING: int = 0
EXIT_COMMANDS: list = ["прощай", "bye", "!!"]  # !
HELP_COMMANDS: list = ["помощь", "help"]  # !
HELP_MESSAGE: str = "В настоящий момент я понимаю только следующие команды:"  # !
NON_STOP: bool = True
POLL_INTERVAL: int = 0
QUIT_BY_DEMAND: int = 1
TOKEN_KEY: str = "token"  # !
BOT_STATUS: int = CONTINUE_RUNNING
SMILES: list = ["8)", "=)", ";)", ":)", "%)", "^_^"]


# ToDo: реализовать отработку команды reload по всем модулям
# ToDo: и чтоб в каждом модуле шла проверка на то,
#       что команда отдана хозяином.


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
        self.config: dict = {}
        self.load_config()
        # *** Нужно ли работать через прокси?
        if self.config["proxy"]:
            apihelper.proxy = {'https': self.config["proxy"]}
        # *** Создаём собственно бота.
        self.robot: telebot.TeleBot = telebot.TeleBot(self.config[TOKEN_KEY])
        self.bot_status: int = CONTINUE_RUNNING
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

            message_text: str = pmessage.text
            command: str = pmessage.text[1:].lower()
            chat_id: int = pmessage.chat.id
            chat_title: str = pmessage.chat.title
            user_name: str = pmessage.from_user.username
            user_title: str = pmessage.from_user.first_name
            answer: str = ""
            # *** Проверим, легитимный ли этот чат
            if self.is_this_chat_enabled(chat_title):

                # *** Да, вполне легитимный. Боту дали команду?
                if message_text[0:1] in COMMAND_SIGNS:

                    # *** Да, команду. Это команда перезагрузки конфига?
                    if command in CONFIG_COMMANDS:

                        self.reload_config(chat_id, user_name, user_title)
                        return
                    # *** Нет. Запросили выход?
                    if command in EXIT_COMMANDS:

                        self.stop_working(chat_id, user_name, user_title)
                        return
                    # *** Опять нет. Запросили помощь?
                    if command in HELP_COMMANDS:

                        self.send_help(chat_id, chat_title)
                        return
                    # *** Нет. Ну и пусть работники разбираются....
                    answer = self.process_modules(chat_title, user_name,
                                                  user_title, message_text)
                    if len(answer) > 0:
                        self.robot.send_message(chat_id, answer)

                else:

                    # *** Нет, не команда.. Сохраним введённую фразу в базу,
                    #     если в этом чате статистик разрешен
                    if self.statistic.is_enabled(chat_title):
                        self.statistic.save_message(pmessage)
                    # *** Болтуну есть что ответить?
                    answer = self.babbler.babbler(chat_title, message_text)
                    if len(answer) > 0:

                        self.robot.send_message(chat_id, answer)
            else:

                self.robot.send_message(chat_id, "Вашего чата нет в списке разрешённых. Чао!")
                self.robot.leave_chat(chat_id)
                print(f"Караул! Меня похитили и затащили в чат {chat_title}! Но я удрал.")
    
    def is_this_chat_enabled(self, pchat_title: str):
        """Проверяет, находится ли данный чат в списке разрешенных.
        >>> self.is_this_chat_enabled('Ботовка')
        True
        >>> self.is_this_chat_enabled('Test1')
        False
        """
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

    def send_help(self, pchat_id: int, pchat_title: str):
        """Проверяет, не была ли запрошена подсказка.
        # >>> len(self.send_help(-583831606, 'Ботовка')) > 0
        True
        #>>> len(self.send_help(0, 'Test1')) > 0
        False
        """
        assert pchat_id is not None, \
            "Assert: [softice.is_help_command_queried] " \
            "No <pchat_id> parameter specified!"
        assert pchat_title is not None, \
            "Assert: [softice.is_help_command_queried] " \
            "No <pchat_title> parameter specified!"
        # *** Собираем ответы работников на запрос помощи
        answer: str = f"""\n{self.barman.get_hint(pchat_title)}
                          \n{self.librarian.get_hint(pchat_title)}
                          \n{self.meteorolog.get_hint(pchat_title)}
                          \n{self.statistic.get_hint(pchat_title)}
                          \n{self.theolog.get_hint(pchat_title)}"""
        # *** Если ответы есть, отвечаем на запрос
        if len(answer) > 0:
            self.robot.send_message(pchat_id, HELP_MESSAGE + answer)

    def stop_working(self, pchat_id: int, puser_name: str, puser_title: str):
        """Проверка, вдруг была команда выхода."""
        assert pchat_id is not None, \
            "Assert: [softice.is_quit_command_queried] " \
            "No <pchat_id> parameter specified!"
        assert puser_title is not None, \
            "Assert: [softice.is_quit_command_queried] " \
            "No <puser_title> parameter specified!"
        if puser_name == self.config["master"]:
            self.robot.send_message(pchat_id, "Всем пока!")
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
        if puser_name == self.config["master"]:

            self.robot.send_message(pchat_id, "Обновляю конфигурацию.")
            self.load_config()
            self.robot.send_message(pchat_id, "Конфигурация обновлена.")
        else:

            self.robot.send_message(pchat_id, f"Извини, {puser_title}, ты мне не хозяин!")

    def load_config(self):
        """Загружает конфигурацию из JSON."""
        with open(CONFIG_FILE_NAME, "r", encoding="utf-8") as json_file:
            self.config = json.load(json_file)

    def process_modules(self, pchat_title: str,
                        puser_name: str, puser_title: str,
                        pmessage_text: str):
        """Пытается обработать команду различными модулями."""
        assert pchat_title is not None, \
            "Assert: [softice.process_modules] No <pchat_title> parameter specified!"
        assert puser_title is not None, \
            "Assert: [softice.process_modules] No <puser_title> parameter specified!"
        assert pmessage_text is not None, \
            "Assert: [softice.process_modules] No <pmessage_text> parameter specified!"
        answer: str
        # *** Проверим, не запросил ли пользователь что-то у бармена...
        answer = self.barman.barman(pchat_title, pmessage_text, puser_title)
        if len(answer) == 0:

            answer = self.theolog.theolog(pchat_title, pmessage_text)
            if len(answer) == 0:

                answer = self.librarian.librarian(pchat_title, puser_name,
                                                  puser_title, pmessage_text)
                if len(answer) == 0:

                    answer = self.meteorolog.meteorolog(pchat_title, pmessage_text)
                    if len(answer) == 0:
                        print(" .. fail.")
        return answer


# @self.robot.callback_query_handler(func=lambda call: True)
# def callback_inline(call):
#     """Процедура обработки кнопок мафии"""
#
#     mafiozo_process(BOT_CONFIG, call.message.chat.id, call.message.chat.title,
#                     call.from_user.id, call.from_user.username, call.data)

if __name__ == "__main__":
    SofticeBot = CSoftIceBot()
    SofticeBot.poll()
