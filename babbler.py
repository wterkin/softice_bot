# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Модуль бармена."""

import random
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


def reload_babbling():
    """Перезагружает приветствия."""

    global GREETINGS_WORDS
    GREETINGS_WORDS = func.load_from_file(GREETINGS_WORDS_FILE)
    if GREETINGS_WORDS is not None:

        print("Loaded ", len(GREETINGS_WORDS), " greeting words.")

    global GREETINGS_ANSWERS
    GREETINGS_ANSWERS = func.load_from_file(GREETINGS_ANSWERS_FILE)
    if GREETINGS_ANSWERS is not None:

        print("Loaded ", len(GREETINGS_ANSWERS), " greetings answers.")

    global WEATHER_WORDS
    WEATHER_WORDS = func.load_from_file(WEATHER_WORDS_FILE)
    if GREETINGS_WORDS is not None:

        print("Loaded ", len(WEATHER_WORDS), " weather words.")

    global WEATHER_ANSWERS
    WEATHER_ANSWERS = func.load_from_file(WEATHER_ANSWERS_FILE)
    if WEATHER_ANSWERS is not None:

        print("Loaded ", len(WEATHER_ANSWERS), " weather answers.")


def is_enabled(pconfig: dict, pchat_title: str) -> bool:
    """Возвращает True, если бармен разрешен на этом канале.
    >>> is_enabled({'barman_chats':'Ботовка'}, 'Ботовка')
    True
    >>> is_enabled({'barman_chats':'Хокку'}, 'Ботовка')
    False
    """
    return pchat_title in pconfig[CHANNEL_LIST_KEY]


def can_process(pconfig: dict, pchat_title: str, pmessage_text: str) -> bool:
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


# def get_command(pword_list: list) -> int:
#     """Распознает команду и возвращает её код, в случае неудачи - None.
#     >>> get_command(["пиво",])
#     0
#     >>> get_command(["cognac",])
#     4
#     >>> get_command(["вк",])
#     1
#     >>> get_command(["ck",])
#     6
#     >>> type(get_command(["абракадабра",]))
#     <class 'NoneType'>
#     """
#     command: int = None
#     if pword_list[0] in GREETINGS_WORDS:
#
#         command =
#     if pword_list[0] in SHORT_RUS_BAR_COMMANDS:
#
#         command = SHORT_RUS_BAR_COMMANDS.index(pword_list[0])
#     if pword_list[0] in ENGLISH_BAR_COMMANDS:
#
#         command = ENGLISH_BAR_COMMANDS.index(pword_list[0])
#     if pword_list[0] in SHORT_ENG_BAR_COMMANDS:
#
#         command = SHORT_ENG_BAR_COMMANDS.index(pword_list[0])
#     return command


# def execute_command(pcommand: int, pname_to: str) -> str:
#     """Возвращает текстовый эквивалент команды."""
#
#     message: str = f"{RUSSIAN_BAR_COMMANDS[pcommand]}, сэр!"
#     if pcommand == BEER_ID:
#
#         message = bring_beer(pname_to)
#     if pcommand == COCKTAIL_ID:
#
#         message = bring_cocktail(pname_to)
#     if pcommand == COFFEE_ID:
#
#         message = bring_coffee(pname_to)
#     if pcommand == COGNAC_ID:
#
#         message = bring_cognac(pname_to)
#     if pcommand == COOKIES_ID:
#
#         message = bring_cookies(pname_to)
#     if pcommand == TEA_ID:
#
#         message = bring_tea(pname_to)
#     if pcommand == VODKA_ID:
#
#         message = bring_vodka(pname_to)
#
#     return message


def babbler(pmessage_text: str) -> str:
    """Процедура разбора запроса пользователя."""

    # command: int = None
    message: str = None
    word_list: list = pmessage_text.split(" ")
    # *** Возможно, запросили меню.
    print("*** BBL:BBL:WL ", WEATHER_WORDS)
    if len(pmessage_text) > 2:

        for word in word_list:

            print("*** BBL:BBL:WR ", word)
            if word in " ".join(GREETINGS_WORDS):

                message = f"{random.choice(GREETINGS_ANSWERS)}"
                break
            if word in " ".join(WEATHER_WORDS):

                message = f"{random.choice(WEATHER_ANSWERS)}"
                break
    return message
