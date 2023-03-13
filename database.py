# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Модуль функций, связанных с БД."""
# import sys

from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import m_ancestor
# import m_karma  # noqa
import m_chats  # noqa
import m_names  # noqa
import m_penalties  # noqa
import m_stat  # noqa
import m_users  # noqa

# py lint: disable=C0301
# py lint: disable=line-too-long

DATABASE_VERSION: int = 1
DATABASE_NAME: str = "softice.db"


class CDataBase:
    """Класс."""
    def __init__(self, pconfig, pdata_path, pdatabase_name=DATABASE_NAME):
        """Конструктор класса."""
        # super(CMainWindow, self).__init__()
        self.application_folder = Path.cwd()
        self.config = pconfig
        self.data_path = pdata_path
        self.session = None
        self.engine = None
        self.database_name = pdatabase_name
        self.connect()

    def check(self):
        """Проверяет базу на соответствие ее структуры классам."""

    def connect(self):
        """Устанавливает соединение с БД."""
        alchemy_echo: bool = self.config["alchemy_echo"] == "1"
        self.engine = create_engine('sqlite:///' + self.data_path + self.database_name,
                                    echo=alchemy_echo,
                                    connect_args={'check_same_thread': False})
        Session = sessionmaker()
        Session.configure(bind=self.engine)
        self.session = Session()
        m_ancestor.Base.metadata.bind = self.engine

    def create(self):
        """Создает или изменяет БД в соответствии с описанной в классах структурой."""
        m_ancestor.Base.metadata.create_all()
        # information = c_inform.CInformation(DATABASE_VERSION)
        # self.session.add(information)
        # for context in STANDARD_CONTEXTS:
        #
        #     context_object = c_context.CContext(context)
        #     self.session.add(context_object)
        # tag_object = c_tag.CTag(EMPTY_TAG)
        # print("DB:CR:tag ", tag_object)
        # self.session.add(tag_object)
        self.session.commit()

    def disconnect(self):
        """Разрывает соединение с БД."""
        self.session.close()
        self.engine.dispose()

    def exists(self):
        """Проверяет наличие базы данных по пути в конфигурации."""
        return Path(self.data_path + self.database_name).exists()

    def get_session(self):
        """Возвращает экземпляр session."""
        return self.session
