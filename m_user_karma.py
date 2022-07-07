# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Модуль класса справочника событий."""

from sqlalchemy import MetaData, Column, Integer, ForeignKey

import m_ancestor
import m_users


class CUserKarma(m_ancestor.CAncestor):
    """Класс справочника тэгов."""

    __tablename__ = 'tbl_karma'
    fuserid = Column(Integer, ForeignKey(m_users.CUser.id))
    fkarma = Column(Integer, default=0)

    def __init__(self, pkarma: str):
        """Конструктор"""
        super().__init__()
        self.fkarma = pkarma

    def __repr__(self):
        ancestor_repr = super().__repr__()
        return f"""{ancestor_repr},
                   User id:{self.fuserid}
                   User karma:{self.fkarma}"""
