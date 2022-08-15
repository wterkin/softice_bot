#! /usr/bin/python3
# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Модуль прототипа классов модулей бота."""

from abc import ABCMeta, abstractmethod  # , abstractproperty

import datetime

NEW_STYLE_OFFSET = 13


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
    return datetime.date(pyear, month, day)


class CStarGazer:
    """Прототип классов модулей бота."""
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    def can_process(self, pchat_title: str, pmessage_text: str) -> bool:
        """Возвращает True, если модуль может обработать команду."""

    def get_help(self, pchat_title: str) -> str:
        """Возвращает список команд модуля, доступных пользователю."""

    def get_hint(self, pchat_title: str) -> str:
        """Возвращает команду верхнего уровня, в ответ на которую
           модуль возвращает полный список команд, доступных пользователю."""

    def is_enabled(self, pchat_title: str) -> bool:
        """Возвращает True, если на этом канале этот модуль разрешен."""

    def reload(self):
        """Вызывает перезагрузку внешних данных модуля."""
