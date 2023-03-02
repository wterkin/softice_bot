# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Погодный модуль для бота."""
# from time import time
import re
import functions as func
import prototype
from pathlib import Path
import random
# import m_ancestor
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, MetaData, String
from sqlalchemy.ext.declarative import declarative_base

# convention: Optional[Dict[str, str]] = {
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

RELOAD_BAD_WORDS: list = ["bwreload", "bwrl"]
ENABLED_IN_CHATS_KEY: str = "moderator_chats"
DATA_FOLDER: str = "moderator"
BAD_WORDS_FILE: str = "bad_words.txt"
ADMINISTRATION_CMD: list = ["admin", "adm"]
BADWORDS_MUTE_TIME = 300
NEW_USER_RATING: int = 15
MINIMAL_TEXT_RATING: int = 10
MINIMAL_STICKER_RATING: int = 20
MINIMAL_PHOTO_RATING: int = 30
MINIMAL_AUDIO_RATING: int = 40
MINIMAL_VIDEO_RATING: int = 50

DATABASE_NAME: str = "users.db"
STATUS_ACTIVE: int = 1
STATUS_INACTIVE: int = 0
BAD_WORDS_MESSAGES: list = [f"А ну, не матерись тут!!",
                            "\[\*\* censored \*\*\]",
                            "\[\*\* Бип. Бип. Бииииип\! \*\*\]",
                            "\[\*\* beep \*\*\]",
                            "\[\*\* Мат вырезан. \*\*\]"
                            ]

# анти-спам прикрутить!

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
    fchatid = Column(Integer, default=0)
    frating = Column(Integer, default=NEW_USER_RATING)
    fusername = Column(String)

    def __init__(self, puserid: int, pusername: str, pchatid: int):
        """Конструктор"""
        super().__init__()
        self.fuserid = puserid
        self.fchatid = pchatid
        self.fusername = pusername


    def __repr__(self):
        ancestor_repr = super().__repr__()
        return f"""{ancestor_repr},
                   user ID :{self.fuserid}
                   chat ID :{self.fchatid}
                   user rating :{self.frating}"""

    def null(self):
        """Чтоб линтер был щаслиф."""


class CModerator(prototype.CPrototype):
    """Класс модератора."""

    def __init__(self, pbot, pconfig, pdata_path: str):

        super().__init__()
        self.config = pconfig
        self.data_path: str = pdata_path + DATA_FOLDER + "/"
        self.bot = pbot
        # self.database = pdatabase
        self.bad_words: list = []
        self.reload()
        # *** Коннектимся к базе
        database_file_name = Path(self.data_path) / DATABASE_NAME
        Session = sessionmaker()
        self.engine = create_engine('sqlite:///' + str(database_file_name),
                                    echo=False,
                                    connect_args={'check_same_thread': False})
        Session.configure(bind=self.engine)
        self.session = Session()
        Base.metadata.bind = self.engine
        # *** Если базы нет - создаем
        if not database_file_name.exists():

            print("* Создаем базу")
            Base.metadata.create_all()

    def add_user(self, puser_id: int, puser_name: str, pchat_id: int):
        """Добавляет в базу нового пользователя"""
        user = CUser(puser_id, puser_name, pchat_id)
        self.session.add(user)
        self.session.commit()
        return user.id

    def can_process(self, pchat_title: str, pmessage_text: str) -> bool:
        """Возвращает True, если модуль может обработать команду."""
        word_list: list = func.parse_input(pmessage_text)
        return self.is_enabled(pchat_title) and word_list[0] in RELOAD_BAD_WORDS
        # (word_list[0] in MUTE_COMMANDS or word_list[0] in ADMINISTRATION_CMD)

    def check_bad_words(self, pmessage) -> bool:
        """Проверяет сообщение на наличие мата."""
        result: bool = False
        for word in self.bad_words:

            result = re.match(word, pmessage.lower()) is not None
            if result:
                # print(pmessage.lower())
                break

        return result

    def control_talking(self, pmessage):
        """Следит за матершинниками."""
        answer: str = ""
        text: str
        if pmessage.content_type == "text":

            text = pmessage.text
        else:

            text = pmessage.caption
        # pmessage.from_user.first_name, pmessage.from_user.first_name,
        if self.is_enabled(pmessage.chat.title):

            if self.check_bad_words(text):

                self.bot.delete_message(chat_id=pmessage.chat.id, message_id=pmessage.message_id)
                answer = random.choice(BAD_WORDS_MESSAGES)
                print(f"!!! Юзер {pmessage.from_user.first_name} в чате '{pmessage.chat.title}' матерился, редиска "
                      f"такая!")
                print(f"!!! Он сказал '{text}'")

        return answer

    def delete_message(self, pmessage):
        """Удаляет сообщение пользователя."""
        # self.bot.delete_message(chat_id=pmessage.chat.id, message_id=pmessage.message_id)
        # print(f"> Сообщение пользователя {pmessage.from_user.username} в чате '{pmessage.chat.title}' удалено.")

    def find_user_id(self, puser_title: str):
        """Ищет в базе ID пользователя по его нику."""
        # session = self.database.get_session()
        # query = session.query(m_names.CName, m_users.CUser)
        # query = query.filter_by(fusername=puser_title)
        # query = query.join(m_users.CUser, m_users.CUser.id == m_names.CName.fuserid)
        # data = query.first()
        # if data is not None:
        #     return data[1].ftguserid
        # return None

    def get_help(self, pchat_title: str) -> str:
        """Возвращает список команд модуля, доступных пользователю."""
        return ""

    def get_user(self, puser_id):
        """Если пользователь уже есть в базе, возвращает его ID, если нет - None."""
        query = self.session.query(CUser)
        query = query.filter_by(fuserid=puser_id)
        data = query.first()
        if data is not None:
            return data
        return None

    def get_hint(self, pchat_title: str) -> str:
        """Возвращает команду верхнего уровня, в ответ на которую
           модуль возвращает полный список команд, доступных пользователю."""
        return ""

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

    def moderator(self, pmessage) -> str:
        """Процедура разбора запроса пользователя."""
        command: int
        # *** Проверим, всё ли в порядке в чате
        answer: str = self.supervisor(pmessage)
        if not answer:

            # *** Порядок. Возможно, запрошена команда. Мы ее умеем?
            if self.can_process(pmessage.chat.title, pmessage.text):

                # *** Да. Возможно, запросили перезагрузку.
                word_list: list = func.parse_input(pmessage.text)
                if word_list[0] in RELOAD_BAD_WORDS:

                    # *** Пользователь хочет перезагрузить словарь мата.
                    can_reload, answer = self.is_master(pmessage.from_user.username, pmessage.from_user.first_name)
                    if can_reload:

                        self.reload()
                        answer = "Словарь мата обновлен"
                    else:

                        # *** ... но не тут-то было...
                        print(f"> Librarian: Запрос на перегрузку цитат от "
                              f"нелегитимного лица {pmessage.from_user.first_name}.")
                        answer = (f"Извини, {pmessage.from_user.first_name}, "
                                  f"только {self.config['master_name']} может перегружать цитаты!")
        return answer

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

    #
    # or entity in message.entities:  # Пройдёмся по всем entities в поисках ссылок
    # # url - обычная ссылка, text_link - ссылка, скрытая под текстом
    # if entity.type in ["url", "text_link"]:
    #     # Мы можем не проверять chat.id, он проверяется ещё в хэндлере
    #     bot.delete_message(message.chat.id, message.message_id)
    # else:
    #     return

    def supervisor(self, pmessage):
        """Контролирует поведение людей в чате."""
        user: CUser = self.get_user(pmessage.from_user.id)
        answer: str = ""
        if user is not None:

            if pmessage.content_type == "text":

                if user.frating < MINIMAL_TEXT_RATING:

                    self.delete_message(pmessage)
            elif pmessage.content_type == "sticker":

                if user.frating < MINIMAL_STICKER_RATING:

                    self.delete_message(pmessage)
            elif pmessage.content_type == "photo":

                if user.frating < MINIMAL_PHOTO_RATING:

                    self.delete_message(pmessage)
            elif pmessage.content_type in ["voice", "audio"]:

                if user.frating < MINIMAL_AUDIO_RATING:

                    self.delete_message(pmessage)
            elif pmessage.content_type in ["video", "video_note"]:

                if user.frating < MINIMAL_VIDEO_RATING:

                    self.delete_message(pmessage)
        else:

            name: str = pmessage.from_user.first_name + " " + pmessage.from_user.last_name
            self.add_user(pmessage.from_user.id, name, pmessage.chat.id)
        if not answer:

            # *** Проверим, не матерился ли кто.
            answer = self.control_talking(pmessage)
        return answer

    def reload(self):
        """Загружает тексты болтуна."""
        # *** Собираем пути
        assert Path(self.data_path).is_dir(), f"{DATA_FOLDER} must be folder"
        data_path = Path(self.data_path) / BAD_WORDS_FILE
        self.bad_words.clear()
        self.bad_words = func.load_from_file(str(data_path))
        print(f"> Moderator успешно (пере)загрузил {len(self.bad_words)} регэкспов матерных выражений.")

    def administration(self):
        """Выводит список пользователей для модерирования."""
