# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Модели."""
from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, MetaData, DateTime
from sqlalchemy.ext.declarative import declarative_base

STATUS_ACTIVE: int = 1
STATUS_INACTIVE: int = 0

convention = {
    "all_column_names": lambda constraint,
    table: "_".join([
        column.name for column in constraint.columns.values()
    ]),
    "ix": "ix__%(table_name)s__%(all_column_names)s",
    "uq": "uq__%(table_name)s__%(all_column_names)s",
    "cq": "cq__%(table_name)s__%(constraint_name)s",
    "fk": ("fk__%(table_name)s__%(all_column_names)s__"
           "%(referred_table_name)s"),
    "pk": "pk__%(table_name)s"
}

meta_data: object = MetaData(naming_convention=convention)
Base = declarative_base(metadata=meta_data)


class CAncestor(Base):
    """Класс-предок всех классов-моделей таблиц SQLAlchemy."""
    __abstract__ = True
    id = Column(Integer,
                autoincrement=True,
                nullable=False,
                primary_key=True,
                unique=True)
    fstatus = Column(Integer,
                     nullable=False,
                     )

    def __init__(self):
        """Конструктор."""
        self.fstatus = STATUS_ACTIVE

    def __repr__(self):
        return f"""ID:{self.id},
                   Status:{self.fstatus}"""


class CFeed(CAncestor):
    """Класс справочника еды."""

    __tablename__ = 'tbl_feed'
    fname = Column(String, nullable=False)
    fprice = Column(Integer, nullable=False)
    fsatiety = Column(Integer, nullable=False)

    def __init__(self, pname: str, pprice: int, psatiety: int):
        """Конструктор"""
        super().__init__()
        self.fname = pname
        self.fprice = pprice
        self.fsatiety = psatiety

    def __repr__(self):
        ancestor_repr = super().__repr__()
        return f"""{ancestor_repr},
                   Feed:{self.fname},
                   Price:{self.fprice},
                   Satiety:{self.fsatiety}"""


class CToy(CAncestor):
    """Класс справочника игрушек."""

    __tablename__ = 'tbl_toys'
    fname = Column(String, nullable=False)
    fprice = Column(Integer, nullable=False)
    fjoy = Column(Integer, nullable=False)

    def __init__(self, pname: str, pprice: int, pjoy: int):
        """Конструктор"""
        super().__init__()
        self.fname = pname
        self.fprice = pprice
        self.fjoy = pjoy

    def __repr__(self):
        ancestor_repr = super().__repr__()
        return f"""{ancestor_repr},
                   Toy:{self.fname},
                   Price:{self.fprice},
                   Joy:{self.fjoy}"""


class CPrey(CAncestor):
    """Класс справочника добычи."""

    __tablename__ = 'tbl_preys'
    fname = Column(String, nullable=False)
    fworth = Column(Integer, nullable=False)
    fdamage = Column(Integer, nullable=False)

    def __init__(self, pname: str, pworth: int, pdamage: int):
        """Конструктор"""
        super().__init__()
        self.fname = pname
        self.fworth = pworth
        self.fdamage = pdamage

    def __repr__(self):
        ancestor_repr = super().__repr__()
        return f"""{ancestor_repr},
                   Prey:{self.fname},
                   Worth:{self.fworth},
                   Damage:{self.fdamage}"""


class CGameUser(CAncestor):
    """Класс модели таблицы справочника ID пользователей телеграмма."""

    __tablename__ = 'tbl_gameusers'
    fuserid = Column(Integer,
                     nullable=False,
                     unique=True,
                     index=True)
    fusername = Column(String, nullable=False)
    fcoins = Column(Integer, nullable=False, default=5)

    def __init__(self, puserid: int, pusername: str):
        """Конструктор"""
        super().__init__()
        self.fuserid = puserid
        self.fusername = pusername

    def __repr__(self):
        ancestor_repr = super().__repr__()
        return f"""{ancestor_repr},
                   User ID:{self.fuserid},
                   User name:{self.fusername}
                   """


class CCat(CAncestor):
    """Класс кошки."""

    __tablename__ = 'tbl_cats'
    fuser = Column(Integer, ForeignKey(CGameUser.id))
    fname = Column(String, nullable=False, default="Мурзик")
    fcolor = Column(String, nullable=False)
    fwooliness = Column(String, nullable=False)
    fbreed = Column(String, nullable=False)
    fgender = Column(Integer, nullable=False, default=1)
    fhealth = Column(Integer, nullable=False, default=25)
    fstrength = Column(Integer, nullable=False, default=1)
    fsatiety = Column(Integer, nullable=False, default=25)
    fmood = Column(Integer, nullable=False, default=25)
    fdiscipline = Column(Integer, nullable=False, default=25)
    floyalty = Column(Integer, nullable=False, default=25)

    def __init__(self, puser_id: int, pname: str, pcolor: str, pwooliness: str, pbreed: str, pgender: int):
        """Конструктор"""
        super().__init__()
        self.fuserid = puser_id
        self.fname = pname
        self.fcolor = pcolor
        self.fwooliness = pwooliness
        self.fbreed = pbreed
        self.fgender = pgender

    def __repr__(self):
        ancestor_repr = super().__repr__()
        return f"""{ancestor_repr},
                   Name:{self.fname},
                   Color:{self.fcolor},
                   Wooliness:{self.fwooliness},
                   Breed:{self.fbreed},
                   Gender:{self.fgender},
                   Health:{self.fhealth},
                   Strength:{self.fstrength},
                   Satiety:{self.fsatiety},
                   Mood:{self.fmood},
                   Discipline:{self.fdiscipline},
                   Loyalty:{self.floyalty}
                   """


class CFeedLink(CAncestor):
    """Класс таблицы связки еды."""

    __tablename__ = 'tbl_feedlink'
    fuser = Column(Integer, ForeignKey(CGameUser.id))
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


class CToyLink(CAncestor):
    """Класс таблицы связки игрушек."""

    __tablename__ = 'tbl_toylink'
    fuser = Column(Integer, ForeignKey(CGameUser.id))
    ftoy = Column(Integer, ForeignKey(CToy.id))

    def __init__(self, puser: int, ptoy: int):
        """Конструктор"""
        super().__init__()
        self.fuser = puser
        self.ftoy = ptoy

    def __repr__(self):
        ancestor_repr = super().__repr__()
        return f"""{ancestor_repr},
                   User:{self.fuser},
                   Toy:{self.ftoy}"""


class CFeedTimes(CAncestor):
    """Класс таблицы сеансов кормления."""

    __tablename__ = 'tbl_feedtimes'
    fcat = Column(Integer, ForeignKey(CCat.id))
    fdatetime = Column(DateTime, nullable=False)

    def __init__(self, pcat: int, pdate_time: datetime):
        """Конструктор"""
        super().__init__()
        self.fcat = pcat
        self.fdatetime = pdate_time

    def __repr__(self):
        ancestor_repr = super().__repr__()
        return f"""{ancestor_repr},
                   Cat:{self.fcat},
                   Time:{self.fdatetime}"""
