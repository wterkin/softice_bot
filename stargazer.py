#! /usr/bin/python3
# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Модуль прототипа классов модулей бота."""

from abc import ABCMeta

from datetime import date

import functions

NEW_STYLE_OFFSET: int = 13
COMMANDS: tuple = ("пасха", "easter")
HINTS: tuple = ("календарь", "кл", "calendar", "cl")
ENABLED_IN_CHATS_KEY: str = "stargazer_chats"
RUSSIAN_DATE_FORMAT = "%d.%m.%Y"


def calculate_easter(pyear):
    """Вычисляет дату пасхи на заданный год."""
    # a = (19*(year mod 19)+15) mod 30
    first_value: int = (19 * (pyear % 19) + 15) % 30
    # b = (2*(year mod 4) + 4*(year mod 7) +6*a + 6) mod 7
    second_value: int = (2 * (pyear % 4) + 4 * (pyear % 7) + 6 * first_value + 6) % 7
    month: int
    day: int
    if (first_value + second_value) > 9:

        # *** Апрель
        month = 4
        day = (first_value + second_value) - 9
        if day > 30:

            month += 1
            day = day - 30
    else:

        # *** Март
        month = 3
        day = first_value + second_value + 22 + NEW_STYLE_OFFSET
        if day > 31:

            month += 1
            day = day - 31
    return date(pyear, month, day)


class CStarGazer:
    """Прототип классов модулей бота."""
    __metaclass__ = ABCMeta

    def __init__(self, pconfig):
        self.config = pconfig

    def can_process(self, pchat_title: str, pmessage_text: str) -> bool:
        """Возвращает True, если модуль может обработать команду."""
        assert pchat_title is not None, \
            "Assert: [barman.can_process] " \
            "No <pchat_title> parameter specified!"
        assert pmessage_text is not None, \
            "Assert: [barman.can_process] " \
            "No <pmessage_text> parameter specified!"
        found: bool = False
        if self.is_enabled(pchat_title):

            word_list: list = functions.parse_input(pmessage_text)
            found = word_list[0] in COMMANDS
            if not found:

                found = word_list[0] in HINTS
        return found

    def get_help(self, pchat_title: str) -> str:
        """Возвращает список команд модуля, доступных пользователю."""
        assert pchat_title is not None, \
            "Assert: [barman.get_help] " \
            "No <pchat_title> parameter specified!"
        command_list: str = ""
        if self.is_enabled(pchat_title):

            for command in COMMANDS:

                command_list += ", ".join(command) + "\n"
        return command_list

    def get_hint(self, pchat_title: str) -> str:
        """Возвращает команду верхнего уровня, в ответ на которую
           модуль возвращает полный список команд, доступных пользователю."""
        assert pchat_title is not None, \
            "Assert: [barman.get_hint] " \
            "No <pchat_title> parameter specified!"
        if self.is_enabled(pchat_title):

            return ", ".join(HINTS)
        return ""

    def is_enabled(self, pchat_title: str) -> bool:
        """Возвращает True, если на этом канале этот модуль разрешен."""
        assert pchat_title is not None, \
            "Assert: [barman.is_enabled] " \
            "No <pchat_title> parameter specified!"

        return pchat_title in self.config[ENABLED_IN_CHATS_KEY]

    def reload(self):
        """Вызывает перезагрузку внешних данных модуля."""

    def stargazer(self, pchat_title: str, pmessage_text: str, puser_title: str) -> str:
        """Обработчик команд звездочёта."""
        assert pchat_title is not None, \
            "Assert: [barman.barman] No <pchat_title> parameter specified!"
        assert puser_title is not None, \
            "Assert: [barman.barman] No <puser_title> parameter specified!"
        assert pmessage_text is not None, \
            "Assert: [barman.barman] No <pmessage_text> parameter specified!"
        answer: str = ""
        word_list: list = functions.parse_input(pmessage_text)
        if self.can_process(pchat_title, pmessage_text):

            # *** Возможно, запросили меню.
            if word_list[0] in HINTS:

                answer = "Сегодня в баре имеется следующий ассортимент: \n" + \
                         self.get_help(pchat_title)
            else:

                if len(word_list) > 1:

                    if word_list[1].isdigit():

                        year = int(word_list[1])
                        answer = calculate_easter(year).strftime(RUSSIAN_DATE_FORMAT)
                else:

                    year: int = date.today().year
                    answer = calculate_easter(year).strftime(RUSSIAN_DATE_FORMAT)
        if answer:

            print(f"Barman answers: {answer[:16]}")
        return answer.strip()
