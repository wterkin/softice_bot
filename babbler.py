# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Модуль бармена."""

import random
import string
from datetime import datetime
# from pdb import pm
from time import sleep
from pathlib import Path
import functions as func
import constants as cn
import prototype
import debug as dbg

# *** Команда перегрузки текстов
BABBLER_RELOAD: list = ["blreload", "blrl"]
# *** Ключ для списка доступных каналов в словаре конфига
UNIT_ID = "babbler"
BABBLER_PATH: str = "babbler/"
BABBLER_PERIOD_KEY = "babbler_period"
TRIGGERS_FOLDER: str = "triggers"
TRIGGERS_INDEX: int = 0
REACTIONS_FOLDER: str = "reactions"
REACTIONS_INDEX: int = 1
BABBLER_EMODJI: list = ["😎", "😊", "☺", "😊", "😋"]
NICKNAMES: list = ["softice", "софтик", "софтайсик", "ботик", "бот"]


class CBabbler(prototype.CPrototype):
    """Класс болтуна."""

    def __init__(self, pconfig: dict, pdata_path: str):
        """"Конструктор."""
        super().__init__()
        self.config: dict = pconfig
        self.data_path: str = pdata_path + BABBLER_PATH
        self.mind: list = []
        self.last_phrase_time: datetime = datetime.now()
        self.reload()

    def babbler(self, pmsg_rec: dict) -> str:
        """Улучшенная версия болтуна."""
        answer: str = ""
        word_list: list = func.parse_input(pmsg_rec[cn.MTEXT])
        if self.can_process(pmsg_rec[cn.MCHAT_TITLE], pmsg_rec[cn.MTEXT]):

            # *** Возможно, запросили перезагрузку базы.
            if word_list[0] in BABBLER_RELOAD:

                if self.is_master(pmsg_rec[cn.MUSER_NAME]):

                    self.reload()
                    answer = "База болтуна обновлена"
                else:

                    print(f"> Babbler: Запрос на перезагрузку конфига от "
                          f"нелегитимного лица {pmsg_rec[cn.MUSER_TITLE]}.")
                    answer = f"У вас нет на это прав, {pmsg_rec[cn.MUSER_TITLE]}."
        return answer

    def can_process(self, pchat_title: str, pmessage_text: str) -> bool:
        """Болтун всегда может обработать эту команду."""
        assert pchat_title is not None, \
            "Assert: [babbler.can_process] Пропущен параметр <pchat_title> !"
        assert pmessage_text is not None, \
            "Assert: [babbler.can_process] Пропущен параметр <pmessage_text> !"
        return self.is_enabled(pchat_title)

    def get_help(self, pchat_title: str):
        """Возвращает список команд модуля, доступных пользователю."""
        return ""

    def get_hint(self, pchat_title: str):
        """Возвращает команду верхнего уровня, в ответ на которую
           модуль возвращает полный список команд, доступных пользователю."""
        return ""

    def is_enabled(self, pchat_title: str) -> bool:
        """Возвращает True, если бармен разрешен на этом канале."""
        assert pchat_title is not None, \
            "Assert: [babbler.is_enabled] Пропущен параметр <pchat_title> !"
        return UNIT_ID in self.config["chats"][pchat_title]

    def is_master(self, puser_name: str) -> bool:
        """Проверяет, хозяин ли отдал команду."""
        return puser_name == self.config["master"]

    def reload(self):
        """Загружает тексты болтуна."""
        # *** Собираем пути
        triggers_path = Path(self.data_path) / TRIGGERS_FOLDER
        assert triggers_path.is_dir(), f"{TRIGGERS_FOLDER} must be folder"
        reactions_path = Path(self.data_path) / REACTIONS_FOLDER
        assert reactions_path.is_dir(), f"{REACTIONS_FOLDER} must be folder"
        result: bool = False
        self.mind.clear()
        for trigger in triggers_path.iterdir():

            if trigger.is_file():

                module = Path(trigger).resolve().name
                reaction = reactions_path / module
                if reaction.is_file():
                    trigger_content: list = func.load_from_file(str(trigger))
                    block: list = [trigger_content]
                    reaction_content: list = func.load_from_file(str(reaction))
                    block.append(reaction_content)
                    self.mind.append(block)
                    result = True
        if self.mind:
            print(f"> Babbler успешно (пере)загрузил {len(self.mind)} реакций.")
        return result

    def talk(self, pmsg_rec: dict) -> str:
        """Улучшенная версия болтуна."""

        answer: str = ""
        # *** Заданный период времени с последней фразы прошел?
        # print(f"&&&&& 2 {pmsg_rec[cn.MCHAT_TITLE]}")
        # s = self.config["chats"][pmsg_rec[cn.MCHAT_TITLE]]
        # print(f"&&&&& 3 {s}")
        if self.is_enabled(pmsg_rec[cn.MCHAT_TITLE]):

            minutes: float = (datetime.now() - self.last_phrase_time).total_seconds() / \
                             int(self.config[BABBLER_PERIOD_KEY])
            if minutes > 1:
                answer = self.think(pmsg_rec)
            if answer:
                print(f"> Babbler отвечает: {answer[:func.OUT_MSG_LOG_LEN]}...")
                self.last_phrase_time = datetime.now()
        return answer

    def think(self, pmsg_rec: dict):
        """Процесс принятия решений =)"""
        word_list: list = pmsg_rec[cn.MTEXT].split(" ")
        answer: str = ""
        personal: bool = False
        nicks: str = " ".join(NICKNAMES)
        # *** Переберем все слова в сообщении
        # ToDO: Вот тут сделать перебор ников и потом nick in word_list
        for word in word_list:

            # *** Определяем, есть ли в сообщении упоминание бота.
            personal = word.rstrip(string.punctuation).lower().strip() in nicks
            # *** Как только нашли - выходим из цикла.
            if personal:

                break
        # *** Снова перебираем сообщение по словам (как-то неоптимально выходит)
        for word in word_list:

            # *** Убираем из слова знаки пунктуации и пробелы, переводим в нижний регистр
            clean_word = word.rstrip(string.punctuation).lower().strip()
            # *** Если что-то осталось, двигаемся дальше.
            if len(clean_word) > 1:

                # *** Перебираем блоки памяти бота
                for block in self.mind:

                    triggers: list = block[0]
                    # *** Если в списке триггеров есть такое слово

                    if clean_word in triggers or "@" + clean_word in triggers:

                        if "@" in "".join(block[0]):

                            # *** если в строке есть обращение к боту
                            if personal:

                                # dbg.dout(f"%%%%%% 2")
                                answer = f"{random.choice(block[REACTIONS_INDEX])}"
                                sleep(1)
                                break
                        else:

                            # dbg.dout(f"%%%%%% 3")
                            answer = f"{random.choice(block[REACTIONS_INDEX])}"
                            sleep(1)
                            break

                    if answer:
                        break
            if answer:
                break
        return answer
