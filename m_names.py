# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Модуль класса справочника событий."""

from sqlalchemy import Column, String, Integer, ForeignKey

import m_ancestor
import m_users


class CName(m_ancestor.CAncestor):
    """Класс справочника тэгов."""

    __tablename__ = 'tbl_names'
    fuserid = Column(Integer, ForeignKey(m_users.CUser.id))
    fname = Column(String,
                   nullable=False,
                   )

    def __init__(self, pusername: str):
        """Конструктор"""
        super().__init__()
        self.fusername = pusername

    def __repr__(self):
        ancestor_repr = super().__repr__()
        return f"""{ancestor_repr},
                   TG user ID:{self.fuserid}, 
                   User name:{self.fname}"""
