# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Модуль функций, связанных с БД."""
# import sys

from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# from sqlalchemy import and_, or_

import c_config

# *** Классы таблиц
import c_inform
import c_ancestor
import c_context
import c_tag
# import c_task as ctsk

# py lint: disable=C0301
# py lint: disable=line-too-long

DATABASE_VERSION = 1

STANDARD_CONTEXTS = ("Дом", "DIY", "Работа")
EMPTY_TAG = "<Пусто>"


class CDataBase():
    """Класс."""
    def __init__(self, p_config):
        """Конструктор класса."""
        # super(CMainWindow, self).__init__()
        self.application_folder = Path.cwd()
        self.config = p_config
        self.session = None
        self.engine = None
        self.connect()

    def check(self):
        """Проверяет базу на соответствие ее структуры классам."""

    def connect(self):
        """Устанавливает соединение с БД."""
        database_path: str = self.config.restore_value(c_config.DATABASE_FILE_KEY)
        # print("CDB:CNN:DBP ", database_path)
        self.engine = create_engine('sqlite:///'+database_path, echo=False)
        session = sessionmaker()
        session.configure(bind=self.engine)
        self.session = session()

        c_ancestor.Base.metadata.bind = self.engine

    def create(self):
        """Создает или изменяет БД в соответствии с описанной в классах структурой."""
        c_ancestor.Base.metadata.create_all()
        information = c_inform.CInformation(DATABASE_VERSION)
        self.session.add(information)
        for context in STANDARD_CONTEXTS:

            context_object = c_context.CContext(context)
            self.session.add(context_object)
        tag_object = c_tag.CTag(EMPTY_TAG)
        print("DB:CR:tag ", tag_object)
        self.session.add(tag_object)
        self.session.commit()

    def disconnect(self):
        """Разрывает соединение с БД."""
        self.session.close()
        self.engine.dispose()

    def exists(self):
        """Проверяет наличие базы данных по пути в конфигурации."""
        db_folder_path = Path(self.config.restore_value(c_config.DATABASE_FILE_KEY))
        return db_folder_path.exists()

    def get_session(self):
        """Возвращает экземпляр session."""
        return self.session

    # def upgrade(self, revision, context):
    #     """Приводит структуру базы в соответствие с классами Alchemy."""
    #     return self.alembic_script._upgrade_revs(script.get_heads(), revision)
