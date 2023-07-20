#! /usr/bin/python3
# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Бот для Телеграмма"""
import os
from datetime import datetime
import time
import sys
from sys import platform
import json
import logging
import telebot
from telebot import apihelper
from requests import ReadTimeout, ConnectTimeout
import urllib3.exceptions

# *** Собственные модули
import functions as func
import database
import babbler
import barman
import bellringer
import haijin
import librarian
import meteorolog
import moderator
import statistic
import stargazer
# import supervisor
import theolog
import welcomer

# *** Местоположение данных бота
ENABLED_IN_CHATS_KEY: str = "allowed_chats"
LINUX_DATA_FOLDER_KEY: str = "linux_data_folder"
LOGGING_KEY: str = "logging"
WINDOWS_DATA_FOLDER_KEY: str = "windows_data_folder"
TOKEN_KEY: str = "token"


CONFIG_FILE_NAME: str = "config.json"
BOT_NAME: str = "SoftIceBot"
COMMAND_SIGN: str = "!"
HELP_MESSAGE: str = "В настоящий момент я понимаю только следующие группы команд: \n"
EVENTS: list = ["text", "sticker", "photo", "audio", "video", "video_note", "voice"]
RUSSIAN_DATE_FORMAT: str = "%d.%m.%Y"
RUSSIAN_DATETIME_FORMAT = "%d.%m.%Y %H:%M:%S"

CONFIG_COMMANDS: list = ["конфиг", "config"]
EXIT_COMMANDS: list = ["прощай", "bye", "!!"]
HELP_COMMANDS: list = ["помощь", "help"]
RESTART_COMMAND: list = ["перезапуск", "restart", "22"]
NON_STOP: bool = True
POLL_INTERVAL: int = 0
CONTINUE_RUNNING: int = 0
QUIT_BY_DEMAND: int = 1
RESTART_BY_DEMAND: int = 2
BOT_STATUS: int = CONTINUE_RUNNING
RUNNING_FLAG: str = "running.flg"
SLEEP_BEFORE_EXIT_BY_ERROR: int = 10


class CQuitByDemand(Exception):
    """Исключение выхода."""

    def __init__(self):
        self.message: str = "* Выход по требованию."
        super().__init__(self.message)


class CRestartByDemand(Exception):
    """Исключение выхода."""

    def __init__(self):
        self.message: str = "* Перезапуск по требованию."
        super().__init__(self.message)


def decode_message(pmessage):
    """Возвращает куски сообщения, $#^^^!!!! """
    text: str = ""
    if pmessage.text is not None:

        text = pmessage.text
    else:
        if pmessage.caption is not None:

            text = pmessage.caption
    return text, \
        text[1:].lower(), \
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


# int: disable=too-many-instance-attributes # а что еще делать???
class CSoftIceBot:
    """Универсальный бот для Телеграмма."""

    def __init__(self):
        """Конструктор класса."""
        super().__init__()
        self.config: dict = {}
        self.load_config(CONFIG_FILE_NAME)
        print("*****", self.config["chats"]["Anastasis"][0])
        # *** Нужно ли работать через прокси?
        if self.config["proxy"]:

            apihelper.proxy = {'https': self.config["proxy"]}
        # *** Создаём собственно бота.
        self.robot: telebot.TeleBot = telebot.TeleBot(self.config[TOKEN_KEY])
        self.bot_status: int = CONTINUE_RUNNING
        self.running_flag: str = os.getcwd() + "/" + RUNNING_FLAG
        if os.path.exists(self.running_flag):

            print("* Перезапуск после падения либо по требованию.")
            # logging.info("Перезапуск после падения либо по требованию.")
        else:

            with open(self.running_flag, 'tw', encoding='utf-8'):

                pass
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
            database.create()
        log_name: str = self.data_path+'softice.log'
        print(f"* Создаём файл журнала {log_name} с уровнем {self.config[LOGGING_KEY]}")
        self.logger = logging.getLogger(__name__)
        self.logger.propagate = False
        handler = logging.FileHandler(log_name)
        handler.setLevel(int(self.config[LOGGING_KEY]))
        formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        # *** Поехали создавать объекты модулей =)
        self.barman: barman.CBarman = barman.CBarman(self.config, self.data_path)
        self.babbler: babbler.CBabbler = babbler.CBabbler(self.config, self.data_path)
        self.bellringer: bellringer.CBellRinger = bellringer.CBellRinger(self.config,
                                                                         self.data_path)
        self.haijin: haijin.CHaijin = haijin.CHaijin(self.config, self.data_path)
        self.librarian: librarian.CLibrarian = librarian.CLibrarian(self.config, self.data_path)
        self.meteorolog: meteorolog.CMeteorolog = meteorolog.CMeteorolog(self.config)
        self.moderator: moderator.CModerator = moderator.CModerator(self.robot, self.config,
                                                                    self.data_path)
        # !!! self.supervisor: supervisor.CSupervisor =
        # supervisor.CSupervisor(self.robot, self.config,
        #                                                                  self.database)
        self.statistic: statistic.CStatistic = statistic.CStatistic(self.config, self.database)
        self.stargazer: stargazer.CStarGazer = stargazer.CStarGazer(self.config, self.data_path)
        self.theolog: theolog.CTheolog = theolog.CTheolog(self.config, self.data_path)
        self.welcomer: welcomer.CWelcomer = welcomer.CWelcomer(self.config, self.data_path)

        # *** Обработчик сообщений
        @self.robot.message_handler(content_types=EVENTS)
        def process_message(pmessage):

            do_not_screen: bool = False
            answer: str = ""
            # *** Вытаскиваем из сообщения нужные поля
            self.message_text, command, chat_id, chat_title, user_name, user_title = \
                decode_message(pmessage)
            # *** Проверим, легитимный ли этот чат
            if not self.is_this_chat_enabled(chat_title):

                if chat_title is not None:

                    # *** Бота привели на чужой канал. Выходим.
                    self.robot.send_message(chat_id, "Вашего чата нет в списке разрешённых. Чао!")
                    self.robot.leave_chat(chat_id)
                    print(f"* Попытка нелегитимного использования бота в чате {chat_title}.")
                    self.logger.warning("Попытка нелегитимного использования бота"
                                        " в чате %s.", chat_title)
                else:

                    answer = "Я в приватах не работаю."

            else:

                # *** Сообщение не протухло?
                message_date = pmessage.date
                if (datetime.now() - datetime.fromtimestamp(message_date)).total_seconds() < 60:

                    # *** Модератор должен следить за порядком в чате
                    answer = self.moderator.moderator(pmessage)
                    if not answer:

                        # !!! answer = self.supervisor.supervisor(pmessage)
                        if not answer:

                            # *** Если это текстовое сообщение - обрабатываем в этой ветке.
                            if pmessage.content_type == "text" and self.message_text is not None:

                                # *** Если сообщение адресовано другому боту - пропускаем
                                if not is_foreign_command(pmessage.text):

                                    # ***  Боту дали команду?
                                    if self.message_text[0:1] == COMMAND_SIGN:

                                        # *** Это системная команда?
                                        if not self.process_command(command, chat_id, chat_title,
                                                                    {"name": user_name,
                                                                     "title": user_title}):

                                            # *** Нет. Ну и пусть модули разбираются....
                                            answer, do_not_screen = self.process_modules(pmessage)
                                    else:

                                        # *** Нет. В этом чате статистик разрешен?
                                        if self.statistic.is_enabled(chat_title):

                                            # *** Проапдейтим базу статистика
                                            self.statistic.save_all_type_of_messages(pmessage)

                                        # *** Болтуну есть что ответить?
                                        answer = self.babbler.talk(chat_title, self.message_text)
                            elif pmessage.content_type in EVENTS:

                                self.statistic.save_all_type_of_messages(pmessage)

            # *** Ответ имеется?
            if answer:

                # *** Выводим ответ
                if do_not_screen:

                    self.robot.send_message(pmessage.chat.id, answer, parse_mode="MarkdownV2")
                else:

                    self.robot.send_message(pmessage.chat.id, func.screen_text(answer),
                                            parse_mode="MarkdownV2")

    def is_master(self, puser_name: str) -> bool:
        """Проверяет, хозяин ли отдал команду."""
        return puser_name == self.config["master"]

    def is_this_chat_enabled(self, pchat_title: str) -> object:
        """Проверяет, находится ли данный чат в списке разрешенных."""
        return pchat_title in self.config[ENABLED_IN_CHATS_KEY]

    def load_config(self, pconfig_name: str):
        """Загружает конфигурацию из JSON."""
        with open(pconfig_name, "r", encoding="utf-8") as json_file:

            self.config = json.load(json_file)

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
        elif pcommand in RESTART_COMMAND:

            self.restart(pchat_id, puser["name"], puser["title"])
            result = True
        return result

    def process_modules(self, pmessage):
        """Пытается обработать команду различными модулями."""
        # *** Проверим, не запросил ли пользователь что-то у бармена...
        answer: str = self.barman.barman(pmessage.chat.title,
                                         pmessage.from_user.username,
                                         pmessage.from_user.first_name,
                                         self.message_text).strip()
        do_not_screen: bool = False
        if not answer:

            # *** Или у звонаря
            answer = self.bellringer.bellringer(pmessage.chat.title, self.message_text).strip()
        if not answer:

            # *** ... или у хайдзина
            answer = self.haijin.haijin(pmessage.chat.title,
                                        pmessage.from_user.username,
                                        pmessage.from_user.first_name, self.message_text)
            do_not_screen = True
        if not answer:

            do_not_screen = False
            # *** ... или у библиотекаря...
            answer = self.librarian.librarian(pmessage.chat.title,
                                              pmessage.from_user.username,
                                              pmessage.from_user.first_name,
                                              self.message_text).strip()
        if not answer:

            # *** ... или у метеоролога...
            answer = self.meteorolog.meteorolog(pmessage.chat.title, self.message_text).strip()
        if not answer:

            # *** ... или у модератора...
            answer = self.moderator.moderator(pmessage)
        if not answer:

            # *** ... или у статистика...
            answer = self.statistic.statistic(pmessage.chat.id, pmessage.chat.title,
                                              pmessage.from_user.first_name,
                                              self.message_text).strip()
        if not answer:

            # *** ... или у звездочёта...
            answer = self.stargazer.stargazer(pmessage.chat.title, self.message_text).strip()
        if not answer:

            # *** ... или у теолога...
            answer = self.theolog.theolog(pmessage.chat.title, self.message_text).strip()
        if not answer:

            # *** Мажордом точно разберется
            answer = self.welcomer.welcomer(pmessage.chat.title, self.message_text).strip()
        if not answer:
            print("*** 1")
            # *** ... может, у болтуна есть, что сказать?
            answer = self.babbler.babbler(pmessage.chat.title,
                                          pmessage.from_user.username,
                                          pmessage.from_user.first_name,
                                          self.message_text).strip()
        if not answer:
            # *** Незнакомая команда.
            print(f"* Запрошена неподдерживаемая команда {self.message_text}.")
            self.logger.info("* Запрошена неподдерживаемая команда %s"
                             " в чате %s.", self.message_text, pmessage.chat.title)
        return answer, do_not_screen

    def reload_config(self, pchat_id: int, puser_name: str, puser_title: str):
        """Проверяет, не является ли поданная команда командой перезагрузки конфигурации."""
        assert pchat_id is not None, \
            "Assert: [softice.is_reload_config_command_queried] " \
            "Пропущен параметр <pchat_id> !"
        assert puser_title is not None, \
            "Assert: [softice.is_reload_config_command_queried] " \
            "Пропущен параметр <puser_title> !"
        # *** Такое запрашивать может только хозяин
        if self.is_master(puser_name):

            self.robot.send_message(pchat_id, "Обновляю конфигурацию.")
            self.load_config(CONFIG_FILE_NAME)
            self.robot.send_message(pchat_id, "Конфигурация обновлена.")
            return True
        print(f"* Запрос на перезагрузку конфига от нелегитимного лица {puser_title}.")
        self.logger.warning("Запрос на перезагрузку конфига от нелегитимного лица %s.",
                            puser_title)
        self.robot.send_message(pchat_id, f"У вас нет на это прав, {puser_title}.")
        return False

    def send_help(self, pchat_title: str):
        """Проверяет, не была ли запрошена подсказка."""
        assert pchat_title is not None, \
            "Assert: [softice.is_help_command_queried] " \
            "Пропущен параметр <pchat_title> !"
        # *** Собираем ответы модулей на запрос помощи
        answer: str = f"""\n{self.barman.get_hint(pchat_title)}
                          \n{self.bellringer.get_hint(pchat_title)}
                          \n{self.haijin.get_hint(pchat_title)}
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
            "Пропущен параметр <pchat_id> !"
        assert puser_title is not None, \
            "Assert: [softice.is_quit_command_queried] " \
            "Пропущен параметр <puser_title> !"
        if self.is_master(puser_name):

            self.robot.send_message(pchat_id, "Добби свободен!")
            os.remove(self.running_flag)
            # self.exiting = True
            raise CQuitByDemand()
        self.robot.send_message(pchat_id, f"У вас нет на это прав, {puser_title}.")

    def restart(self, pchat_id: int, puser_name: str, puser_title: str):
        """Проверка, вдруг была команда рестарта."""
        assert pchat_id is not None, \
            "Assert: [softice.is_quit_command_queried] " \
            "Пропущен параметр <pchat_id> !"
        assert puser_title is not None, \
            "Assert: [softice.is_quit_command_queried] " \
            "Пропущен параметр <puser_title> !"
        if self.is_master(puser_name):

            self.robot.send_message(pchat_id, "Щасвирнус.")
            raise CRestartByDemand()
        self.robot.send_message(pchat_id, f"У вас нет на это прав, {puser_title}.")

    def poll_forever(self):
        """Функция опроса ботом телеграмма."""
        while self.bot_status == CONTINUE_RUNNING:

            try:

                self.robot.polling(interval=POLL_INTERVAL)
            except CQuitByDemand as exception:

                # print(exception.message)
                self.logger.exception(exception.message)
                self.bot_status = QUIT_BY_DEMAND
                self.robot.stop_polling()
                sys.exit(0)
            except CRestartByDemand as exception:

                # print(exception.message)
                self.logger.exception(exception.message)
                self.bot_status = RESTART_BY_DEMAND
                self.robot.stop_polling()
                sys.exit(1)
            except ConnectionError:

                print("# Соединение прервано. Выход.")
                self.logger.exception("Соединение прервано. Выход.", exc_info=True)
                time.sleep(SLEEP_BEFORE_EXIT_BY_ERROR)
                sys.exit(2)
            except ReadTimeout:

                print("# Превышен интервал ожидания ответа. Выход.")
                self.logger.exception("Превышен интервал ожидания ответа. Выход.", exc_info=True)
                time.sleep(SLEEP_BEFORE_EXIT_BY_ERROR)
                sys.exit(3)
            except telebot.apihelper.ApiTelegramException:

                print("# Telegram отказал в соединении. Выход.")
                self.logger.exception("Telegram отказал в соединении. Выход.", exc_info=True)
                time.sleep(SLEEP_BEFORE_EXIT_BY_ERROR*2)
                sys.exit(4)
            except urllib3.exceptions.MaxRetryError:

                print("# Слишком много попыток соединения. Выход.")
                self.logger.exception("Слишком много попыток соединения. Выход.", exc_info=True)
                time.sleep(SLEEP_BEFORE_EXIT_BY_ERROR*2)
                sys.exit(5)
            except ConnectTimeout:

                print("# Превышен интервал времени для соединения. Выход.")
                self.logger.exception("Превышен интервал времени для соединения. Выход.",
                                      exc_info=True)
                time.sleep(SLEEP_BEFORE_EXIT_BY_ERROR)
                sys.exit(6)
            except urllib3.exceptions.ProtocolError:

                print("# Соединение разорвано. Выход.")
                self.logger.exception("Соединение разорвано. Выход.", exc_info=True)
                time.sleep(SLEEP_BEFORE_EXIT_BY_ERROR)
                sys.exit(7)
            # except ConnectionResetError:
            #
            #     print("# Ошибка переустановления соединения. Выход.")
            #     time.sleep(SLEEP_BEFORE_EXIT_BY_ERROR)
            #     sys.exit(5)


if __name__ == "__main__":

    print(f"* SoftIce (пере)запущен {datetime.now().strftime(RUSSIAN_DATETIME_FORMAT)}")
    SofticeBot: CSoftIceBot = CSoftIceBot()
    SofticeBot.logger.info("SoftIce (пере)запущен %s",
                           datetime.now().strftime(RUSSIAN_DATETIME_FORMAT))
    SofticeBot.poll_forever()

# logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
# logging.basicConfig(filename='msg.log', filemode='w',
#   format='%(name)s - %(levelname)s - %(message)s')
# logging.debug('The debug message is displaying')
# logging.info('The info message is displaying')
# logging.warning('The warning message is displaying')
# logging.error('The error message is displaying')
# logging.critical('The critical message is displaying')
