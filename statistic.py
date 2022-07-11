# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Модуль статистики для бота."""

import prototype
import functions

import m_users

HINT = ["стат", "stat"]
COMMANDS = ["топ10", "топ25", "топ50", "перс", "top10", "top25", "top50", "pers"]
ENABLED_IN_CHATS_KEY = "statistic_chats"


class CStatistic(prototype.CPrototype):
    """Класс метеоролога."""

    def __init__(self, pconfig, pdatabase):
        super().__init__()
        self.config = pconfig
        self.database = pdatabase

    def can_process(self, pchat_title: str, pmessage_text: str) -> bool:
        """Возвращает True, если модуль может обработать команду."""
        if self.is_enabled(pchat_title):
            word_list: list = functions.parse_input(pmessage_text)
            return word_list[0] in COMMANDS or word_list[0] in HINT
        return False

    def get_help(self, pchat_title: str) -> str:
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

    def save_message(self, pmessage):
        """Сохраняет фразу, произнесенную пользователем, в базе."""
        # print(pmessage)
        message_text: str = pmessage.text
        chat_id: int = pmessage.chat.id
        chat_title: str = pmessage.chat.title
        user_id: int = pmessage.from_user.id
        user_name: str = pmessage.from_user.username
        user_title: str = pmessage.from_user.first_name
        # проверить, нет ли чата в таблице чатов, если нет - добавить, и получить id
        # если есть - получить id
        # проверить, нет ли юзера в таблице тг юзеров, если нет - добавить и получить id
        # если есть - получить id
        # проверить, нет ли юзера в таблице имен, если нет - добавить и получить id
        # если есть - получить id

        tg_id_data = self.database.get_session().query(m_users.CUser).filter_by(ftguserid=user_id)
        if tg_id_data.count() == 0:

            # print(tg_id_data.all())
