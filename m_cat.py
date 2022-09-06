# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Модуль класса справочника чатов."""

from sqlalchemy import Column, Integer, String

import m_ancestor
import m_users

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

class CInterior(m_ancestor.CAncestor):
    """Класс моделей для игры в кошек."""

    __tablename__ = 'tbl_interior'
    fcolor = Column(String, nullable=False)
    fwooliness = Column(Integer, nullable=False)
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
    fuserid = Column(Integer, ForeignKey(m_users.CUser.id))
    fname = Column(String, nullable=False, default="Мурзик")
    fcolor = Column(String, nullable=False)
    fwooliness = Column(String, nullable=False)
    fbreed = Column(String, nullable=False)
    fhealth = Column(Integer, nullable=False, default=25)
    fstrength = Column(Integer, nullable=False, default=1)
    fsatiety = Column(Integer, nullable=False, default=25)
    fmood = Column(Integer, nullable=False, default=25)
    fdiscipline = Column(Integer, nullable=False, default=25)

    def __init__(self, pname: str, pprice: int):
        """Конструктор"""
        super().__init__()

    def __repr__(self):
        ancestor_repr = super().__repr__()
        return f"""{ancestor_repr},
                   Name:{self.fname},
                   Color:{self.fcolor},
                   Wooliness:{self.fwooliness},
                   Breed:{self.fbreed},
                   Health:{self.fhealth},
                   Strength:{self.fstrength},
                   Satiety:{self.fsatiety},
                   Mood:{self.fmood},
                   Discipline:{self.fdiscipline},
                   Exterior:{self.fexterior}
                   """

