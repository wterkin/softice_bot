# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Модуль статистики для бота."""

# from pathlib import Path
import prototype
import functions
# import database
import m_chats
import m_users
# from sys import platform
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker

import m_ancestor

HINT = ["стат", "stat"]
COMMANDS = ["топ10", "топ25", "топ50", "перс", "top10", "top25", "top50", "pers"]
ENABLED_IN_CHATS_KEY = "statistic_chats"


class CStatistic(prototype.CPrototype):
    """Класс метеоролога."""

    def __init__(self, pconfig, pdatabase):
        super().__init__()
        self.config = pconfig
        self.database = pdatabase
        # self.application_folder = Path.cwd()
        # database_path = self.config[database.get_db_path_key()]
        # if Path(database_path).exists():
        #
        #     self.engine = create_engine('sqlite:///'+database_path,
        #                                 echo=False,
        #                                 connect_args={'check_same_thread': False})
        #     session = sessionmaker()
        #     session.configure(bind=self.engine)
        #     self.session = session()
        #     m_ancestor.Base.metadata.bind = self.engine
        #
        # else:
        #
        #     raise IOError

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
        return pchat_title in self.config[ENABLED_IN_CHATS_KEY]

    def reload(self):
        """Вызывает перезагрузку внешних данных модуля."""

    def save_message(self, pmessage):
        """Сохраняет фразу, произнесенную пользователем, в базе."""
        # print(pmessage)
        message_text: str = pmessage.text
        tg_chat_id: int = pmessage.chat.id
        tg_chat_title: str = pmessage.chat.title
        user_id: int = pmessage.from_user.id
        user_name: str = pmessage.from_user.username
        user_title: str = pmessage.from_user.first_name

        # проверить, нет ли юзера в таблице имен, если нет - добавить и получить id
        # если есть - получить id

        # проверить, нет ли чата в таблице чатов
        query = self.database.get_session().query(m_chats.CChat)
        query = query.filter_by(fchatid=tg_chat_id)
        data = query.first()
        if data is None:

            # если нет - добавить, и получить id
            chat = m_chats.CChat(tg_chat_id)
            self.database.get_session().add(chat)
            self.database.get_session().commit()
            chat_id = chat.id
        else:

            chat_id = data.id
        print("STT:SM:CHAT ID: ", chat_id)
        # проверить, нет ли юзера в таблице тг юзеров, если нет - добавить и получить id
        query = self.database.get_session().query(m_users.CUser)
        query = query.filter_by(fchatid=user_id)
        data = query.first()
        if data is None:

            # если нет - добавить, и получить id
            user = m_users.CUser(user_id)
            self.database.get_session().add(user)
            self.database.get_session().commit()
            user_id = user.id
        else:

            user_id = data.id
        print("STT:SM:USER ID: ", user_id)

        # если есть - получить id
        # if tg_chat_id.count() == 0:
        #
        #     #
        #     chat = m_chats.CChat(chat_id)
        #     self.database.get_session().add(chat)
        #     self.database.get_session().commit()
        #     print(f"{chat_title}:{chat_id}:{chat}")
        #     # else:
        #     #     # если есть - получить id
        #     # query =
        #     # print(tg_chat_id.all())
        #
        # # tg_id_data = self.database.get_session().query(m_users.CUser).filter_by(ftguserid=user_id)
        # # if tg_id_data.count() == 0:
        # select seq
        # from sqlite_sequence where
        # name = "table_name"
        # me = User(nickname, email, passw)
        #     db.session.add(me)
        #     db.session.commit()
        #     print(me.id)
