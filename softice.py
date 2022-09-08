#! /usr/bin/python3
# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Бот для Телеграмма"""
from datetime import date
import sys
from sys import platform
from datetime import datetime
import json
import telebot
from requests import ReadTimeout
from telebot import apihelper

import database
import babbler
import barman
import bellringer
import librarian
import meteorolog
import moderator
import statistic
import stargazer
import theolog
import tomcat

LINUX_DATA_FOLDER_KEY: str = "linux_data_folder"
WINDOWS_DATA_FOLDER_KEY: str = "windows_data_folder"
ENABLED_IN_CHATS_KEY: str = "allowed_chats"
BOT_NAME: str = "SoftIceBot"
COMMAND_SIGN: str = "!"
CONFIG_FILE_NAME: str = "config.json"
CONFIG_COMMANDS: list = ["конфиг", "config"]  # !
EXIT_COMMANDS: list = ["прощай", "bye", "!!"]  # !
HELP_COMMANDS: list = ["помощь", "help"]  # !
HELP_MESSAGE: str = "В настоящий момент я понимаю только следующие группы команд: \n"
NON_STOP: bool = True
POLL_INTERVAL: int = 0
CONTINUE_RUNNING: int = 0
QUIT_BY_DEMAND: int = 1
TOKEN_KEY: str = "token"
BOT_STATUS: int = CONTINUE_RUNNING
EVENTS: list = ["text", "sticker", "photo", "audio", "video", "video_note", "voice"]
RUSSIAN_DATE_FORMAT = "%d.%m.%Y"


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


def is_foreign_command(pcommand: str) -> bool:
    """Возвращает True, если в команде присутствует имя другого бота."""
    result: bool = False
    for bot in statistic.BOTS:

        result = bot in pcommand
        if result:

            break
    return result


# pylint: disable=too-many-instance-attributes # а что еще делать???
class CSoftIceBot:
    """Универсальный бот для Телеграмма."""

    def __init__(self):
        """Конструктор класса."""
        super().__init__()
        self.config: dict = {}
        self.config_name: str = ""
        self.load_config(CONFIG_FILE_NAME)
        # *** Нужно ли работать через прокси?
        if self.config["proxy"]:
            apihelper.proxy = {'https': self.config["proxy"]}
        # *** Создаём собственно бота.
        self.robot: telebot.TeleBot = telebot.TeleBot(self.config[TOKEN_KEY])
        self.bot_status: int = CONTINUE_RUNNING
        self.exiting: bool = False
        self.message_text: str = ""
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
        self.bellringer: bellringer.CBellRinger = bellringer.CBellRinger(self.config, self.data_path)

        self.librarian: librarian.CLibrarian = librarian.CLibrarian(self.config, self.data_path)
        self.meteorolog: meteorolog.CMeteorolog = meteorolog.CMeteorolog(self.config)
        self.moderator: moderator.CModerator = moderator.CModerator(self.robot, self.config,
                                                                    self.database)
        self.statistic: statistic.CStatistic = statistic.CStatistic(self.config, self.database)
        self.stargazer: stargazer.CStarGazer = stargazer.CStarGazer(self.config, self.data_path)
        self.theolog: theolog.CTheolog = theolog.CTheolog(self.config, self.data_path)
        # *** Игра
        self.tomcat: tomcat.CTomCat = tomcat.CTomCat(self.config, self.data_path)
        # *** Обработчик сообщений
        """Обработчик сообщений."""
        @self.robot.message_handler(content_types=EVENTS)
        def process_message(pmessage):

            # *** Если это текстовое сообщение - обрабатываем в этой ветке.
            if pmessage.content_type == "text":

                # print(pmessage)
                # *** Вытаскиваем из сообщения нужные поля
                self.message_text, command, chat_id, chat_title, user_name, user_title = \
                    decode_message(pmessage)

                # *** Защита от привата
                if chat_title is None:

                    return

                # *** Проверим, легитимный ли этот чат
                if not self.is_this_chat_enabled(chat_title):

                    # *** Бота привели на чужой канал. Выходим.
                    self.robot.send_message(chat_id, "Вашего чата нет в списке разрешённых. Чао!")
                    self.robot.leave_chat(chat_id)
                    print(f"Караул! Меня похитили и затащили в чат {chat_title}! Но я удрал.")
                    return

                # *** Да, вполне легитимный. Сообщение не протухло?
                message_date = pmessage.date
                if (datetime.now() - datetime.fromtimestamp(message_date)).total_seconds() < 60:

                    # *** Если сообщение адресовано другому боту - пропускаем
                    if not is_foreign_command(pmessage.text):

                        answer: str = ""
                        # ***  Боту дали команду?
                        if self.message_text[0:1] == COMMAND_SIGN:

                            # *** Это системная команда?
                            if not self.process_command(command, chat_id, chat_title,
                                                        {"name": user_name, "title": user_title}):

                                # *** Нет. Ну и пусть модули разбираются....
                                answer = self.process_modules(chat_id, chat_title,
                                                              pmessage.from_user.id,
                                                              user_name,
                                                              user_title)
                                # *** Разобрались?
                        else:

                            # *** Нет. В этом чате статистик разрешен?
                            if self.statistic.is_enabled(chat_title):

                                # *** Проапдейтим базу статистика
                                self.statistic.save_all_type_of_messages(pmessage)
                            # *** Болтуну есть что ответить?
                            answer = self.babbler.talk(chat_title, self.message_text)
                        # *** Модули сработали?
                        if answer:

                            # *** Выводим ответ.
                            self.robot.send_message(chat_id, answer)
            # else:
            #
            #     # *** Бота привели на чужой канал. Выходим.
            #     self.robot.send_message(chat_id, "Вашего чата нет в списке разрешённых. Чао!")
            #     self.robot.leave_chat(chat_id)
            #     print(f"Караул! Меня похитили и затащили в чат {chat_title}! Но я удрал.")

            elif pmessage.content_type in EVENTS:

                self.statistic.save_all_type_of_messages(pmessage)

    def is_master(self, puser_name: str) -> bool:
        """Проверяет, хозяин ли отдал команду."""
        return puser_name == self.config["master"]

    def is_this_chat_enabled(self, pchat_title: str):
        """Проверяет, находится ли данный чат в списке разрешенных."""
        return pchat_title in self.config[ENABLED_IN_CHATS_KEY]

    def load_config(self, pconfig_file):
        """Загружает конфигурацию из JSON."""
        with open(pconfig_file, "r", encoding="utf-8") as json_file:

            self.config = json.load(json_file)
        self.config_name = pconfig_file

    def poll(self):
        """Функция опроса ботом телеграмма."""
        try:

            while self.bot_status == CONTINUE_RUNNING:

                self.robot.polling(none_stop=NON_STOP, interval=POLL_INTERVAL)
                print(f"Bot status = {BOT_STATUS}")

        except CQuitByDemand as exception:

            print(exception.message)
            self.bot_status = QUIT_BY_DEMAND
            self.robot.stop_polling()

    def process_command(self, pcommand: str, pchat_id: int, pchat_title: str,
                        puser: dict):
        """Обрабатывает системные команды"""
        result: bool = False
        # *** Да, команду. Это команда перезагрузки конфига?
        if pcommand in CONFIG_COMMANDS:

            result = self.reload_config(pchat_id, puser["name"], puser["title"])
        # *** Нет. Запросили выход?
        elif pcommand in EXIT_COMMANDS:

            self.stop_working(pchat_id, puser["name"], puser["title"])
            result = True
        # *** Опять нет. Запросили помощь?
        elif pcommand in HELP_COMMANDS:

            answer: str = self.send_help(pchat_title)
            if answer:

                self.robot.send_message(pchat_id, answer)
            result = True
        return result

    def process_modules(self, pchat_id: int, pchat_title: str,
                        puser_id: int, puser_name: str, puser_title: str):
        """Пытается обработать команду различными модулями."""
        assert pchat_title is not None, \
            "Assert: [softice.process_modules] No <pchat_title> parameter specified!"
        assert puser_title is not None, \
            "Assert: [softice.process_modules] No <puser_title> parameter specified!"
        # *** Проверим, не запросил ли пользователь что-то у бармена...
        print("**** ", self.message_text)
        answer: str = self.barman.barman(pchat_title, puser_name, puser_title,
                                         self.message_text).strip()

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

            answer = self.bellringer.bellringer(pchat_title, self.message_text).strip()
        if not answer:

            answer = self.babbler.babbler(pchat_title, puser_name, puser_title,
                                          self.message_text).strip()
        if not answer:

            answer = self.stargazer.stargazer(pchat_title, self.message_text).strip()
        if not answer:

            answer = self.moderator.moderator(pchat_id, pchat_title, puser_title, self.message_text)
        if not answer:

            answer = self.tomcat.tomcat(pchat_title, puser_id, puser_title, self.message_text)
        if not answer:

            # *** Незнакомая команда.
            print(" .. fail.")
        return answer

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
            self.load_config(self.config_name)
            self.robot.send_message(pchat_id, "Конфигурация обновлена.")
            return True
        print("Softice - нет прав.")
        self.robot.send_message(pchat_id, f"У вас нет на это прав, {puser_title}.")
        return False

    def send_help(self, pchat_title: str):
        """Проверяет, не была ли запрошена подсказка."""
        assert pchat_title is not None, \
            "Assert: [softice.is_help_command_queried] " \
            "No <pchat_title> parameter specified!"
        # *** Собираем ответы работников на запрос помощи
        answer: str = f"""\n{self.barman.get_hint(pchat_title)}
                          \n{self.bellringer.get_hint(pchat_title)}
                          \n{self.librarian.get_hint(pchat_title)}
                          \n{self.meteorolog.get_hint(pchat_title)}
                          \n{self.statistic.get_hint(pchat_title)}
                          \n{self.stargazer.get_hint(pchat_title)}
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

            self.robot.send_message(pchat_id, "Ухожу, ухожу...")
            self.exiting = True
            raise CQuitByDemand()
        self.robot.send_message(pchat_id, f"У вас нет на это прав, {puser_title}.")

    def poll_forever(self):
        """Функция опроса ботом телеграмма."""
        while self.bot_status == CONTINUE_RUNNING:

            try:

                # self.robot.polling(none_stop=NON_STOP, interval=POLL_INTERVAL)
                self.robot.polling(interval=POLL_INTERVAL)
            except CQuitByDemand as exception:

                print(exception.message)
                self.bot_status = QUIT_BY_DEMAND
                self.robot.stop_polling()
            except ConnectionError as ex:

                print("*" * 40)
                print(f"**** Exception occured: {ex}, reconnecting...")
            except ReadTimeout as ex:

                print("*" * 40)
                print(f"**** Exception occured: {ex}, reconnecting...")


if __name__ == "__main__":
    print(f"Started at {date.today().strftime(RUSSIAN_DATE_FORMAT)}")
    SofticeBot: CSoftIceBot = CSoftIceBot()
    SofticeBot.poll_forever()
    sys.exit(0)

# while not SofticeBot.exiting:
#
#     try:
#
#         SofticeBot.poll()
#     except ConnectionError as ex:
#
#         print("*" * 40)
#         print(f"**** Exception occured: {ex}, reconnecting...")
#     except ReadTimeout as ex:
#
#         print("*" * 40)
#         print(f"**** Exception occured: {ex}, reconnecting...")
# if SofticeBot.bot_status == QUIT_BY_DEMAND:

# @self.robot.callback_query_handler(func=lambda call: True)
# def callback_inline(call):
#     """Процедура обработки кнопок мафии"""
#
#     mafiozo_process(BOT_CONFIG, call.message.chat.id, call.message.chat.title,
#                     call.from_user.id, call.from_user.username, call.data)
