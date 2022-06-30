# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Модуль бармена."""

import random
import string
from datetime import datetime
from pathlib import Path
import functions as func
import prototype

BABBLER_BASE = "data/babbling"

# *** Команда перегрузки текстов
BABBLER_RELOAD: list = ["babreload", "bblr"]

# *** Ключ для списка доступных каналов в словаре конфига
ENABLED_IN_CHATS_KEY: str = "babbler_chats"

GREETINGS_WORDS: list = []
GREETINGS_WORDS_FILE: str = "data/babbling/greetings_words.txt"
GREETINGS_ANSWERS: list = []
GREETINGS_ANSWERS_FILE: str = "data/babbling/greetings_answers.txt"

WEATHER_WORDS: list = []
WEATHER_WORDS_FILE: str = "data/babbling/weather_words.txt"
WEATHER_ANSWERS: list = []
WEATHER_ANSWERS_FILE: str = "data/babbling/weather_answers.txt"

BEAUTY_WORDS: list = []
BEAUTY_WORDS_FILE: str = "data/babbling/beauty_words.txt"
BEAUTY_ANSWERS: list = []
BEAUTY_ANSWERS_FILE: str = "data/babbling/beauty_answers.txt"

BABBLER_DATA: str = "data/babbling/"
BABBLER_PERIOD: int = 10  # !
TRIGGERS_FOLDER: str = "triggers"
REACTIONS_FOLDER: str = "reactions"

TRIGGERS_INDEX: int = 0
REACTIONS_INDEX: int = 1
BABBLER_MIND: list = []


class CBabbler(prototype.CPrototype):
    """Класс болтуна."""

    def __init__(self, pconfig):
        """"Конструктор."""
        super().__init__()
        self.config = pconfig
        self.mind: list = []
        self.last_phrase_time: datetime = datetime.now()
        self.reload()

    def babbler(self, pchat_title: str, pmessage_text: str) -> str:
        """Улучшенная версия болтуна."""
        message: str = ""
        found: bool = False

        minutes = (datetime.now() - self.last_phrase_time).total_seconds() / BABBLER_PERIOD
        # *** Заданный период времени с последней фразы прошел?
        if minutes > 1:

            # *** Болтун может? болтун может всегда!
            if self.can_process(pchat_title, pmessage_text):

                word_list: list = pmessage_text.split(" ")
                for word in word_list:

                    clean_word = word.rstrip(string.punctuation).lower()
                    if len(clean_word) > 2:  # or ")" in clean_word:

                        for block in self.mind:

                            for block_item in block:

                                if clean_word in block_item:

                                    answer = random.choice(block[REACTIONS_INDEX])
                                    message = f"{answer}"
                                    found = True
                                    break
                            if found:

                                break
                    if found:

                        break

        if len(message) > 0:

            print("Babbler answers.", message)
            self.last_phrase_time = datetime.now()
        return message

    def can_process(self, pchat_title: str, pmessage_text: str) -> bool:
        """Болтун всегда может обработать эту команду."""

        return self.is_enabled(pchat_title)

    def get_help(self):
        """Возвращает список команд модуля, доступных пользователю."""
        return ""

    def get_hint(self):
        """Возвращает команду верхнего уровня, в ответ на которую
           модуль возвращает полный список команд, доступных пользователю."""
        return ""

    def is_enabled(self, pchat_title: str) -> bool:
        """Возвращает True, если бармен разрешен на этом канале.
        >>> self.is_enabled({'barman_chats':'Ботовка'}, 'Ботовка')
        True
        >>> self.is_enabled({'barman_chats':'Хокку'}, 'Ботовка')
        False
        """
        return pchat_title in self.config[ENABLED_IN_CHATS_KEY]

    def reload(self):
        """Загружает тексты болтуна."""
        # *** Собираем пути
        triggers_path = Path(BABBLER_DATA) / TRIGGERS_FOLDER
        assert triggers_path.is_dir(), f"{TRIGGERS_FOLDER} must be folder"
        reactions_path = Path(BABBLER_DATA) / REACTIONS_FOLDER
        assert reactions_path.is_dir(), f"{REACTIONS_FOLDER} must be folder"
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
        if self.mind:

            print("Babbler successfully reload his mind.")
