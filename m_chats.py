# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Модуль класса справочника чатов."""

from sqlalchemy import Column, Integer

import m_ancestor


class CChat(m_ancestor.CAncestor):
    """Класс справочника чатов."""

    __tablename__ = 'tbl_chats'
    fchatid = Column(Integer,
                     nullable=False,
                     unique=True,
                     index=True)

    def __init__(self, pchatid: int):
        """Конструктор"""
        super().__init__()
        self.fchatid = pchatid

    def __repr__(self):
        ancestor_repr = super().__repr__()
        return f"""{ancestor_repr},
                   Chat ID:{self.fchatid}"""
