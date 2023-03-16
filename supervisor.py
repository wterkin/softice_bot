# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Модуль для контроля над чатом."""
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, MetaData, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
import functions as func
import prototype

# import threading
# convention: Optional[Dict[str, str]] = {
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

DATA_FOLDER: str = "supervisor"
DATABASE_NAME: str = "users.db"
STATUS_ACTIVE: int = 1
STATUS_INACTIVE: int = 0
NEW_USER_RATING: int = 2
MINIMAL_TEXT_RATING: int = 2
MINIMAL_STICKER_RATING: int = 3
MINIMAL_PHOTO_RATING: int = 4
MINIMAL_AUDIO_RATING: int = 5
MINIMAL_VIDEO_RATING: int = 6
KARMA_UPPER_LIMIT: int = 50
ENABLED_IN_CHATS_KEY: str = "supervisor_chats"
COMMANDS: list = ["svon", "svoff", "rt+", "rt-", "rt="]

meta_data: MetaData = MetaData(naming_convention=convention)
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

    def null(self):
        """Чтоб линтер был щаслиф."""


class CUser(CAncestor):
    """Класс модели таблицы справочника ID пользователей телеграмма."""

    __tablename__ = 'tbl_users'
    fuserid = Column(Integer,
                     nullable=False,
                     unique=False,
                     index=True)
    fusername = Column(String)
    fchatid = Column(Integer)
    fchatname = Column(String)
    frating = Column(Integer, default=NEW_USER_RATING)
    fkarma = Column(Integer, default=0)
    fadmin = Column(Boolean, default=False)

    def __init__(self, puserid: int, pusername: str, pchatid: int, pchatname: str):
        """Конструктор"""
        super().__init__()
        self.fuserid = puserid
        self.fusername = pusername
        self.fchatid = pchatid
        self.fchatname = pchatname

    def __repr__(self):
        ancestor_repr = super().__repr__()
        return f"""{ancestor_repr},
                   user ID :{self.fuserid}
                   user name :{self.fchatname}
                   chat ID :{self.fchatid}
                   chat ID :{self.fchatname}
                   user rating :{self.frating}
                   user karma: {self.fkarma} """

    def null(self):
        """Чтоб линтер был щаслиф."""


class CSupervisor(prototype.CPrototype):
    """ Класс смотрителя за чатом."""
    def __init__(self, pbot, pconfig, pdata_path: str):
        super().__init__()
        self.config = pconfig
        self.data_path: str = pdata_path + DATA_FOLDER + "/"
        self.busy: bool = False
        self.bot = pbot
        self.state = False
        self.admins: dict = {}
        self.create_admin_list()
        # *** Коннектимся к базе
        self.connect_database()
        self.session = None

    def add_user(self, puser_id: int, puser_name: str, pchat_id: int, pchat_title: str):
        """Добавляет в базу нового пользователя"""
        user = CUser(puser_id, puser_name, pchat_id, pchat_title)
        # *** Если кто-то уже залочил базу, подождём
        while self.busy:
            pass
        # *** Лочим запись в базу и пишем сами
        self.busy = True
        # *** Пишем
        self.session.add(user)
        self.session.commit()
        # *** Запись окончена, разлочиваем базу
        self.busy = False
        return user.id

    def can_process(self, pchat_title: str, pmessage_text: str) -> bool:
        """Возвращает True, если модуль может обработать команду."""
        return self.is_enabled(pchat_title)

    def connect_database(self):
        """Процедура, осуществляющее соединение с БД."""
        database_file_name = Path(self.data_path) / DATABASE_NAME
        alchemy_echo: bool = self.config["alchemy_echo"] == "1"
        engine = create_engine('sqlite:///' + str(database_file_name),
                               echo=alchemy_echo,
                               connect_args={'check_same_thread': False})
        Session = sessionmaker()  # noqa
        Session.configure(bind=engine)
        self.session = Session()
        Base.metadata.bind = engine
        # *** Если базы нет - создаем
        if not database_file_name.exists():
            Base.metadata.create_all()
            print("* БД супервизора создана.")

    def create_admin_list(self):
        """Создаёт двумерный список админов чатов."""

        for chat_name in self.config[ENABLED_IN_CHATS_KEY]:

            self.admins[chat_name] = []

    def delete_message(self, pmessage):
        """Удаляет сообщение пользователя."""
        # self.bot.delete_message(chat_id=pmessage.chat.id, message_id=pmessage.message_id)
        # print(f"> Сообщение пользователя {pmessage.from_user.username} в чате "
        # f"'{pmessage.chat.title}' удалено.")

    def get_chat_admin_list(self, pchat_id):
        """Возвращает список админов указанного чата."""
        return self.bot.get_chat_administrators(pchat_id)

    def get_help(self, pchat_title: str) -> str:
        """Возвращает список команд модуля, доступных пользователю."""
        return ""

    def get_hint(self, pchat_title: str) -> str:
        """Возвращает команду верхнего уровня, в ответ на которую
           модуль возвращает полный список команд, доступных пользователю."""
        return ""  # , ".join(HINT)

    def get_user(self, pchat_id: int, puser_id: int):
        """Если пользователь уже есть в базе, возвращает его ID, если нет - None."""
        query = self.session.query(CUser)
        # query = self.database
        query = query.filter_by(fchat_id=pchat_id, fuserid=puser_id)
        data = query.first()
        if data is not None:

            return data
        return None

    def increment_karma(self, pmessage):
        """Увеличивает счётчик кармы на 1, если карма переполнится - увеличивает рейтинг."""
        user: CUser = self.get_user(pmessage.chat.id, pmessage.from_user.id)
        if user.fkarma < (KARMA_UPPER_LIMIT * user.frating):

            user.fkarma += 1
        else:

            user.frating += 1
            user.fkarma = 0
        # *** Если кто-то уже залочил базу, подождём
        while self.busy:

            pass
        # *** Лочим запись в базу и пишем сами
        self.busy = True
        # *** Пишем
        self.session.add(user)
        self.session.commit()
        # *** Запись окончена, разлочиваем базу
        self.busy = False

    def is_admin(self, pchat_id: int, puser_id: str):
        """Возвращает True, если пользователь является админом данного чата, иначе False."""

        # member = self.bot.get_chat_member(pchat_id, puser_id)
        # return member.is_chat_admin()
        # pass

    def is_enabled(self, pchat_title: str) -> bool:
        """Возвращает True, если на этом канале этот модуль разрешен."""
        return pchat_title in self.config[ENABLED_IN_CHATS_KEY]

    def is_master(self, puser_name, puser_title):
        """Проверяет, является ли пользователь хозяином бота."""

        if puser_name == self.config["master"]:

            return True, ""
        return False, f"У вас нет на это прав, {puser_title}."

    def reload(self):
        """ Заглушка. """

    def process_commands(self, pmessage):
        """Обрабатывает команды пользователя."""
        answer: str = ""
        word_list: list = func.parse_input(pmessage.text)
        if self.can_process(pmessage.chat.title, pmessage.text):

            # *** Получим код команды
            command = func.get_command(word_list[0], COMMANDS)
            if command == 0:

                # *** Включить супервизор
                if self.is_master(pmessage.from_user.username, pmessage.from_user.first_name):

                    if not self.state:
                        self.state = True
                        print("* Супервизор активирован.")
                        answer = "Супервизор активирован."
            elif command == 1:
                # *** Выключить супервизор
                if self.is_master(pmessage.from_user.username, pmessage.from_user.first_name):

                    if self.state:
                        self.state = True
                        print("* Супервизор деактивирован.")
                        answer = "Супервизор деактивирован."
            elif command == 2:
                # *** Увеличить рейтинг на 1
                # reply_to_message
                pass
            elif command == 3:
                # *** Уменьшить рейтинг на 1
                pass
            elif command == 4:
                # *** Установить рейтинг
                pass
        return answer

    def supervisor(self, pmessage):
        """Контролирует поведение людей в чате."""
        answer: str = ""
        # user_id: int
        # print(self.is_admin(pmessage.chat.id, pmessage.from_user.id))
        # # *** Если это ответ на сообщение..
        if pmessage.reply_to_message is not None:

            # from_part = pmessage.reply_to_message.json["from"]
            # *** ..получим ID пользователя, отправившего оригинальное сообщение
            # user_id = pmessage.reply_to_message.json["from"]["id"]
            # print(user_id)
            pass
        if pmessage.content_type == "text":

            answer = self.process_commands(pmessage)
        if self.state:

            # print(pmessage)
            if self.is_enabled(pmessage.chat.title):

                user: CUser = self.get_user(pmessage.chat.id, pmessage.from_user.id)
                if user is not None:

                    if pmessage.content_type == "text":

                        if user.frating < MINIMAL_TEXT_RATING:

                            self.delete_message(pmessage)
                        else:

                            self.increment_karma(pmessage)
                    elif pmessage.content_type == "sticker":

                        if user.frating < MINIMAL_STICKER_RATING:

                            self.delete_message(pmessage)
                        else:

                            self.increment_karma(pmessage)
                    elif pmessage.content_type == "photo":

                        if user.frating < MINIMAL_PHOTO_RATING:

                            self.delete_message(pmessage)
                        else:

                            self.increment_karma(pmessage)
                    elif pmessage.content_type in ["voice", "audio"]:

                        if user.frating < MINIMAL_AUDIO_RATING:

                            self.delete_message(pmessage)
                        else:

                            self.increment_karma(pmessage)
                    elif pmessage.content_type in ["video", "video_note"]:

                        if user.frating < MINIMAL_VIDEO_RATING:

                            self.delete_message(pmessage)
                        else:

                            self.increment_karma(pmessage)
                else:

                    name: str = pmessage.from_user.first_name + " "
                    if pmessage.from_user.last_name is not None:

                        name += pmessage.from_user.last_name
                        print(f"! {name}")
                    self.add_user(pmessage.from_user.id, name,
                                  pmessage.chat.id,
                                  pmessage.chat.title)
        return answer
