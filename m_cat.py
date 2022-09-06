# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Модуль класса справочника чатов."""

from sqlalchemy import Column, Integer, String

import m_ancestor


class CFeed(m_ancestor.CAncestor):
    """Класс моделей для игры в кошек."""

    __tablename__ = 'tbl_feed'
    fname = Column(String, nullable=False)
    fprice = Column(Integer, nullable=False)

    def __init__(self, pname: str, pprice: int):
        """Конструктор"""
        super().__init__()
        self.fname = pname
        self.fprice = pprice

    def __repr__(self):
        ancestor_repr = super().__repr__()
        return f"""{ancestor_repr},
                   Chat ID:{self.fname}
                   Chat Name:{self.fprice}"""



class CCat(m_ancestor.CAncestor):
    """Класс модели кошки."""

    __tablename__ = 'tbl_cats'
    fname = Column(String, nullable=False, default="Мурзик")
    fhealth = Column(Integer, nullable=False, default=25)
    fstrength = Column(Integer, nullable=False, default=1)
    fsatiety = Column(Integer, nullable=False, default=25)
    fmood = Column(Integer, nullable=False, default=25)
    fdiscipline = Column(Integer, nullable=False, default=25)
    fexterior = Column(Integer, nullable=False)  # ссылка на справочник внешностей

    def __init__(self, pname: str, pprice: int):
        """Конструктор"""
        super().__init__()

    def __repr__(self):
        ancestor_repr = super().__repr__()
        return f"""{ancestor_repr},
                   Name:{self.fname},
                   Health:{self.fhealth},
                   Strength:{self.fstrength},
                   Satiety:{self.fsatiety},
                   Mood:{self.fmood},
                   Discipline:{self.fdiscipline},
                   Exterior:{self.fexterior}
                   """

