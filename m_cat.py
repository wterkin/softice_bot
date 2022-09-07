# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Модуль класса справочника чатов."""

from sqlalchemy import Column, Integer, String, ForeignKey

import m_ancestor
import m_users


class CFeed(m_ancestor.CAncestor):
    """Класс справочника еды."""

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
                   Feed:{self.fname}
                   Price:{self.fprice}"""


class CToy(m_ancestor.CAncestor):
    """Класс справочника игрушек."""

    __tablename__ = 'tbl_toys'
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
                   Toy:{self.fname}
                   Price:{self.fprice}"""


class CPrey(m_ancestor.CAncestor):
    """Класс справочника добычи."""

    __tablename__ = 'tbl_toys'
    fname = Column(String, nullable=False)
    fworth = Column(Integer, nullable=False)

    def __init__(self, pname: str, pworth: int):
        """Конструктор"""
        super().__init__()
        self.fname = pname
        self.fworth = pworth

    def __repr__(self):
        ancestor_repr = super().__repr__()
        return f"""{ancestor_repr},
                   Prey:{self.fname}
                   Worth:{self.fworth}"""


class CCat(m_ancestor.CAncestor):
    """Класс кошки."""

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

    def __init__(self, puser_id: int, pname: str, pcolor: str, pwooliness: str, pbreed: str):
        """Конструктор"""
        super().__init__()
        self.fuserid = puser_id
        self.fname = pname
        self.fcolor = pcolor
        self.fwooliness = pwooliness
        self.fbreed = pbreed

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
                   """


class CFeedLink(m_ancestor.CAncestor):
    """Класс таблицы связки еды."""

    __tablename__ = 'tbl_feedlink'
    fcat = Column(Integer, ForeignKey(CCat.id))
    ffeed = Column(Integer, ForeignKey(CFeed.id))
    fquantity = Column(Integer, nullable=False, default=1)

    def __init__(self, pcat: int, pfeed: int, pquantity: int):
        """Конструктор"""
        super().__init__()
        self.fcat = pcat
        self.ffeed = pfeed
        self.fquantity = pquantity

    def __repr__(self):
        ancestor_repr = super().__repr__()
        return f"""{ancestor_repr},
                   Cat:{self.fcat},
                   Feed:{self.ffeed},
                   Quant:{self.fquantity}"""


class CToyLink(m_ancestor.CAncestor):
    """Класс таблицы связки игрушек."""

    __tablename__ = 'tbl_toylink'
    fcat = Column(Integer, ForeignKey(CCat.id))
    ftoy = Column(Integer, ForeignKey(CToy.id))

    def __init__(self, pcat: int, ptoy: int, pquantity: int):
        """Конструктор"""
        super().__init__()
        self.fcat = pcat
        self.ftoy = ptoy

    def __repr__(self):
        ancestor_repr = super().__repr__()
        return f"""{ancestor_repr},
                   Cat:{self.fcat},
                   Toy:{self.ftoy}"""

