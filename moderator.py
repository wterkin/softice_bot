# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Погодный модуль для бота."""
from time import time

import functions as func
import prototype

import m_names
import m_users
ENABLED_IN_CHATS_KEY: str = "moderator_chats"
READ_ONLY_PERIOD: int = 900
READ_ONLY_MESSAGE: str = f"Помолчите {READ_ONLY_PERIOD / 60} минут"

MUTE_COMMANDS: list = ["mute", "mt",
                       "mutehour", "mth",
                       "muteday", "mtd",
                       "muteweek", "mtw",
                       "unmute", "unm"]
MINUTE: int = 60
QUART_OF_HOUR: int = MINUTE * 3 #15
HOUR: int = MINUTE * 60
DAY: int = HOUR * 24
WEEK: int = DAY * 7
# MONTH: int = WEEK * 4
# YEAR: int = MONTH * 12

MUTE_PERIODS: list = [QUART_OF_HOUR, QUART_OF_HOUR,
                      HOUR, HOUR,
                      DAY, DAY,
                      WEEK, WEEK,
                      0, 0]
MUTE_PERIODS_TITLES: list = ["15 минут", "15 минут",
                             "1 час", "1 час",
                             "1 день", "1 день",
                             "1 неделю", "1 неделю"]


class CModerator(prototype.CPrototype):
    """Класс бармена."""

    def __init__(self, pbot, pconfig, pdatabase):

        super().__init__()
        self.config = pconfig
        self.bot = pbot
        self.database = pdatabase

    def can_process(self, pchat_title: str, pmessage_text: str) -> bool:
        """Возвращает True, если модуль может обработать команду."""
        word_list: list = func.parse_input(pmessage_text)
        return self.is_enabled(pchat_title) and word_list[0] in MUTE_COMMANDS

    def find_user_id(self, puser_title: str):
        """Ищет в базе ID пользователя по его нику."""
        session = self.database.get_session()
        query = session.query(m_names.CName, m_users.CUser)
        query = query.filter_by(fusername=puser_title)
        query = query.join(m_users.CUser, m_users.CUser.id == m_names.CName.fuserid)
        data = query.first()
        # inner_user_id = data.fuserid
        # query =
        # print("%%%%%%% ", data.ftguserid)
        if data is not None:

            return data[1].ftguserid
        else:

            return None

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

    def moderator(self, pchat_id: int, pchat_title: str,
                  pmessage_text: str) -> str:
        """Процедура разбора запроса пользователя."""
        answer: str = ""
        word_list: list = func.parse_input(pmessage_text)
        if self.can_process(pchat_title, pmessage_text):

            # admin_list: list = self.bot.getChatAdministrators(pchat_id)

            # mute_time: int = READ_ONLY_PERIOD
            if word_list[0] in MUTE_COMMANDS:

                # *** Молчанка
                period_index: int = MUTE_COMMANDS.index(word_list[0])
                user_title: str = " ".join(word_list[1:])
                mute_time = MUTE_PERIODS[period_index]
                user_id = self.find_user_id(user_title)
                if user_id is not None:

                    self.bot.restrict_chat_member(pchat_id, user_id, until_date=time() + mute_time)
                    if mute_time == 0:

                        answer = f"{user_title}, можете разговаривать."
                    else:

                        answer = f"{user_title}, помолчите {MUTE_PERIODS_TITLES[period_index]}, подумайте..."
                else:

                    answer = f"Кто такой {user_title}? Не знаю его..."
                # elf.bot.send_message(pchat_id, )
        return answer
        # bot.restrict_chat_member(chat_id, user_id,
        # can_send_messages=False, can_send_media_messages=False,
        #                          can_send_other_messages=False)
    #
    # or entity in message.entities:  # Пройдёмся по всем entities в поисках ссылок
    # # url - обычная ссылка, text_link - ссылка, скрытая под текстом
    # if entity.type in ["url", "text_link"]:
    #     # Мы можем не проверять chat.id, он проверяется ещё в хэндлере
    #     bot.delete_message(message.chat.id, message.message_id)
    # else:
    #     return

    def reload(self):
        """Вызывает перезагрузку внешних данных модуля."""
