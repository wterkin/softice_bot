# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Модуль бармена."""

import random
import string
from pathlib import Path
import functions as func

BABBLER_BASE = "data/babbling"

# *** Команда перегрузки текстов
BABBLER_RELOAD: list = ["babble", "blr"]

# *** Ключ для списка доступных каналов в словаре конфига
CHANNEL_LIST_KEY: str = "babbler_chats"

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
TRIGGERS_FOLDER: str = "triggers"
REACTIONS_FOLDER: str = "reactions"

TRIGGERS_INDEX: int = 0
REACTIONS_INDEX: int = 1
BABBLER_MIND: list = []


def reload_babling_ext():
    """Загружает тексты болтуна."""
    # global BABBLER_MIND
    # *** Собираем пути
    triggers_path = Path(BABBLER_DATA) / TRIGGERS_FOLDER
    assert triggers_path.is_dir(), f"{TRIGGERS_FOLDER} must be folder"
    reactions_path = Path(BABBLER_DATA) / REACTIONS_FOLDER
    assert reactions_path.is_dir(), f"{REACTIONS_FOLDER} must be folder"
    # *** Создадим хранилище триггеров и реакций
    # triggers_list: list = []
    # BABBLER_MIND.append(triggers_list)
    # reactions_list: list = []
    # BABBLER_MIND.append(reactions_list)
    # *** Обойдём папку триггеров
    # data\babbling\triggers\001.txt
    for trigger in triggers_path.iterdir():

        if trigger.is_file():

            module = Path(trigger).resolve().name
            reaction = reactions_path / module
            if reaction.is_file():

                trigger_content: list = []
                trigger_content = func.load_from_file(trigger)
                block: list = [trigger_content]
                reaction_content: list = []
                reaction_content = func.load_from_file(reaction)
                block.append(reaction_content)
                BABBLER_MIND.append(block)
                print(trigger_content)
                print(reaction_content)


# def reload_babbling():
#     """Перезагружает приветствия."""
#
#     global GREETINGS_WORDS
#     GREETINGS_WORDS = func.load_from_file(GREETINGS_WORDS_FILE)
#     if GREETINGS_WORDS is not None:
#
#         print("Loaded ", len(GREETINGS_WORDS), " greeting words.")
#
#     global GREETINGS_ANSWERS
#     GREETINGS_ANSWERS = func.load_from_file(GREETINGS_ANSWERS_FILE)
#     if GREETINGS_ANSWERS is not None:
#
#         print("Loaded ", len(GREETINGS_ANSWERS), " greetings answers.")
#
#     global WEATHER_WORDS
#     WEATHER_WORDS = func.load_from_file(WEATHER_WORDS_FILE)
#     if WEATHER_WORDS is not None:
#
#         print("Loaded ", len(WEATHER_WORDS), " weather words.")
#
#     global WEATHER_ANSWERS
#     WEATHER_ANSWERS = func.load_from_file(WEATHER_ANSWERS_FILE)
#     if WEATHER_ANSWERS is not None:
#
#         print("Loaded ", len(WEATHER_ANSWERS), " weather answers.")
#
#     global BEAUTY_WORDS
#     BEAUTY_WORDS = func.load_from_file(BEAUTY_WORDS_FILE)
#     if BEAUTY_WORDS is not None:
#
#         print("Loaded ", len(BEAUTY_WORDS), " beauty words.")
#
#     global BEAUTY_ANSWERS
#     BEAUTY_ANSWERS = func.load_from_file(BEAUTY_ANSWERS_FILE)
#     if BEAUTY_ANSWERS is not None:
#
#         print("Loaded ", len(WEATHER_ANSWERS), " beauty answers.")


def is_enabled(pconfig: dict, pchat_title: str) -> bool:
    """Возвращает True, если бармен разрешен на этом канале.
    >>> is_enabled({'barman_chats':'Ботовка'}, 'Ботовка')
    True
    >>> is_enabled({'barman_chats':'Хокку'}, 'Ботовка')
    False
    """
    return pchat_title in pconfig[CHANNEL_LIST_KEY]


# def can_process(pconfig: dict, pchat_title: str, pmessage_text: str) -> bool:
def can_process(pconfig: dict, pchat_title: str) -> bool:
    """Возвращает True, если бармен может обработать эту команду
    >>> can_process({'barman_chats':'Ботовка'}, 'Ботовка', '!vodka')
    True
    >>> can_process({'barman_chats':'Хокку'}, 'Ботовка', '!vodka')
    False
    >>> can_process({'barman_chats':'Ботовка'}, 'Ботовка', '!мартини')
    False
    """

    if is_enabled(pconfig, pchat_title):

        # word_list: list = pmessage_text.split(" ")
        # if word_list[0] in " ".join(GREETINGS_WORDS) or
        #    word_list[0] in " ".join(WEATHER_WORDS)
        #     # (word_list[0] in ENGLISH_BAR_COMMANDS) or
        #     # (word_list[0] in SHORT_ENG_BAR_COMMANDS) or
        #     # (word_list[0] in MAIN_COMMANDS_LIST) or
        #     # (word_list[0] in BAR_RELOAD))
        #    :
        return True
    return False


def babbler(pmessage_text: str) -> str:
    """Улучшенная версия болтуна."""
    # global BABBLER_MIND
    message: str = ""
    found: bool = False
    word_list: list = pmessage_text.split(" ")
    for word in word_list:

        clean_word = word.rstrip(string.punctuation).lower()
        if len(clean_word) > 2 or ")" in clean_word:

            for block in BABBLER_MIND:

                if clean_word in " ".join(block[TRIGGERS_INDEX]):

                    print(block[REACTIONS_INDEX])
                    answer = random.choice(block[REACTIONS_INDEX])
                    message = f"{answer}"
                    found = True
                    break
        if found:

            break
    return message


# def babbler(pmessage_text: str) -> str:
#     """Процедура разбора запроса пользователя."""
#
#     # command: int = None
#     message: str = ""
#     word_list: list = pmessage_text.split(" ")
#     # *** Возможно, запросили меню.
#     # print("*** BBL:BBL:WL ", message)
#
#     for word in word_list:
#
#         clean_word = word.rstrip(string.punctuation)
#         if len(clean_word) > 2:
#
#             print("*** BBL:BBL:WR ", clean_word)
#             # print("*** BBL:BBL:GW ", GREETINGS_WORDS)
#             if clean_word in " ".join(GREETINGS_WORDS):
#
#                 message = f"{random.choice(GREETINGS_ANSWERS)}"
#                 print("*** BBL:BBL:GREET")
#                 break
#             if clean_word in " ".join(WEATHER_WORDS):
#
#                 message = f"{random.choice(WEATHER_ANSWERS)}"
#                 print("*** BBL:BBL:WEATHER")
#
#                 break
#             if clean_word in " ".join(BEAUTY_WORDS):
#
#                 message = f"{random.choice(BEAUTY_ANSWERS)}"
#                 print("*** BBL:BBL:BEAUTY")
#                 break
#
#     return message
