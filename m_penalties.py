# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Модуль класса справочника событий."""

from sqlalchemy import Date, Column, Integer, ForeignKey

import m_ancestor
import m_users
from datetime import datetime
MUTE_PENALTY = 1
BAN_PENALTY = 2
RUSSIAN_DATETIME_FORMAT = "%d.%m.%Y %H:%M:%S"


class CPenalty(m_ancestor.CAncestor):
    """Класс справочника тэгов."""

    __tablename__ = 'tbl_penalties'
    fuserid = Column(Integer, ForeignKey(m_users.CUser.id))
    ftype: int = Column(Integer, default=0) # 1 - mute, 2 - ban
    fendsat: datetime = Column(Date, nullable=False)

    def __init__(self, ptype: int, pends_at: datetime):
        """Конструктор"""
        super().__init__()
        self.ftype = ptype
        self.fendsat = pends_at

    def __repr__(self):
        ancestor_repr = super().__repr__()
        return f"""{ancestor_repr},
                   Penalty type:{self.ftype}
                   Penalty ends at:{self.fendsat.strftime(RUSSIAN_DATETIME_FORMAT)}"""
