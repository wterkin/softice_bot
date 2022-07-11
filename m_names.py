# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Модуль класса модели таблицы связки ID и имен пользователей."""

from sqlalchemy import Column, String, Integer, ForeignKey

import m_ancestor
import m_users


class CName(m_ancestor.CAncestor):
    """Класс модели таблицы связки имен и ID пользователей."""

    __tablename__ = 'tbl_names'
    fuserid = Column(Integer, ForeignKey(m_users.CUser.id))
    fname = Column(String,
                   nullable=False,
                   )

    def __init__(self, puserid: int, pusername: str):
        """Конструктор"""
        super().__init__()
        self.fuserid = puserid
        self.fusername = pusername

    def __repr__(self):
        ancestor_repr = super().__repr__()
        return f"""{ancestor_repr},
                   User ID:{self.fuserid}, 
                   User name:{self.fname}"""
