# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Модуль для контроля над чатом."""
import functions as func
import prototype
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, MetaData, String
from sqlalchemy.ext.declarative import declarative_base

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
COMMANDS: list = ["svon", "svoff", "rt+", "rt-", "setrt"]

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


class CUser(CAncestor):
    """Класс модели таблицы справочника ID пользователей телеграмма."""

    __tablename__ = 'tbl_users'
    fuserid = Column(Integer,
                     nullable=False,
                     unique=True,
                     index=True)
    fusername = Column(String)
    fchatid = Column(Integer)
    fchatname = Column(String)
    frating = Column(Integer, default=NEW_USER_RATING)
    fkarma = Column(Integer, default=0)

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

    def __init__(self, pbot, pconfig, pdata_path: str):
        super().__init__()
        self.config = pconfig
        self.data_path: str = pdata_path + DATA_FOLDER + "/"
        self.busy: bool = False
        self.bot = pbot
        self.state = False
        # *** Коннектимся к базе
        database_file_name = Path(self.data_path) / DATABASE_NAME
        self.engine = create_engine('sqlite:///' + str(database_file_name),
                                    echo=False,
                                    connect_args={'check_same_thread': False})
        Session = sessionmaker()  # noqa
        Session.configure(bind=self.engine)
        self.session = Session()
        Base.metadata.bind = self.engine
        # *** Если базы нет - создаем
        if not database_file_name.exists():

            print("* БД модератора создана.")
            Base.metadata.create_all()

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

    def delete_message(self, pmessage):
        """Удаляет сообщение пользователя."""
        # self.bot.delete_message(chat_id=pmessage.chat.id, message_id=pmessage.message_id)
        # print(f"> Сообщение пользователя {pmessage.from_user.username} в чате '{pmessage.chat.title}' удалено.")

    def get_command(self, pword: str) -> int:  # noqa
        """Распознает команду и возвращает её код, в случае неудачи - None."""
        assert pword is not None, \
            "Assert: [librarian.get_command] " \
            "No <pword> parameter specified!"
        result: int = -1
        for command_idx, command in enumerate(COMMANDS):

            if pword in command:
                result = command_idx

        if result > (len(COMMANDS) // 2) - 1:
            result = result - len(COMMANDS) // 2

        return result

    def get_help(self, pchat_title: str) -> str:
        """Возвращает список команд модуля, доступных пользователю."""
        return ""

    def get_hint(self, pchat_title: str) -> str:
        """Возвращает команду верхнего уровня, в ответ на которую
           модуль возвращает полный список команд, доступных пользователю."""
        return ""  # , ".join(HINT)

    def get_user(self, puser_id):
        """Если пользователь уже есть в базе, возвращает его ID, если нет - None."""
        query = self.session.query(CUser)
        query = query.filter_by(fuserid=puser_id)
        data = query.first()
        if data is not None:

            return data
        return None

    def increment_karma(self, pmessage):
        """Увеличивает счётчик кармы на 1, если карма переполнится - увеличивает рейтинг."""
        user: CUser = self.get_user(pmessage.from_user.id)
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

    def is_admin(self, pchat_id: int, puser_title: str):
        """Возвращает True, если пользователь является админом данного чата, иначе False."""
        found = False
        data = self.bot.get_chat_administrators(pchat_id)

        for item in data:

            user = item.user
            user_name = user.first_name
            if user.last_name is not None:
                user_name += " " + user.last_name
            if user_name == puser_title:
                found = True
                break
        return found

    def is_enabled(self, pchat_title: str) -> bool:
        """Возвращает True, если на этом канале этот модуль разрешен."""
        return pchat_title in self.config[ENABLED_IN_CHATS_KEY]

    def is_master(self, puser_name, puser_title):
        """Проверяет, является ли пользователь хозяином бота."""

        if puser_name == self.config["master"]:

            return True, ""
        # *** Низзя
        print(f"> Moderator: Запрос на перезагрузку регэкспов матерных выражений от нелегитимного лица {puser_title}.")
        return False, f"У вас нет на это прав, {puser_title}."

    def reload(self):
        """ """

    def supervisor(self, pmessage):
        """Контролирует поведение людей в чате."""
        answer: str = ""
        # print("-"*20)
        # print(pmessage.reply_to_message.json.from.id)
        # print(pmessage.reply_to_message.json.from.first_name)
        # print("-"*20)
        if pmessage.content_type == "text":

            word_list: list = func.parse_input(pmessage.text)
            if self.can_process(pmessage.chat.title, pmessage.text):

                # *** Получим код команды
                command = self.get_command(word_list[0])
                if command == 0:

                    # *** Включить супервизор
                    # Только для админа !!!
                    if not self.state:

                        self.state = True
                        print("* Супервизор включён.")
                elif command == 1:
                    # *** Выключить супервизор
                    # Только для админа !!!
                    if self.state:

                        self.state = True
                        print("* Супервизор выключен.")
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

        if self.state:
            if self.is_enabled(pmessage.chat.title):

                user: CUser = self.get_user(pmessage.from_user.id)
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
                    self.add_user(pmessage.from_user.id, name, pmessage.chat.id, pmessage.chat.title)
        return answer
