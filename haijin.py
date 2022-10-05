# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Модуль - цитатник хокку. 俳人"""

import os
import random
from datetime import datetime as dtime
import functions as func
import prototype
import librarian

# *** Команды для цитатника хокку
ASK_HOKKU_CMD: int = 0
ADD_HOKKU_CMD: int = 1
DEL_HOKKU_CMD: int = 2
FIND_HOKKU_CMD: int = 3

RELOAD_BOOK: list = ["hokkureload", "hkrl"]
SAVE_BOOK: list = ["hokkuksave", "hksv"]
HAIJIN_FOLDER: str = "haijin/"
HAIJIN_FILE_NAME: str = "hokku.txt"

HAIJIN_COMMANDS: list = [["хк", "hk", "Получить случайное хокку"],
                         ["хк?", "hk?", "Найти хокку по фрагменту текста"],
                         ["хк+", "hk+", "Добавить хокку в базу"],
                         ["хк-", "hk-", "Удалить хокку из базы"],
                        ]

HINT = ["хокку", "hokku"]
ENABLED_IN_CHATS_KEY: str = "haijin_chats"


def get_command(self, pword: str) -> int:
    """Распознает команду и возвращает её код, в случае неудачи - None.
    """
    assert pword is not None, \
        "Assert: [haijin.get_command] " \
        "No <pword> parameter specified!"
    result: int = -1
    for command_idx, command in enumerate(HAIJIN_COMMANDS):

        if pword in command:
            result = command_idx

    return result


class CHaijin(prototype.CPrototype):
    """Класс хайдзина."""

    def __init__(self, pconfig: dict, pdata_path: str):

        super().__init__()
        self.config = pconfig
        self.data_path = pdata_path + HAIJIN_FOLDER
        self.hokku: list = []
        self.reload()

    def can_process(self, pchat_title: str, pmessage_text: str) -> bool:
        """Возвращает True, если хайдзин может обработать эту команду."""
        assert pchat_title is not None, \
            "Assert: [haijin.can_process] " \
            "No <pchat_title> parameter specified!"
        assert pmessage_text is not None, \
            "Assert: [haijin.can_process] " \
            "No <pmessage_text> parameter specified!"
        found: bool = False
        if self.is_enabled(pchat_title):

            word_list: list = func.parse_input(pmessage_text)
            for command in HAIJIN_COMMANDS:

                found = word_list[0] in command
                if found:

                    break

            if not found:

                found = word_list[0] in HINT
                if not found:

                    found = word_list[0] in RELOAD_BOOK
                    if not found:

                        found = word_list[0] in SAVE_BOOK
        return found
