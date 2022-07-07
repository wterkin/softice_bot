# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Модуль класса справочника событий."""

from sqlalchemy import Column, Integer

import m_ancestor


class CUser(m_ancestor.CAncestor):
    """Класс справочника тэгов."""

    __tablename__ = 'tbl_users'
    ftguserid = Column(Integer,
                       nullable=False,
                       unique=True)

    def __init__(self, ptguserid: str):
        """Конструктор"""
        super().__init__()
        self.ftguserid = ptguserid

    def __repr__(self):
        ancestor_repr = super().__repr__()
        return f"""{ancestor_repr},
                   TG user ID:{self.ftguserid}"""
