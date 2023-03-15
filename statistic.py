# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Модуль статистики для бота."""

import prototype
import database as db
import functions as func

TOP_10_COMMAND = [0, 4]
TOP_25_COMMAND = [1, 5]
TOP_50_COMMAND = [2, 6]
PERS_COMMAND = [3, 7]

HINT = ["стат", "stat"]
COMMANDS = ["топ10", "топ25", "топ50", "перс", "top10", "top25", "top50", "pers"]
ENABLED_IN_CHATS_KEY = "statistic_chats"
BOTS = ("TrueMafiaBot", "MafiaWarBot", "glagolitic_bot", "combot", "chgk_bot")
FOREIGN_BOTS = "foreign_bots"
SORTED_BY: tuple = ("предложений", "слов", "стикеров", "картинок",
                    "звуковых сообщений", "видео сообщений")


def decode_stat(pstat: db.CStat):
    """Декодирует запись статистики."""

    return pstat.fletters, pstat.fwords, pstat.fphrases, pstat.fstickers, \
        pstat.fpictures, pstat.faudios, pstat.fvideos


class CStatistic(prototype.CPrototype):
    """Класс статистика."""

    def __init__(self, pconfig: dict, pdatabase: db.CDataBase):
        super().__init__()
        self.config: dict = pconfig
        self.database: db.CDataBase = pdatabase
        self.busy: bool = False
        self.session = self.database.get_session()

    def add_chat_to_base(self, ptg_chat_id: int, ptg_chat_title: str):
        """Добавляет новый чат в БД и возвращает его ID."""
        chat = db.CChat(ptg_chat_id, ptg_chat_title)
        self.session.add(chat)
        self.session.commit()
        return chat.id

    def add_user_stat(self, puser_id: int, pchat_id: int, pstatfields: dict):
        """Добавляет новую запись статистики по человеку."""
        stat = db.CStat(puser_id, pchat_id, pstatfields)
        self.session.add(stat)
        self.session.commit()

    def add_user_to_base(self, ptg_user_id: int, ptg_user_title: str):
        """Добавляет нового пользователя в БД и возвращает его ID."""

        user = db.CUser(ptg_user_id, ptg_user_title)
        self.session.add(user)
        self.session.commit()
        return user.id

    def can_process(self, pchat_title: str, pmessage_text: str) -> bool:
        """Возвращает True, если модуль может обработать команду, иначе False."""
        if self.is_enabled(pchat_title):

            word_list: list = func.parse_input(pmessage_text)
            return word_list[0] in COMMANDS or word_list[0] in HINT
        return False

    def get_chat_id(self, ptg_chat_id):
        """Если чат уже есть в базе, возвращает его ID, если нет - None."""
        query = self.session.query(db.CChat)
        query = query.filter_by(fchatid=ptg_chat_id)
        data = query.first()
        if data is not None:

            return data.id
        return None

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
        answer: str = ""
        session = self.database.get_session()
        query = session.query(db.CUser)
        query = query.filter_by(fusername=puser_title)
        data = query.first()
        if data is not None:

            user_id: int = data.fuserid
            # *** Получим ID чата в базе
            query = session.query(db.CChat)
            query = query.filter_by(fchatid=ptg_chat_id)
            data = query.first()
            if data is not None:

                chat_id: int = data.id
                # print("*** STAT:GPI:СID ", user_id)
                query = session.query(db.CStat)
                query = query.filter_by(fuserid=user_id)
                query = query.filter_by(fchatid=chat_id)
                data = query.first()
                if data is not None:
                    answer = f"{puser_title} наболтал {data.fphrases} фраз, " \
                             f"{data.fwords} слов, {data.fletters} букв, запостил " \
                             f"{0 if data.fstickers is None else data.fstickers} стик., " \
                             f"{0 if data.fpictures is None else data.fpictures} фоток, " \
                             f"{0 if data.faudios is None else data.faudios} аудио и " \
                             f"{0 if data.fvideos is None else data.fvideos} видео,"

        return answer

    def get_statistic(self, ptg_chat_id: int, pcount: int, porder_by: int):
        """Получает из базы статистику по самым говорливым юзерам."""
        session = self.database.session
        query = session.query(db.CChat, db.CStat, db.CUser)  # , db.CName
        query = query.filter_by(fchatid=ptg_chat_id)
        query = query.join(db.CStat, db.CStat.fchatid == db.CChat.id)
        query = query.join(db.CUser, db.CUser.id == db.CStat.fuserid)
        # query = query.join(db.CName, db.CName.fuserid == db.CUser.id)
        if porder_by == 1:

            query = query.order_by(db.CStat.fphrases.desc())
        elif porder_by == 2:

            query = query.order_by(db.CStat.fwords.desc())
        elif porder_by == 3:

            query = query.order_by(db.CStat.fstickers.desc())
        elif porder_by == 4:

            query = query.order_by(db.CStat.fpictures.desc())
        elif porder_by == 5:

            query = query.order_by(db.CStat.faudios.desc())
        elif porder_by == 6:

            query = query.order_by(db.CStat.fvideos.desc())
        else:

            query = query.order_by(db.CStat.fphrases.desc())
            print("Предл")
        data = query.limit(pcount).all()
        print(data)
        answer = "Самые говорливые:\n"
        for number, item in enumerate(data):
            answer += f"{number + 1} : {item[2].fusername} : {item[1].fphrases}" \
                      f" предл., {item[1].fwords} слов, " \
                      f"{0 if item[1].fstickers is None else item[1].fstickers} стик., " \
                      f"{0 if item[1].fpictures is None else item[1].fpictures} фоток, " \
                      f"{0 if item[1].faudios is None else item[1].faudios} звук. и " \
                      f"{0 if item[1].fvideos is None else item[1].fvideos} вид. \n"
        # print('-'*50)
        # print(porder_by)
        # print(SORTED_BY)
        # print(SORTED_BY[porder_by-1])
        # print('-'*50)
        answer += f"Отсортировано по количеству {SORTED_BY[porder_by]}. \n"
        return answer

    def get_user_id(self, ptg_user_id):
        """Если пользователь уже есть в базе, возвращает его ID, если нет - None."""
        query = self.session.query(db.CUser)
        query = query.filter_by(ftguserid=ptg_user_id)
        data = query.first()
        if data is not None:
            return data.id
        return None

    def get_user_stat(self, pchat_id: int, puser_id: int):
        """Получает из базы статистику пользователя и возвращает её."""
        query = self.session.query(db.CStat)
        query = query.filter_by(fuserid=puser_id, fchatid=pchat_id)
        return query.first()

    def is_enabled(self, pchat_title: str) -> bool:
        """Возвращает True, если на этом канале этот модуль разрешен."""
        return pchat_title in self.config[ENABLED_IN_CHATS_KEY]

    def reload(self):
        """Вызывает перезагрузку внешних данных модуля."""

    def save_all_type_of_messages(self, pmessage):
        """Учитывает стикеры, видео, аудиосообщения."""
        message_text: str = pmessage.text
        tg_chat_id: int = pmessage.chat.id
        tg_chat_title: str = pmessage.chat.title
        tg_user_title: str = ""
        tg_user_id: int = pmessage.from_user.id
        tg_user_name: str = pmessage.from_user.username
        statfields: dict = {db.STATUSERID: 0,
                            db.STATLETTERS: 0,
                            db.STATWORDS: 0,
                            db.STATPHRASES: 0,
                            db.STATPICTURES: 0,
                            db.STATSTICKERS: 0,
                            db.STATAUDIOS: 0,
                            db.STATVIDEOS: 0}

        # *** Если есть у юзера первое имя - берем.
        if pmessage.from_user.first_name is not None:
            tg_user_title: str = pmessage.from_user.first_name
        # *** Если есть у юзера второе имя - тож берем.
        if pmessage.from_user.last_name is not None:
            tg_user_title += " " + pmessage.from_user.last_name
        # *** Это не бот написал? Чужой бот, не наш?
        if tg_user_name not in self.config[FOREIGN_BOTS]:

            # *** Если кто-то уже залочил базу, подождём
            while self.busy:

                pass
            # *** Лочим запись в базу и пишем сами
            self.busy = True
            # Проверить, нет ли уже этого чата в таблице чатов
            chat_id = self.get_chat_id(tg_chat_id)
            if chat_id is None:
                # Нету еще, новый чат - добавить, и получить id
                chat_id = self.add_chat_to_base(tg_chat_id, tg_chat_title)
            # *** Проверить, нет ли юзера в таблице тг юзеров
            user_id = self.get_user_id(tg_user_id)
            if user_id is None:
                # *** Нету, новый пользователь
                user_id = self.add_user_to_base(tg_user_id, tg_user_title)
            # *** Имеется ли в БД статистика по этому пользователю?
            user_stat = self.get_user_stat(chat_id, user_id)
            if user_stat is not None:

                statfields = user_stat.get_all_fields()  # !!! тут
            # *** Изменяем статистику юзера в зависимости от типа сообщения
            if pmessage.content_type in ["video", "video_note"]:

                statfields[db.STATVIDEOS] += 1
            elif pmessage.content_type in ["audio", "voice"]:

                statfields[db.STATAUDIOS] += 1
            elif pmessage.content_type == "photo":

                statfields[db.STATPICTURES] += 1
            elif pmessage.content_type == "sticker":

                statfields[db.STATSTICKERS] += 1
            elif pmessage.content_type == "text":

                if message_text[0] != "!":

                    statfields[db.STATLETTERS] += len(message_text)
                    statfields[db.STATWORDS] += len(message_text.split(" "))
                    statfields[db.STATPHRASES] += 1

            if user_stat is None:

                self.add_user_stat(user_id, chat_id, statfields)

            else:

                self.update_user_stat(user_id, chat_id, statfields)
            # *** Запись окончена, разлочиваем базу
            self.busy = False

    def statistic(self, pchat_id: int, pchat_title: str, puser_title, pmessage_text: str):
        """Обработчик команд."""
        command: int
        answer: str = ""
        order_by: int = 0
        word_list: list = func.parse_input(pmessage_text)
        if self.can_process(pchat_title, pmessage_text):

            if word_list[0] in HINT:

                answer = self.get_help(pchat_title)
            else:
                # *** Получим код команды
                command = func.get_command(word_list[0], COMMANDS)
                # print(word_list[0], command)
                if command >= 0:

                    if len(word_list) > 1 and word_list[1].isdigit():

                        order_by = int(word_list[1])
                        if order_by < 1 or order_by > 6:

                            order_by = 1
                    if command in TOP_10_COMMAND:

                        answer = self.get_statistic(pchat_id, 10, order_by)
                    elif command in TOP_25_COMMAND:

                        answer = self.get_statistic(pchat_id, 25, order_by)
                    elif command in TOP_50_COMMAND:

                        answer = self.get_statistic(pchat_id, 50, order_by)
                    elif command in PERS_COMMAND:

                        answer = self.get_personal_information(pchat_id, puser_title)
        return answer

    def update_user_stat(self, puser_id: int, pchat_id: int, pstatfields: dict):
        """Изменяет запись статистики по человеку."""
        query = self.session.query(db.CStat)
        query = query.filter_by(fuserid=puser_id)
        query = query.filter_by(fchatid=pchat_id)
        stat: db.CStat = query.first()
        stat.set_all_fields(pstatfields)
        self.session.add(stat)
        self.session.commit()
