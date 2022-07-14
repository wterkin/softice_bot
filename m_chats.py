# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Модуль класса справочника чатов."""

from sqlalchemy import Column, Integer, String

import m_ancestor


class CChat(m_ancestor.CAncestor):
    """Класс справочника чатов."""

    __tablename__ = 'tbl_chats'
    fchatid = Column(Integer,
                     nullable=False,
                     unique=True,
                     index=True)
    fchatname = Column(String,
                       nullable=False,
                       )

    def __init__(self, pchat_id: int, pchat_name: str):
        """Конструктор"""
        super().__init__()
        self.fchatid = pchat_id
        self.fchatname = pchat_name

    def __repr__(self):
        ancestor_repr = super().__repr__()
        return f"""{ancestor_repr},
                   Chat ID:{self.fchatid}
                   Chat Name:{self.fchatname}"""
