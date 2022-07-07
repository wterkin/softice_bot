# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Модуль класса справочника событий."""

from sqlalchemy import MetaData, Column, Integer, ForeignKey, String
from sqlalchemy.ext.declarative import declarative_base
import users

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


class CUserKarma(Base):
    """Класс справочника тэгов."""

    __tablename__ = 'tbl_karma'
    id = Column(Integer,
                autoincrement=True,
                nullable=False,
                primary_key=True,
                unique=True)
    fkarma = Column(Integer, default=0)
    fstatus = Column(Integer,
                     nullable=False,
                     )

    def __init__(self, pkarma: str):
        """Конструктор"""
        super().__init__()
        self.fkarma = pkarma

    def __repr__(self):
        return f"""User karma:{self.fkarma}, status:{self.fstatus}"""
