# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Модуль класса справочника событий."""

from sqlalchemy import MetaData, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

import c_ancestor as anc

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


class CUser(Base):
    """Класс справочника тэгов."""

    __tablename__ = 'tbl_users'
    id = Column(Integer,
                autoincrement=True,
                nullable=False,
                primary_key=True,
                unique=True)
    ftguserid = Column(Integer,
                       nullable=False,
                       unique=True)
    fstatus = Column(Integer,
                     nullable=False,
                     )

    def __init__(self, puserid: str):
        """Конструктор"""
        super().__init__()
        self.fuserid = puserid

    def __repr__(self):
        ancestor_repr = super().__repr__()
        return f"""User ID:{self.fuserid}, fstatus:{self.fstatus}"""
