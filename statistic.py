# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Модуль статистики для бота."""

import prototype


HINT = ["стат", "stat"]
COMMANDS = ["топ10", "топ25", "топ50", "перс", "top10", "top25", "top50", "pers"]
ENABLED_IN_CHATS_KEY = "statistic_chats"


class CStatistic(prototype.CPrototype):
    """Класс метеоролога."""

    def __init__(self, pconfig):
        super().__init__()
        self.config = pconfig

    def can_process(self, pchat_title: str, pmessage_text: str) -> bool:
        """Возвращает True, если модуль может обработать команду."""
        if self.is_enabled(pchat_title):
            word_list: list = func.parse_input(pmessage_text)
            return word_list[0] in COMMANDS or word_list[0] in HINT
        return False


    def get_help(self) -> str:
        """Возвращает список команд модуля, доступных пользователю."""
        if self.is_enabled(pchat_title):

            command_list: str = ", ".join(COMMANDS)
            command_list += "\n"
            return command_list
        return ""

    def get_hint(self, pchat_title: str) -> str:
        """Возвращает команду верхнего уровня, в ответ на которую
           модуль возвращает полный список команд, доступных пользователю."""
        if self.is_enabled(pchat_title):

            return ", ".join(HINT)
        return ""

    def is_enabled(self, pchat_title: str) -> bool:
        """Возвращает True, если на этом канале этот модуль разрешен."""

    def reload(self):
        """Вызывает перезагрузку внешних данных модуля."""
