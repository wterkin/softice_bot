# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Модуль для бота."""
import functions
import prototype

COMMANDS: list = ["звонить", "звон", "зв", "bell"]
BELLRINGER_HINT: list = ["звонарь", "ringer"]
BELLRINGER_FOLDER: str = "bellringer/"
ENABLED_IN_CHATS_KEY: str = "bellringer_chats"


class CBellRinger(prototype.CPrototype):
    """Класс звонаря."""

    def __init__(self, pconfig, pdata_path):

        super().__init__()
        self.config = pconfig
        self.data_path = pdata_path + BELLRINGER_FOLDER

    def bellringer(self, pchat_title: str, pmessage_text: str):
        """Основная функция модуля."""
        answer: str = ""
        word_list: list = functions.parse_input(pmessage_text)
        print("bellringer")
        if self.can_process(pchat_title, pmessage_text):

            if word_list[0] in BELLRINGER_HINT:

                answer = self.get_help(pchat_title)
            else:

                if word_list[0] in COMMANDS:

                    user_list = functions.load_from_file(self.data_path+"/"+pchat_title+".txt")
                    answer = "Эй, " + ", ".join(user_list) + "!!! \n Игра начинается!"
        return answer

    def can_process(self, pchat_title: str, pmessage_text: str) -> bool:
        """Возвращает True, если модуль может обработать команду."""
        found: bool = False
        if self.is_enabled(pchat_title):

            word_list: list = functions.parse_input(pmessage_text)
            for command in COMMANDS:

                found = word_list[0] in command
                if found:

                    break
            if not found:

                found = word_list[0] in BELLRINGER_HINT
        return found

    def get_help(self, pchat_title: str) -> str:
        """Возвращает список команд модуля, доступных пользователю."""
        return ", ".join(COMMANDS) + "\n"

    def get_hint(self, pchat_title: str) -> str:
        """Возвращает команду верхнего уровня, в ответ на которую
           модуль возвращает полный список команд, доступных пользователю."""
        if self.is_enabled(pchat_title):

            return ", ".join(BELLRINGER_HINT)
        return ""

    def is_enabled(self, pchat_title: str) -> bool:
        """Возвращает True, если на этом канале этот модуль разрешен."""
        return pchat_title in self.config[ENABLED_IN_CHATS_KEY]

    def is_master(self, puser_name: str) -> bool:
        """Проверяет, хозяин ли отдал команду."""
        return puser_name == self.config["master"]

    def reload(self):
        """Вызывает перезагрузку внешних данных модуля."""
