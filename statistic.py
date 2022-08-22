# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Модуль статистики для бота."""

# from pathlib import Path
import m_names
import prototype
import functions
import database
import m_chats
import m_users
import m_stat

# from sys import platform
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker

# import m_ancestor
TOP_10_COMMAND = 0
TOP_25_COMMAND = 1
TOP_50_COMMAND = 2
PERS_COMMAND = 3

HINT = ["стат", "stat"]
COMMANDS = ["топ10", "топ25", "топ50", "перс", "top10", "top25", "top50", "pers"]
ENABLED_IN_CHATS_KEY = "statistic_chats"
BOTS = ("TrueMafiaBot", "MafiaWarBot", "glagolitic_bot", "combot", "chgk_bot")


class CStatistic(prototype.CPrototype):
    """Класс метеоролога."""

    def __init__(self, pconfig: dict, pdatabase: database.CDataBase):
        super().__init__()
        self.config: dict = pconfig
        self.database: database.CDataBase = pdatabase
        self.busy: bool = False
        self.session = self.database.get_session()

    def add_chat_to_base(self, ptg_chat_id: int, ptg_chat_title: str):
        """Добавляет чат в базу."""

        chat = m_chats.CChat(ptg_chat_id, ptg_chat_title)
        self.session.add(chat)
        self.session.commit()
        return chat.id

    def add_user_to_base(self, ptg_user_id: int, ptg_user_title: str):
        """Добавляет юзера в базу."""

        user = m_users.CUser(ptg_user_id)
        self.session.add(user)
        self.session.commit()
        # *** заодно сохраним имя пользователя
        user_name = m_names.CName(user.id, ptg_user_title)
        self.session.add(user_name)
        self.session.commit()
        return user.id

    def can_process(self, pchat_title: str, pmessage_text: str) -> bool:
        """Возвращает True, если модуль может обработать команду."""
        if self.is_enabled(pchat_title):

            word_list: list = functions.parse_input(pmessage_text)
            # print(word_list[0])
            return word_list[0] in COMMANDS or word_list[0] in HINT
        return False

    def get_command(self, pword: str) -> int:  # noqa
        """Распознает команду и возвращает её код, в случае неудачи - None.
        """
        assert pword is not None, \
            "Assert: [librarian.get_command] " \
            "No <pword> parameter specified!"
        result: int = -1
        for command_idx, command in enumerate(COMMANDS):

            if pword in command:
                result = command_idx

        if result > 3:
            result = result - 4

        return result

    def get_help(self, pchat_title: str) -> str:
        """Возвращает список команд модуля, доступных пользователю."""
        if self.is_enabled(pchat_title):

            command_list: str = ", ".join(COMMANDS)
            command_list += "\n"
            return command_list
        return ""

    def get_hint(self, pchat_title: str) -> str:
        """Возвращает команду верхнего уровня, в ответ на которую
           модуль возвращает полный список команд, доступных пользователю."""
        if self.is_enabled(pchat_title):
            return ", ".join(HINT)
        return ""

    def get_personal_information(self, ptg_chat_id: int, puser_title: str):
        """Возвращает информацию о пользователе"""
        message: str = ""
        session = self.database.get_session()
        query = session.query(m_names.CName)
        query = query.filter_by(fusername=puser_title)
        data = query.first()
        if data is not None:

            user_id: int = data.fuserid
            # print("*** STAT:GPI:UID ", user_id)
            # *** Получим ID чата в базе
            query = session.query(m_chats.CChat)
            query = query.filter_by(fchatid=ptg_chat_id)
            data = query.first()
            if data is not None:

                chat_id: int = data.id
                # print("*** STAT:GPI:СID ", user_id)
                query = session.query(m_stat.CStat)
                query = query.filter_by(fuserid=user_id)
                query = query.filter_by(fchatid=chat_id)
                data = query.first()
                if data is not None:

                    # print("*** STAT:GPI:STAT ", data.fphrases)
                    message = f"{puser_title} наболтал {data.fphrases} фраз, " \
                              f"{data.fwords} слов, {data.fletters} букв."
        return message

    def get_statistic(self, ptg_chat_id: int, pcount: int):
        """Получает из базы статистику по самым говорливым юзерам."""
        session = self.database.session
        query = session.query(m_chats.CChat, m_stat.CStat, m_names.CName)
        query = query.filter_by(fchatid=ptg_chat_id)
        query = query.join(m_stat.CStat, m_stat.CStat.fchatid == m_chats.CChat.id)
        query = query.join(m_users.CUser, m_users.CUser.id == m_stat.CStat.fuserid)
        query = query.join(m_names.CName, m_names.CName.fuserid == m_users.CUser.id)
        query = query.order_by(m_stat.CStat.fphrases.desc())
        data = query.limit(pcount).all()
        answer = "Самые говорливые:\n"
        for number, item in enumerate(data):

            answer += f"{number+1} : {item[2].fusername} : {item[1].fphrases}" \
                      f" предложений, {item[1].fwords} слов.\n"
        return answer

    def get_chat_id(self, ptg_chat_id):
        """Если чат уже есть в базе, возвращает его ID, если нет - None."""
        query = self.session.query(m_chats.CChat)
        query = query.filter_by(fchatid=ptg_chat_id)
        data = query.first()
        if data is not None:

            return data.id
        return None

    def get_user_id(self, ptg_user_id):
        """Если юзер уже есть в базе, возвращает его ID, если нет - None."""

        query = self.session.query(m_users.CUser)
        query = query.filter_by(ftguserid=ptg_user_id)
        data = query.first()
        if data is not None:

            return data.id
        return None

    def is_enabled(self, pchat_title: str) -> bool:
        """Возвращает True, если на этом канале этот модуль разрешен."""
        return pchat_title in self.config[ENABLED_IN_CHATS_KEY]

    def reload(self):
        """Вызывает перезагрузку внешних данных модуля."""

    def read_user_stat(self, pchat_id: int, puser_id: int):
        """Читает из базы информацию о пользователе и возвращает ее."""
        query = self.session.query(m_stat.CStat)
        query = query.filter_by(fuserid=puser_id, fchatid=pchat_id)
        return query.first()

    def save_message(self, pmessage):
        """Сохраняет фразу, произнесенную пользователем, в базе."""
        session = self.database.get_session()
        message_text: str = pmessage.text
        tg_chat_id: int = pmessage.chat.id
        tg_chat_title: str = pmessage.chat.title
        tg_user_title: str = ""
        tg_user_id: int = pmessage.from_user.id
        tg_user_name: str = pmessage.from_user.username
        if pmessage.from_user.first_name is not None:

            tg_user_title: str = pmessage.from_user.first_name
        if pmessage.from_user.last_name is not None:

            tg_user_title += " " + pmessage.from_user.last_name
        # tg_user_title: str = first_name + last_name
        # print("> ", tg_user_title)
        if message_text[0] != "!":

            if tg_user_name != "TrueMafiaBot" and \
                    tg_user_name != "MafiaWarBot":

                # *** Если кто-то уже залочил базу, подождём
                while self.busy:
                    pass

                # *** Лочим запись в базу и пишем сами
                self.busy = True
                # проверить, нет ли чата в таблице чатов
                # chat_id: int = -1
                query = session.query(m_chats.CChat)
                query = query.filter_by(fchatid=tg_chat_id)
                data = query.first()
                if data is None:

                    # если нет - добавить, и получить id
                    chat = m_chats.CChat(tg_chat_id, tg_chat_title)
                    session.add(chat)
                    session.commit()
                    chat_id = chat.id
                else:

                    chat_id = data.id
                # print("STT:SM:CHAT ID: ", chat_id)
                # *** проверить, нет ли юзера в таблице тг юзеров, если нет - добавить и получить id
                query = session.query(m_users.CUser)
                query = query.filter_by(ftguserid=tg_user_id)
                data = query.first()
                if data is None:

                    # *** если нет - добавить, и получить id
                    user = m_users.CUser(tg_user_id)
                    session.add(user)
                    session.commit()
                    user_id = user.id
                    # *** заодно сохраним имя пользователя
                    user_name = m_names.CName(user_id, tg_user_title)
                    session.add(user_name)
                    session.commit()
                    # print(f"STT:SM:USR NAME: {user_name.id}")
                else:

                    user_id = data.id
                # print("STT:SM:USER NAME: ", tg_user_name)
                # print("STT:SM:USER ID: ", user_id)
                # *** Проанализируем фразу
                letters = len(message_text)
                words = len(message_text.split(" "))
                # *** Есть ли запись об этом человеке в таблице статистики?
                # если есть - получить id
                query = session.query(m_stat.CStat)
                query = query.filter_by(fuserid=user_id, fchatid=chat_id)
                data = query.first()
                if data is None:

                    pass
                    # *** Добавляем информацию в базу
                    # stat_object = m_stat.CStat(user_id, chat_id, letters, words, 1)
                    # session.add(stat_object)

                else:

                    # *** Изменяем информацию в базе
                    query.update({m_stat.CStat.fletters: data.fletters + letters,
                                  m_stat.CStat.fwords: data.fwords + words,
                                  m_stat.CStat.fphrases: data.fphrases + 1}, synchronize_session=False)
                session.commit()
                # *** Запись окончена, разлочиваем базу
                self.busy = False

            # if tg_chat_id.count() == 0:
            #
            #     #
            #     chat = m_chats.CChat(chat_id)
            #     self.database.get_session().add(chat)
            #     self.database.get_session().commit()
            #     print(f"{chat_title}:{chat_id}:{chat}")
            #     # else:
            #     #     # если есть - получить id
            #     # query =
            #     # print(tg_chat_id.all())
            #
            # # tg_id_data = self.database.get_session().query(m_users.CUser).filter_by(ftguserid=user_id)
            # # if tg_id_data.count() == 0:
            # select seq
            # from sqlite_sequence where
            # name = "table_name"
            # me = User(nickname, email, passw)
            #     db.session.add(me)
            #     db.session.commit()
            #     print(me.id)

    def save_non_text_message(self, pmessage):
        """Учитывает стикеры, видео, аудиосообщения."""
        session = self.database.get_session()
        message_text: str = pmessage.text
        tg_chat_id: int = pmessage.chat.id
        tg_chat_title: str = pmessage.chat.title
        tg_user_title: str = ""
        tg_user_id: int = pmessage.from_user.id
        tg_user_name: str = pmessage.from_user.username
        # *** Если есть у юзера первое имя - берем.
        if pmessage.from_user.first_name is not None:

            tg_user_title: str = pmessage.from_user.first_name
        # *** Если есть у юзера второе имя - тож берем.
        if pmessage.from_user.last_name is not None:

            tg_user_title += " " + pmessage.from_user.last_name
        # *** Сообщение не от бота?
        if tg_user_name not in BOTS:

            # *** Если кто-то уже залочил базу, подождём
            while self.busy:

                pass

            # *** Лочим запись в базу и пишем сами
            self.busy = True

            # Проверить, нет ли уже этого чата в таблице чатов
            chat_id = self.get_chat_id(tg_chat_id)
            # query = session.query(m_chats.CChat)
            # query = query.filter_by(fchatid=tg_chat_id)
            # data = query.first()
            if chat_id is None:

                # Нету еще, новый чат - добавить, и получить id
                chat_id = self.add_chat_to_base(tg_chat_id, tg_chat_title)
                # chat = m_chats.CChat(tg_chat_id, tg_chat_title)
                # session.add(chat)
                # session.commit()
                # chat_id = chat.id
            # *** Проверить, нет ли юзера в таблице тг юзеров
            user_id = self.get_user_id(tg_user_id)
            # query = session.query(m_users.CUser)
            # query = query.filter_by(ftguserid=tg_user_id)
            # data = query.first()
            if user_id is None:

                # *** если нет - добавить, и получить id
                # user = m_users.CUser(tg_user_id)
                # session.add(user)
                # session.commit()
                # user_id = user.id
                # # *** заодно сохраним имя пользователя
                # user_name = m_names.CName(user_id, tg_user_title)
                # session.add(user_name)
                # session.commit()
                user_id = self.add_user_to_base(tg_user_id, tg_user_title)
            # else:
            #
            #     user_id = data.id
            user_stat = self.read_user_stat(chat_id, user_id)
            print(user_stat)
            if user_stat is not None:

                # *** Изменяем статистику юзера в зависимости от типа сообщения
                if pmessage.content_type in ["video", "video_note"]:

                    if user_stat.fvideos is None:

                        user_stat.fvideos = 0
                    else:

                        user_stat.fvideos += 1
                elif pmessage.content_type in ["audio", "voice"]:

                    if user_stat.faudios is None:

                        user_stat.faudios = 0
                    else:

                        user_stat.faudios += 1
                elif pmessage.content_type == "photo":

                    if user_stat.fphotos is None:

                        user_stat.fphotos = 0
                    else:

                        user_stat.fphotos += 1
                elif pmessage.content_type == "sticker":

                    if user_stat.fstickers is None:

                        user_stat.fstickers = 0
                    else:

                        user_stat.fstickers += 1
            else:

                self.add_user_stat(tg_user_id, tg_user_title)
            # *** Есть ли запись об этом человеке в таблице статистики?
            # если есть - получить id
            # query = session.query(m_stat.CStat)
            # query = query.filter_by(fuserid=user_id, fchatid=chat_id)
            # data = query.first()
            # if data is None:
            #
                # *** Добавляем информацию в базу
                # stat_object = m_stat.CStat(user_id, chat_id, 0, 0, sticker_count, photo_count,
                #                            audio_count, video_count)
                # session.add(stat_object)

            # else:
            #
            #     if data.fstickers is None:
            #
            #         data.fstickers = 0
            #     if data.fpictures is None:
            #
            #         data.fpictures = 0
            #     if data.faudios is None:
            #
            #         data.faudios = 0
            #     if data.fvideos is None:
            #
            #         data.fvideos = 0
            #
                # *** Изменяем информацию в базе
            # query.update({m_stat.CStat.fletters: data.fletters,
            #               m_stat.CStat.fwords: data.fwords,
            #               m_stat.CStat.fphrases: data.fphrases}, synchronize_session=False)
            session.commit()
            # *** Запись окончена, разлочиваем базу
            self.busy = False

    def statistic(self, pchat_id: int, pchat_title: str, puser_title, pmessage_text: str):
        """Обработчик команд."""
        command: int
        answer: str = ""
        word_list: list = functions.parse_input(pmessage_text)
        if self.can_process(pchat_title, pmessage_text):

            if word_list[0] in HINT:

                answer = self.get_help(pchat_title)
            else:
                # *** Получим код команды
                command = self.get_command(word_list[0])
                # print(word_list[0], command)
                if command >= 0:

                    if command == TOP_10_COMMAND:

                        answer = self.get_statistic(pchat_id, 10)
                    elif command == TOP_25_COMMAND:

                        answer = self.get_statistic(pchat_id, 25)
                    elif command == TOP_50_COMMAND:

                        answer = self.get_statistic(pchat_id, 50)
                    elif command == PERS_COMMAND:

                        answer = self.get_personal_information(pchat_id, puser_title)
        return answer
