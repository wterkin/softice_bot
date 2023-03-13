# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Модуль класса статистики."""

from sqlalchemy import Column, Integer, ForeignKey

import m_ancestor
import m_chats
import m_users

STATUSERID: str = "userid"
STATLETTERS: str = "letters"
STATWORDS: str = "words"
STATPHRASES: str = "phrases"
STATPICTURES: str = "pictures"
STATSTICKERS: str = "stickers"
STATAUDIOS: str = "audios"
STATVIDEOS: str = "videos"


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

    def get_all_fields(self):
        """Возвращает словарь с данными класса."""
        fields_dict: dict = {STATUSERID: self.fuserid, STATLETTERS: self.fletters,
                             STATWORDS: self.fwords, STATPHRASES: self.fphrases,
                             STATPICTURES: self.fpictures, STATSTICKERS: self.fstickers,
                             STATAUDIOS: self.faudios,  STATVIDEOS: self.fvideos}
        return fields_dict

    def set_all_fields(self, pdata_dict):
        """Присваивает полям записи данные из словаря."""
        self.fletters = pdata_dict[STATLETTERS]
        self.fwords = pdata_dict[STATWORDS]
        self.fphrases = pdata_dict[STATPHRASES]
        self.fstickers = pdata_dict[STATSTICKERS]
        self.fpictures = pdata_dict[STATPICTURES]
        self.faudios = pdata_dict[STATAUDIOS]
        self.fvideos = pdata_dict[STATVIDEOS]
