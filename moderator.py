# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Погодный модуль для бота."""
from time import time
import re
import functions as func
import prototype
import m_names
import m_users

ENABLED_IN_CHATS_KEY: str = "moderator_chats"
MUTE_COMMANDS: list = ["mute", "mt",
                       "mutehour", "mth",
                       "muteday", "mtd",
                       "muteweek", "mtw",
                       "unmute", "unm"]
MINUTE: int = 60
QUART_OF_HOUR: int = MINUTE * 15
HOUR: int = MINUTE * 60
DAY: int = HOUR * 24
WEEK: int = DAY * 7
UNMUTE_PERIOD = 60

MUTE_PERIODS: list = [QUART_OF_HOUR, QUART_OF_HOUR,
                      HOUR, HOUR,
                      DAY, DAY,
                      WEEK, WEEK,
                      UNMUTE_PERIOD, UNMUTE_PERIOD]

MUTE_PERIODS_TITLES: list = ["15 минут", "15 минут",
                             "1 час", "1 час",
                             "1 день", "1 день",
                             "1 неделю", "1 неделю"]

ADMINISTRATION_CMD: list = ["admin", "adm"]

BAD_WORDS_LANG: list = ["^\s*[б,м,п]л[яR][д,т]*[ьъb]*$",
                        "^.*[х,п]у[и,й].*$",
                        "^.*п[е,и][с,з][д,т]а.*$"
                        ]
BADWORDS_MUTE_TIME = 300


def check_bad_words(pmessage) -> bool:
    """Проверяет сообщение на наличие мата."""
    result: bool = False
    for word in BAD_WORDS_LANG:

        # print(word, pmessage)
        # print(re.search(word, pmessage))
        result = re.match(word, pmessage) is not None
        # print(result)
        if result:

            # print("Агааа!")
            break

    return result


class CModerator(prototype.CPrototype):
    """Класс модератора."""

    def __init__(self, pbot, pconfig, pdatabase):

        super().__init__()
        self.config = pconfig
        self.bot = pbot
        self.database = pdatabase

    def can_process(self, pchat_title: str, pmessage_text: str) -> bool:
        """Возвращает True, если модуль может обработать команду."""
        word_list: list = func.parse_input(pmessage_text)
        return self.is_enabled(pchat_title) and \
            (word_list[0] in MUTE_COMMANDS or word_list[0] in ADMINISTRATION_CMD)

    def control_talking(self, pchat_id, pchat_title: str, puser_title: str, pmessage_text: str):
        """Следит за матершинниками."""
        answer: str = ""
        # print(pmessage_text)
        if self.is_enabled(pchat_title):

            # print("!!!", check_bad_words(pmessage_text))
            if check_bad_words(pmessage_text):

                user_id = self.find_user_id(puser_title)
                if user_id is not None:

                    self.bot.restrict_chat_member(pchat_id, user_id, until_date=time() + BADWORDS_MUTE_TIME)
                    answer = f"{puser_title}, мат тут запрещен, отдохни {BADWORDS_MUTE_TIME} секунд."
                else:
                    answer = f"@{self.config['master']} У меня в базе нет такого пользователя"
                print(f"!!! Юзер {puser_title} матерился, редиска такая!")
        return answer

    def find_user_id(self, puser_title: str):
        """Ищет в базе ID пользователя по его нику."""
        session = self.database.get_session()
        query = session.query(m_names.CName, m_users.CUser)
        query = query.filter_by(fusername=puser_title)
        query = query.join(m_users.CUser, m_users.CUser.id == m_names.CName.fuserid)
        data = query.first()
        if data is not None:
            return data[1].ftguserid
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
                  puser_title: str, pmessage_text: str) -> str:
        """Процедура разбора запроса пользователя."""
        answer: str = ""
        word_list: list = func.parse_input(pmessage_text)
        if self.can_process(pchat_title, pmessage_text):

            if word_list[0] in MUTE_COMMANDS:

                # *** Молчанка
                period_index: int = MUTE_COMMANDS.index(word_list[0])
                user_title: str = " ".join(word_list[1:])
                mute_time = MUTE_PERIODS[period_index]
                user_id = self.find_user_id(user_title)
                if user_id is not None:

                    if self.is_admin(pchat_id, puser_title):

                        answer = self.mute_user(pchat_id, user_id, user_title,
                                                mute_time, period_index)
                    else:

                        answer = f"Извини, {puser_title}, ты тут не админ..."
                else:

                    answer = f"Кто такой {user_title}? Не знаю его..."
            else:

                if word_list[0] in ADMINISTRATION_CMD:

                    if self.is_admin(pchat_id, puser_title):

                        answer = " ".join(MUTE_COMMANDS)
                        self.administration()
                    else:

                        answer = f"Извини, {puser_title}, ты тут не админ..."
        return answer

    def mute_user(self, pchat_id: int, pmuted_user_id: int, pmuted_user_title: str,
                  pmute_time: int, pperiod_index: int):
        """Отобрать голос у пользователя."""
        self.bot.restrict_chat_member(pchat_id, pmuted_user_id, until_date=time() + pmute_time)
        if pmute_time == UNMUTE_PERIOD:

            answer = f"{pmuted_user_title}, через {UNMUTE_PERIOD} секунд можете разговаривать."
        else:

            answer = f"{pmuted_user_title}, помолчите {MUTE_PERIODS_TITLES[pperiod_index]}, " \
                     "подумайте..."
        return answer

    def is_admin(self, pchat_id: int, puser_title: str):
        """Возвращает True, если пользователь является админом данного чата, иначе False."""
        found = False
        data = self.bot.get_chat_administrators(pchat_id)

        for item in data:

            user = item.user
            user_name = user.first_name
            if user.last_name is not None:
                user_name += " " + user.last_name
            if user_name == puser_title:
                found = True
                break
        return found

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

    def administration(self):
        """Выводит список пользователей для модерирования."""
