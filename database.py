# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Модуль функций, связанных с БД."""
# import sys

from pathlib import Path
from sys import platform
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import m_ancestor
import m_karma
import m_names
import m_penalties
import m_stat
import m_users

# py lint: disable=C0301
# py lint: disable=line-too-long

DATABASE_VERSION: int = 1
LINUX_DATABASE_PATH_KEY: str = "linux_db_path"
WINDOWS_DATABASE_PATH_KEY: str = "windows_db_path"


class CDataBase:
    """Класс."""
    def __init__(self, pconfig):
        """Конструктор класса."""
        # super(CMainWindow, self).__init__()
        self.application_folder = Path.cwd()
        self.config = pconfig
        self.session = None
        self.engine = None
        self.connect()

    def check(self):
        """Проверяет базу на соответствие ее структуры классам."""

    def connect(self):
        """Устанавливает соединение с БД."""
        self.engine = create_engine('sqlite:///'+self.get_db_path(), echo=False)
        session = sessionmaker()
        session.configure(bind=self.engine)
        self.session = session()
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
        db_folder_path = self.get_db_path()
        return Path(db_folder_path).exists()

    def get_db_path(self):
        """Возвращает путь к БД в зависимости от ОС."""
        if platform in ("linux", "linux2"):

            return self.config[LINUX_DATABASE_PATH_KEY]
        else:

            return self.config[WINDOWS_DATABASE_PATH_KEY]


    def get_session(self):
        """Возвращает экземпляр session."""
        return self.session
