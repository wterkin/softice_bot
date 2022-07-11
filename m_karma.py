# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Модуль класса модели таблицы кармы."""

from sqlalchemy import MetaData, Column, Integer, ForeignKey

import m_ancestor
import m_chats
import m_users


class CKarma(m_ancestor.CAncestor):
    """Класс модели таблицы кармы."""

    __tablename__ = 'tbl_karma'
    fuserid = Column(Integer, ForeignKey(m_users.CUser.id))
    fchatid = Column(Integer, ForeignKey(m_chats.CChat.id))
    fkarma = Column(Integer, default=0)

    def __init__(self, puserid: int, pchatid: int, pkarma: str):
        """Конструктор"""
        super().__init__()
        self.fuserid = puserid
        self.fchatid = pchatid
        self.fkarma = pkarma

    def __repr__(self):
        ancestor_repr = super().__repr__()
        return f"""{ancestor_repr},
                   User id:{self.fuserid}
                   Chat id:{self.fchatid}
                   User karma:{self.fkarma}"""
