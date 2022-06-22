# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Модуль бармена."""

import random
import functions as func

# *** Идентификаторы, они же индексы, напитков
BEER_ID: int = 0
VODKA_ID: int = 1
COCKTAIL_ID: int = 2
COFFEE_ID: int = 3
COGNAC_ID: int = 4
TEA_ID: int = 5
COOKIES_ID: int = 6

DRINK_SOURCES: list = None
DRINK_TRANSFER: list = None
BEER_CANS: list = None
BEER_MARKS: list = None
COCKTAIL_MARKS: list = None
COFFEE_MARKS: list = None
COFFEE_FILLS: list = None
COGNAC_CANS: list = None
COGNAC_MARKS: list = None
COGNAC_FILLS: list = None
COOKIES_SOURCES: list = None
COOKIES_MARKS: list = None
COOKIES_TRANSFER: list = None
TEA_MARKS: list = None
TEA_FILLS: list = None
VODKA_CANS: list = None
VODKA_MARKS: list = None
VODKA_FILLS: list = None

MENU_MESSAGE: str = "Сегодня в меню у нас имеются следующие напитки: "

# *** Русские команды бара
RUSSIAN_BAR_COMMANDS: list = ["пиво", "водка", "коктейль", "кофе",
                              "коньяк", "чай", "печеньки"]

# *** Английские команды бара
ENGLISH_BAR_COMMANDS: list = ["beer", "vodka", "cocktail", "coffee",
                              "cognac", "tea", "cookies"]

# *** Укороченные русские команды бара
SHORT_RUS_BAR_COMMANDS: list = ["пв", "вк", "кт", "кф",
                                "кн", "чй", "пч"]

# *** Укороченные английские команды бара
SHORT_ENG_BAR_COMMANDS: list = ["br", "vk", "ct", "cf",
                                "cn", "te", "ck"]

# *** Команды вызова меню
MAIN_COMMANDS_LIST: list = ["меню", "menu", "бар", "bar"]
MAIN_COMMANDS_STRING: str = "меню, (menu, бар, bar)"

BEER_EMODJI: str = "🍺"
COFFEE_EMODJI: str = "☕️"
COGNAC_EMODJI: str = "🥃"
COCTAIL_EMODJI: str = "🍹"
COOKIE_EMODJI: str = "🍪"
# *** Команда перегрузки текстов
BAR_RELOAD: list = ["barreload", "br"]

# *** Ключ для списка доступных каналов в словаре конфига
CHANNEL_LIST_KEY: str = "barman_chats"

#    ... if data_list is None:
#   ...        print("No")
#    ...    else:
#    ...        print("Yes")

def load_from_file(pfile_name: str) -> list:
    """Загружает файл в список
    >>> load_from_file("data/bar/bar_test.txt")
    ['Test 1', 'Test 2', 'Test 3']
    >>> type(load_from_file("ABCDEF"))
    <class 'NoneType'>
    """
    content: list = None
    # *** откроем файл
    try:

        with open(pfile_name, encoding="utf8") as text_file:

            content = []
            # *** читаем в список
            for line in text_file:

                if line:

                    content.append(line.strip())
    except FileNotFoundError:

        return content
    return content


def reload_alcohol():
    """Перезагружает алкоголь."""

    global BEER_CANS
    BEER_CANS = load_from_file("data/bar/beer_cans.txt")
    if BEER_CANS is not None:

        print("Loaded ", len(BEER_CANS), " beer cans.")

    global BEER_MARKS
    BEER_MARKS = load_from_file("data/bar/beer_marks.txt")
    if BEER_MARKS is not None:

        print("Loaded ", len(BEER_MARKS), " beer marks.")

    global COCKTAIL_MARKS
    COCKTAIL_MARKS = load_from_file("data/bar/cocktail_marks.txt")
    if COCKTAIL_MARKS is not None:

        print("Loaded ", len(COCKTAIL_MARKS), " cocktail marks.")

    global COGNAC_CANS
    COGNAC_CANS = load_from_file("data/bar/cognac_cans.txt")
    if COGNAC_CANS is not None:

        print("Loaded ", len(COGNAC_CANS), " cognac cans.")

    global COGNAC_MARKS
    COGNAC_MARKS = load_from_file("data/bar/cognac_marks.txt")
    if COGNAC_MARKS is not None:

        print("Loaded ", len(COGNAC_MARKS), " cognac marks.")

    global COGNAC_FILLS
    COGNAC_FILLS = load_from_file("data/bar/cognac_fills.txt")
    if COGNAC_FILLS is not None:

        print("Loaded ", len(COGNAC_FILLS), " cognac fills.")

    global VODKA_CANS
    VODKA_CANS = load_from_file("data/bar/vodka_cans.txt")
    if VODKA_CANS is not None:

        print("Loaded ", len(VODKA_CANS), " vodka cans.")

    global VODKA_MARKS
    VODKA_MARKS = load_from_file("data/bar/vodka_marks.txt")
    if VODKA_MARKS is not None:

        print("Loaded ", len(VODKA_MARKS), " vodka marks.")

    global VODKA_FILLS
    VODKA_FILLS = load_from_file("data/bar/vodka_fills.txt")
    if VODKA_FILLS is not None:

        print("Loaded ", len(VODKA_FILLS), " vodka fills.")


def reload_alcohol_free():
    """Перезагружает безалкогольные напитки."""

    global COFFEE_MARKS
    COFFEE_MARKS = load_from_file("data/bar/coffee_marks.txt")
    print("Loaded ", len(COFFEE_MARKS), " coffee marks.")

    global COFFEE_FILLS
    COFFEE_FILLS = load_from_file("data/bar/coffee_fills.txt")
    print("Loaded ", len(COFFEE_FILLS), " coffee fills.")

    global COOKIES_SOURCES
    COOKIES_SOURCES = load_from_file("data/bar/cookies_sources.txt")
    print("Loaded ", len(COOKIES_SOURCES), " cookies sources.")

    global COOKIES_MARKS
    COOKIES_MARKS = load_from_file("data/bar/cookies_marks.txt")
    print("Loaded ", len(COOKIES_MARKS), " cookies marks.")

    global COOKIES_TRANSFER
    COOKIES_TRANSFER = load_from_file("data/bar/cookies_transfer.txt")
    print("Loaded ", len(COOKIES_TRANSFER), " cookies transfers.")

    global TEA_MARKS
    TEA_MARKS = load_from_file("data/bar/tea_marks.txt")
    print("Loaded ", len(TEA_MARKS), " tea marks.")

    global TEA_FILLS
    TEA_FILLS = load_from_file("data/bar/tea_fills.txt")
    print("Loaded ", len(TEA_FILLS), " tea fills.")


def reload_bar():
    """Перезагружает тексты из файлов в списки."""

    global DRINK_SOURCES
    DRINK_SOURCES = load_from_file("data/bar/drink_sources.txt")
    print("Loaded ", len(DRINK_SOURCES), " drink sources.")

    global DRINK_TRANSFER
    DRINK_TRANSFER = load_from_file("data/bar/drink_transfer.txt")
    print("Loaded ", len(DRINK_TRANSFER), " drink transfers.")

    reload_alcohol()
    reload_alcohol_free()


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

        word_list: list = func.parse_input(pmessage_text)
        return ((word_list[0] in RUSSIAN_BAR_COMMANDS) or
                (word_list[0] in SHORT_RUS_BAR_COMMANDS) or
                (word_list[0] in ENGLISH_BAR_COMMANDS) or
                (word_list[0] in SHORT_ENG_BAR_COMMANDS) or
                (word_list[0] in MAIN_COMMANDS_LIST) or
                (word_list[0] in BAR_RELOAD))
    return False


def get_command_list() -> str:
    """Пользователь запросил список комманд."""
    command_list: str = ""
    for command_idx, command in enumerate(RUSSIAN_BAR_COMMANDS):

        command_list += (f"{command} "
                         f"({SHORT_RUS_BAR_COMMANDS[command_idx]}, "
                         f"{ENGLISH_BAR_COMMANDS[command_idx]}, "
                         f"{SHORT_ENG_BAR_COMMANDS[command_idx]}). ")
    return command_list


def get_help(pconfig: dict, pchat_title: str) -> str:
    """Возвращает список команд, поддерживаемых модулем.
    >>> get_help({'barman_chats':'Ботовка'}, 'Ботовка')
    'меню, (menu, бар, bar)'
    >>> type(get_help({'barman_chats':'Хокку'}, 'Ботовка'))
    <class 'NoneType'>
    """

    if is_enabled(pconfig, pchat_title):

        return "меню, (menu, бар, bar)"
    return None


def is_enabled(pconfig: dict, pchat_title: str) -> bool:
    """Возвращает True, если бармен разрешен на этом канале.
    >>> is_enabled({'barman_chats':'Ботовка'}, 'Ботовка')
    True
    >>> is_enabled({'barman_chats':'Хокку'}, 'Ботовка')
    False
    """
    return pchat_title in pconfig[CHANNEL_LIST_KEY]


def bring_beer(puser_name: str) -> str:
    """Пользователь запросил пиво."""

    if (DRINK_SOURCES is not None and
       BEER_CANS is not None and
       BEER_MARKS is not None and
       DRINK_TRANSFER  is not None):
        source: str = random.choice(DRINK_SOURCES)
        can: str = random.choice(BEER_CANS)
        beer: str = random.choice(BEER_MARKS)
        transfer: str = random.choice(DRINK_TRANSFER)
        return f"Softice {source} {can} пива \"{beer}\" {transfer} {puser_name} {BEER_EMODJI}"
    return "А нету пива!"


def bring_cocktail(puser_name: str) -> str:
    """Пользователь запросил коктейль."""

    if (DRINK_SOURCES is not None and
       COCKTAIL_MARKS is not None and
       VODKA_FILLS is not None):
        source: str = random.choice(DRINK_SOURCES)
        cocktail: str = random.choice(COCKTAIL_MARKS)
        transfer: str = random.choice(VODKA_FILLS)
        return f"Softice {source} {cocktail} и {transfer} {puser_name} {COCTAIL_EMODJI}"
    return "Кончились коктейли!"


def bring_coffee(puser_name: str) -> str:
    """Пользователь запросил кофе."""

    if (COFFEE_FILLS is not None and
       COFFEE_MARKS is not None and
       DRINK_TRANSFER is not None):
        fill: str = random.choice(COFFEE_FILLS)
        coffee: str = random.choice(COFFEE_MARKS)
        transfer: str = random.choice(DRINK_TRANSFER)
        return f"Softice {fill} кофе \"{coffee}\" {transfer} {puser_name} {COFFEE_EMODJI}"
    return "Кофе весь вышел."


def bring_cognac(puser_name: str) -> str:
    """Пользователь запросил коньяк."""

    if (DRINK_SOURCES is not None and
       COGNAC_CANS is not None and
       COGNAC_MARKS is not None and
       COGNAC_FILLS is not None):
        source: str = random.choice(DRINK_SOURCES)
        can: str = random.choice(COGNAC_CANS)
        cognac: str = random.choice(COGNAC_MARKS)
        transfer: str = random.choice(COGNAC_FILLS)
        return f"Softice {source} {can} {cognac} и {transfer} {puser_name} {COGNAC_EMODJI}"
    return "Выпили весь коньяк."


def bring_cookies(puser_name: str) -> str:
    """Пользователь запросил печеньки."""

    if (COOKIES_SOURCES is not None and
       COOKIES_MARKS is not None and
       COOKIES_TRANSFER is not None):
        source: str = random.choice(COOKIES_SOURCES)
        can: str = "пачку"
        cookies: str = random.choice(COOKIES_MARKS)
        transfer: str = random.choice(COOKIES_TRANSFER)
        return f"Softice {source} {can} печенья \"{cookies}\" {transfer} {puser_name} {COOKIE_EMODJI}"
    return "Нету печенья. Съели."


def bring_tea(puser_name: str) -> str:
    """Пользователь запросил чай."""

    if (TEA_FILLS is not None and
       TEA_MARKS is not None and
       DRINK_TRANSFER is not None):
        fill: str = random.choice(TEA_FILLS)
        tea: str = random.choice(TEA_MARKS)
        transfer: str = random.choice(DRINK_TRANSFER)
        return f"Softice {fill} {tea} {transfer} {puser_name}"
    return "Чаю нет."


def bring_vodka(puser_name: str) -> str:
    """Пользователь запросил пиво."""

    if (DRINK_SOURCES is not None and
       VODKA_CANS is not None and
       VODKA_MARKS is not None and
       VODKA_FILLS is not None):
        source: str = random.choice(DRINK_SOURCES)
        can: str = random.choice(VODKA_CANS)
        vodka: str = random.choice(VODKA_MARKS)
        transfer: str = random.choice(VODKA_FILLS)
        return f"Softice {source} {can} {vodka} и {transfer} {puser_name}"
    return "А водочка-то тютю. Кончилась вся."


def get_command(pword_list: list) -> int:
    """Распознает команду и возвращает её код, в случае неудачи - None.
    >>> get_command(["пиво",])
    0
    >>> get_command(["cognac",])
    4
    >>> get_command(["вк",])
    1
    >>> get_command(["ck",])
    6
    >>> type(get_command(["абракадабра",]))
    <class 'NoneType'>
    """
    command: int = None
    if pword_list[0] in RUSSIAN_BAR_COMMANDS:

        command = RUSSIAN_BAR_COMMANDS.index(pword_list[0])
    if pword_list[0] in SHORT_RUS_BAR_COMMANDS:

        command = SHORT_RUS_BAR_COMMANDS.index(pword_list[0])
    if pword_list[0] in ENGLISH_BAR_COMMANDS:

        command = ENGLISH_BAR_COMMANDS.index(pword_list[0])
    if pword_list[0] in SHORT_ENG_BAR_COMMANDS:

        command = SHORT_ENG_BAR_COMMANDS.index(pword_list[0])
    return command


def execute_command(pcommand: int, pname_to: str) -> str:
    """Возвращает текстовый эквивалент команды."""

    message: str = f"{RUSSIAN_BAR_COMMANDS[pcommand]}, сэр!"
    if pcommand == BEER_ID:

        message = bring_beer(pname_to)
    if pcommand == COCKTAIL_ID:

        message = bring_cocktail(pname_to)
    if pcommand == COFFEE_ID:

        message = bring_coffee(pname_to)
    if pcommand == COGNAC_ID:

        message = bring_cognac(pname_to)
    if pcommand == COOKIES_ID:

        message = bring_cookies(pname_to)
    if pcommand == TEA_ID:

        message = bring_tea(pname_to)
    if pcommand == VODKA_ID:

        message = bring_vodka(pname_to)

    return message


def barman(pmessage_text: str, pfrom_user_name: str) -> str:
    """Процедура разбора запроса пользователя."""

    command: int = None
    message: str = None
    word_list: list = func.parse_input(pmessage_text)
    # *** Возможно, запросили меню.
    if word_list[0] in MAIN_COMMANDS_LIST:

        message = f"{MENU_MESSAGE}\n{get_command_list()}"
    elif word_list[0] in BAR_RELOAD:

        reload_bar()
        message = "Содержимое бара обновлено"
    else:

        # *** Нет, видимо, напиток.
        command = get_command(word_list)
        name_to = pfrom_user_name
        if len(word_list) > 1:

            name_to = word_list[1]
        # *** В зависимости от команды выполняем действия
        message = execute_command(command, name_to)
    return message
