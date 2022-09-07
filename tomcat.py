#! /usr/bin/python3
# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
# Модуль игры в кошек
import prototype
import m_cat
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

"""
Свойства кошки
1. Здоровье.
При охоте или битве уменьшается,
при кормлении или лечении увеличивается
2. Сила.
Увеличивается при игре и охоте. медленно.
3. Сытость.
Увеличивается при кормлении,
уменьшается при игре, охоте и в битве.
4. Настроение
Увеличивается при игре, ласке и кормлении, также после удачной охоты
Уменьшается после шлепка
5. Дисциплина
Увеличивается после шлепка
Уменьшается после нескольких поглаживаний (>2 подряд)
6. Внешность
Задаётся случайно при получении кота

Действия
1. Покормить
2. Погладить
3. Шлёпнуть
4. Отправить охотиться
5. Сделать кусь другому коту
6. Отвесить оплеуху другому коту
7. Устроить махач с другим котом

Инвентарь
1. Монеты
2. Игрушки
3. Корм

Добыча
Муха     -  5 м  3 урон
Кузнечик -  7 м  6 у
Мышонок  - 10 м  9 у
Лягушка  - 12 м 12 у
Мышь     - 15 м 15 у
Хомяк    - 17 м 18 у
Крыса    - 20 м 21 у
Белка    - 30 м 24 у
Хорёк    - 40 м 27 у
Ласка    - 50 м 30 у

Таблица кошек - привязывается к пользователю
Справочник пищи
Справочник игрушек
--Справочник добычи
--Справочник лекарств
"""

CAT_GAME_DB: str = "cat_game.db"


class CTomCat(prototype.CPrototype):
    """Класс игры."""

    def __init__(self, pconfig: dict, pdata_path: str):
        super().__init__()
        self.config: dict = pconfig
        self.busy: bool = False
        self.data_path = pdata_path
        self.engine = None
        self.session = None
        # self.database: database.CDataBase = database.CDataBase(self.config, self.data_path, CAT_GAME_DB)
        # print("** ", self.database.data_path)
        # print("** ", self.database.database_name)
        self.database_connect()
        if not self.database_exists():

            self.database_create()
        # self.session = self.database.get_session()

    def database_connect(self):
        """Устанавливает соединение с БД."""
        self.engine = create_engine('sqlite:///' + self.data_path + CAT_GAME_DB,
                                    echo=False,
                                    connect_args={'check_same_thread': False})
        Session = sessionmaker()
        Session.configure(bind=self.engine)
        self.session = Session()
        m_cat.Base.metadata.bind = self.engine

    def database_create(self):
        """Создает или изменяет БД в соответствии с описанной в классах структурой."""
        m_cat.Base.metadata.create_all()
        self.session.commit()
        # *** Добыча
        prey = m_cat.CPrey("Муха", 5, 3)
        self.session.add(prey)
        prey = m_cat.CPrey("Кузнечик", 7, 6)
        self.session.add(prey)
        prey = m_cat.CPrey("Мышонок", 10, 9)
        self.session.add(prey)
        prey = m_cat.CPrey("Лягушка", 12, 12)
        self.session.add(prey)
        prey = m_cat.CPrey("Хомяк", 17, 18)
        self.session.add(prey)
        prey = m_cat.CPrey("Крыса", 20, 21)
        self.session.add(prey)
        prey = m_cat.CPrey("Белка", 30, 24)
        self.session.add(prey)
        prey = m_cat.CPrey("Хорёк", 40, 27)
        self.session.add(prey)
        prey = m_cat.CPrey("Ласка", 50, 30)
        self.session.add(prey)
        self.session.commit()

    def database_disconnect(self):
        """Разрывает соединение с БД."""
        self.session.close()
        self.engine.dispose()

    def database_exists(self):
        """Проверяет наличие базы данных по пути в конфигурации."""
        return Path(self.data_path + CAT_GAME_DB).exists()

    def reload(self):
        pass

    def is_enabled(self, pchat_title: str) -> bool:
        pass

    def get_hint(self, pchat_title: str) -> str:
        pass

    def get_help(self, pchat_title: str) -> str:
        pass

    def can_process(self, pchat_title: str, pmessage_text: str) -> bool:
        pass
