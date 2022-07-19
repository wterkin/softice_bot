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


class CStatistic(prototype.CPrototype):
    """Класс метеоролога."""

    def __init__(self, pconfig: dict, pdatabase: database.CDataBase):
        super().__init__()
        self.config: dict = pconfig
        self.database: database.CDataBase = pdatabase
        self.busy: bool = False

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
        # query = session.query(m_chats.CChat)
        # *** Что мы хотим получить?
        # *** Мы хотим выбрать pcount людей, которые больше всего болтали.
        #     и количество фраз, сказанных ими, разумеется.
        #     Что мы имеем?
        #     Идентификатор чата, телеграмский.
        #     Наши действия?
        #     Делаем выборку из таблицы chats по tg id
        """
        query = session.query(m_chats.CChat.id,
                              m_stat.CStat.fphrases,
                              m_users.CUser.id,
                              m_names.CName.fusername)
        query = query.filter_by(fchatid=ptg_chat_id)
        data = query.limit(pcount).all()
        query = query.join(UserRole, UserRole.user_id == User.id)
        query = query.join(Role, Role.id == UserRole.role_id)
        query = query.join(Order, Order.user_id == User.id)
        query = query.join(Product, Product.id == Order.product_id)
            """
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

    def is_enabled(self, pchat_title: str) -> bool:
        """Возвращает True, если на этом канале этот модуль разрешен."""
        return pchat_title in self.config[ENABLED_IN_CHATS_KEY]

    def reload(self):
        """Вызывает перезагрузку внешних данных модуля."""

    def save_message(self, pmessage):
        """Сохраняет фразу, произнесенную пользователем, в базе."""
        # print(pmessage)
        session = self.database.get_session()
        message_text: str = pmessage.text
        tg_chat_id: int = pmessage.chat.id
        tg_chat_title: str = pmessage.chat.title
        tg_user_id: int = pmessage.from_user.id
        tg_user_name: str = pmessage.from_user.username
        tg_user_title: str = pmessage.from_user.first_name
        if message_text[0] != "!":

            if tg_user_name is not None and \
                    tg_user_name != "TrueMafiaBot" and \
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

                    # *** Добавляем информацию в базу
                    stat_object = m_stat.CStat(user_id, chat_id, letters, words, 1)
                    session.add(stat_object)

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
