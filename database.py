# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Модуль функций, связанных с БД."""
from datetime import datetime
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Date, MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

# py lint: disable=C0301
# py lint: disable=line-too-long

DATABASE_VERSION: int = 1
DATABASE_NAME: str = "softice.db"
STATUS_ACTIVE: int = 1
STATUS_INACTIVE: int = 0

STATUSERID: str = "userid"
STATLETTERS: str = "letters"
STATWORDS: str = "words"
STATPHRASES: str = "phrases"
STATPICTURES: str = "pictures"
STATSTICKERS: str = "stickers"
STATAUDIOS: str = "audios"
STATVIDEOS: str = "videos"

MUTE_PENALTY = 1
BAN_PENALTY = 2
RUSSIAN_DATETIME_FORMAT = "%d.%m.%Y %H:%M:%S"


convention = {
    "all_column_names": lambda constraint, table: "_".join([
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


# def __init__(self, puserid: int, pchatid: int, pletters: int, pwords: int, pphrases: int,
#              pstickers: int, ppictures: int, paudios: int, pvideos: int):

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

    def null(self):
        """Чтоб линтер был щаслиф."""


class CChat(CAncestor):
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


class CUser(CAncestor):
    """Класс модели таблицы справочника ID пользователей телеграмма."""

    __tablename__ = 'tbl_users'
    ftguserid = Column(Integer,
                       nullable=False,
                       unique=True,
                       index=True)

    def __init__(self, ptguserid: int):
        """Конструктор"""
        super().__init__()
        self.ftguserid = ptguserid

    def __repr__(self):
        ancestor_repr = super().__repr__()
        return f"""{ancestor_repr},
                   TG user ID:{self.ftguserid}"""

    def null(self):
        """Чтоб линтер был щаслив."""


class CName(CAncestor):
    """Класс модели таблицы связки имен и ID пользователей."""

    __tablename__ = 'tbl_names'
    fuserid = Column(Integer, ForeignKey(CUser.id))
    fusername = Column(String,
                       nullable=False,
                       )

    def __init__(self, puserid: int, pusername: str):
        """Конструктор"""
        super().__init__()
        self.fuserid = puserid
        self.fusername = pusername

    def __repr__(self):
        ancestor_repr = super().__repr__()
        return f"""{ancestor_repr},
                   User ID:{self.fuserid}, 
                   User name:{self.fusername}"""


class CStat(CAncestor):
    """Класс статистики."""

    __tablename__ = 'tbl_stat'
    fuserid = Column(Integer, ForeignKey(CUser.id))
    fchatid = Column(Integer, ForeignKey(CChat.id))
    fletters = Column(Integer, default=0)
    fwords = Column(Integer, default=0)
    fphrases = Column(Integer, default=0)
    fstickers = Column(Integer, default=0)
    fpictures = Column(Integer, default=0)
    faudios = Column(Integer, default=0)
    fvideos = Column(Integer, default=0)

    def __init__(self, puserid: int, pchatid: int, pdata_dict: dict):
        """Конструктор"""
        super().__init__()
        self.fuserid = puserid
        self.fchatid = pchatid
        self.set_all_fields(pdata_dict)
        # self.fletters = pletters
        # self.fwords = pwords
        # self.fphrases = pphrases
        # self.fstickers = pstickers
        # self.fpictures = ppictures
        # self.faudios = paudios
        # self.fvideos = pvideos

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


class CPenalty(CAncestor):
    """Класс модели таблицы проскрипций."""

    __tablename__ = 'tbl_penalties'
    fuserid = Column(Integer, ForeignKey(CUser.id))
    fchatid = Column(Integer, ForeignKey(CChat.id))
    ftype: int = Column(Integer, default=0) # 1 - mute, 2 - ban
    fendsat: datetime = Column(Date, nullable=False)

    def __init__(self, puser_id: int, pchat_id: int, ptype: int, pends_at: datetime):
        """Конструктор"""
        super().__init__()
        self.fuserid = puser_id
        self.fchatid = pchat_id
        self.ftype = ptype
        self.fendsat = pends_at

    def __repr__(self):
        ancestor_repr = super().__repr__()
        return f"""{ancestor_repr},
                   User ID:{self.fuserid}
                   Chat ID:{self.fchatid}
                   Penalty type:{self.ftype}
                   Penalty ends at:{self.fendsat.strftime(RUSSIAN_DATETIME_FORMAT)}"""


class CDataBase:
    """Класс."""

    def __init__(self, pconfig, pdata_path, pdatabase_name=DATABASE_NAME):
        """Конструктор класса."""
        # super(CMainWindow, self).__init__()
        self.application_folder = Path.cwd()
        self.config = pconfig
        self.data_path = pdata_path
        self.session = None
        self.engine = None
        self.database_name = pdatabase_name
        self.connect()

    def check(self):
        """Проверяет базу на соответствие ее структуры классам."""

    def connect(self):
        """Устанавливает соединение с БД."""
        alchemy_echo: bool = self.config["alchemy_echo"] == "1"
        self.engine = create_engine('sqlite:///' + self.data_path + self.database_name,
                                    echo=alchemy_echo,
                                    connect_args={'check_same_thread': False})
        Session = sessionmaker()
        Session.configure(bind=self.engine)
        self.session = Session()
        Base.metadata.bind = self.engine

    def create(self):
        """Создает или изменяет БД в соответствии с описанной в классах структурой."""
        Base.metadata.create_all()
        # information = c_inform.CInformation(DATABASE_VERSION)
        # self.session.add(information)
        # for context in STANDARD_CONTEXTS:
        #
        #     context_object = c_context.CContext(context)
        #     self.session.add(context_object)
        # tag_object = c_tag.CTag(EMPTY_TAG)
        # print("DB:CR:tag ", tag_object)
        # self.session.add(tag_object)
        self.session.commit()

    def disconnect(self):
        """Разрывает соединение с БД."""
        self.session.close()
        self.engine.dispose()

    def exists(self):
        """Проверяет наличие базы данных по пути в конфигурации."""
        return Path(self.data_path + self.database_name).exists()

    def get_session(self):
        """Возвращает экземпляр session."""
        return self.session
