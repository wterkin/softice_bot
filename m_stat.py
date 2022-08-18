# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Модуль класса статистики."""

from sqlalchemy import Column, Integer, ForeignKey

import m_ancestor
import m_chats
import m_users


class CStat(m_ancestor.CAncestor):
    """Класс статистики."""

    __tablename__ = 'tbl_stat'
    fuserid = Column(Integer, ForeignKey(m_users.CUser.id))
    fchatid = Column(Integer, ForeignKey(m_chats.CChat.id))
    fletters = Column(Integer, default=0)
    fwords = Column(Integer, default=0)
    fphrases = Column(Integer, default=0)
    fstickers = Column(Integer, default=0)
    fpictures = Column(Integer, default=0)
    faudios = Column(Integer, default=0)
    fvideos = Column(Integer, default=0)

    def __init__(self, puserid: int, pchatid: int, pletters: int, pwords: int, pphrases: int,
                 pstickers: int, ppictures: int, paudios: int, pvideos: int):
        """Конструктор"""
        super().__init__()
        self.fuserid = puserid
        self.fchatid = pchatid
        self.fletters = pletters
        self.fwords = pwords
        self.fphrases = pphrases
        self.fstickers = pstickers
        self.fpictures = ppictures
        self.faudios = paudios
        self.fvideos = pvideos

    def __repr__(self):
        ancestor_repr = super().__repr__()
        return f"""{ancestor_repr},
                   User id:{self.fuserid}
                   Letters:{self.fletters},
                   Words: {self.fwords},
                   Sentences: {self.fphrases},
                   Stickers: {self.fstickers},
                   Pictures: {self.fpictures},
                   Audios: {self.faudios},
                   Videos: {self.fvideos}"""
