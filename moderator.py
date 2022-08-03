# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Погодный модуль для бота."""
from time import time

import functions as func
import prototype

ENABLED_IN_CHATS_KEY: str = "policeman_chats"
READ_ONLY_PERIOD: int = 600
READ_ONLY_MESSAGE: str = f"Помолчите {READ_ONLY_PERIOD / 60} минут"

MUTE_COMMANDS: list = ["mute", "mt"]


class CModerator(prototype.CPrototype):
    """Класс бармена."""

    def __init__(self, pbot, pconfig):

        super().__init__()
        self.config = pconfig
        self.bot = pbot

    def can_process(self, pchat_title: str, pmessage_text: str) -> bool:
        """Возвращает True, если модуль может обработать команду."""
        word_list: list = func.parse_input(pmessage_text)
        return self.is_enabled(pchat_title) and word_list[0] in MUTE_COMMANDS

    def get_help(self, pchat_title: str) -> str:
        """Возвращает список команд модуля, доступных пользователю."""
        return ""

    def get_hint(self, pchat_title: str) -> str:
        """Возвращает команду верхнего уровня, в ответ на которую
           модуль возвращает полный список команд, доступных пользователю."""
        return ""

    def is_enabled(self, pchat_title: str) -> bool:
        """Возвращает True, если на этом канале этот модуль разрешен."""
        return pchat_title in self.config[ENABLED_IN_CHATS_KEY]

    def moderator(self, pchat_id: int, pchat_title: str, puser_id: int,
                  puser_title: str, pmessage_text: str) -> str:
        """Процедура разбора запроса пользователя."""
        answer: str = ""
        word_list: list = func.parse_input(pmessage_text)
        if self.can_process(pchat_title, pmessage_text):

            mute_time: int = READ_ONLY_PERIOD
            if word_list[0] in MUTE_COMMANDS:

                # *** Молчанка
                # user_name: str = word_list[1]
                if len(word_list) > 2:

                    mute_time = int(word_list[2])
                    # ToDo: Вот тут получить ID указанного юзера по нику.
                self.bot.restrict_chat_member(pchat_id, puser_id, until_date=time() + mute_time)
                answer = f"{puser_title}, помолчите пока..."
                # self.bot.send_message(pchat_id, )
        return answer
        # bot.restrict_chat_member(chat_id, user_id,
        # can_send_messages=False, can_send_media_messages=False,
        #                          can_send_other_messages=False)

    def reload(self):
        """Вызывает перезагрузку внешних данных модуля."""
