# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Модуль класса модели таблицы справочника ID пользователей телеграмма."""

from sqlalchemy import Column, Integer

import m_ancestor


class CUser(m_ancestor.CAncestor):
    """Класс модели таблицы справочника ID пользователей телеграмма."""

    __tablename__ = 'tbl_users'
    ftguserid = Column(Integer,
                       nullable=False,
                       unique=True,
                       index=True)

    def __init__(self, ptguserid: int):
        """Конструктор"""
        super().__init__()
        self.ftguserid = ptguserid

    def __repr__(self):
        ancestor_repr = super().__repr__()
        return f"""{ancestor_repr},
                   TG user ID:{self.ftguserid}"""
    def null(self):
        """Чтоб линтер был щаслив."""
