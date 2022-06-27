## -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Модуль - цитатник для бота."""
import os
import random
from datetime import datetime as dtime
import functions as func

# *** Команды для цитатника хокку
RUSSIAN_HOKKU_COMMANDS: list = ["хокку", "добхк", "удалхк", "сохрхк", "искх"]
SHORT_RUS_HOKKU_COMMANDS: list = ["х", "х+", "х-", "х!", "х?"]
ENGLISH_HOKKU_COMMANDS: list = ["hokku", "addh", "delh", "saveh", "findh"]
SHORT_ENG_HOKKU_COMMANDS: list = ["h", "h+", "h-", "h!", "h?"]
ASK_HOKKU_CMD: int = 0
ADD_HOKKU_CMD: int = 1
DEL_HOKKU_CMD: int = 2
SAVE_HOKKU_CMD: int = 3
FIND_HOKKU_CMD: int = 4

# *** Команды для цитатника высказываний
RUSSIAN_QUOTES_COMMANDS: list = ["цитата", "добцт", "удалцт", "сохрцт", "искцт"]
SHORT_RUS_QUOTES_COMMANDS: list = ["ц", "ц+", "ц-", "ц!", "ц?"]
ENGLISH_QUOTES_COMMANDS: list = ["quotes", "addq", "delq", "saveq", "findq"]
SHORT_ENG_QUOTES_COMMANDS: list = ["q", "q+", "q-", "q!", "q?"]
ASK_QUOTE_CMD: int = 10
ADD_QUOTE_CMD: int = 11
DEL_QUOTE_CMD: int = 12
SAVE_QUOTE_CMD: int = 13
FIND_QUOTE_CMD: int = 14

RELOAD_LIBRARY: list = ["libreload", "lrl"]
# *** Ключ для списка доступных каналов в словаре конфига
CHANNEL_LIST_KEY: str = "librarian_chats"

HOKKU_FILE_NAME: str = "data/hokku.txt"
QUOTES_FILE_NAME: str = "data/quotes.txt"

HOKKU_BOOK: list = None
QUOTES_BOOK: list = None


def ask_book(pbook: list, pword_list: list) -> str:
    """ Возвращает хокку с заданным номером, если номер не задан, то случайную."""

    message: str = None
    if len(pword_list) > 1:

        # *** ... с заданным номером.
        number: int = int(pword_list[1])
        message = f"[{number}] {pbook[number]}"
    else:

        # *** случайную.
        message = random.choice(pbook)
        message = f"[{pbook.index(message)}] {message}"
    return message


def can_process(pconfig: dict, pchat_title: str, pmessage_text: str) -> bool:
    """Возвращает True, если библиотекарь может обработать эту команду."""

    if is_enabled(pconfig, pchat_title):

        word_list: list = func.parse_input(pmessage_text)
        return ((word_list[0] in RUSSIAN_HOKKU_COMMANDS) or
                (word_list[0] in SHORT_RUS_HOKKU_COMMANDS) or
                (word_list[0] in ENGLISH_HOKKU_COMMANDS) or
                (word_list[0] in SHORT_RUS_QUOTES_COMMANDS) or
                (word_list[0] in SHORT_ENG_HOKKU_COMMANDS) or
                (word_list[0] in RUSSIAN_QUOTES_COMMANDS) or
                (word_list[0] in ENGLISH_QUOTES_COMMANDS) or
                (word_list[0] in SHORT_ENG_QUOTES_COMMANDS) or
                (word_list[0] in RELOAD_LIBRARY))

    return False


def find_in_book(pbook: list, pword_list: list) -> str:
    """Ищет хокку в книге по заданной строке"""

    message: str = None
    if len(pword_list) > 1:

        found_list: list = []
        search_line: str = " ".join(pword_list[1:])
        for line in pbook:

            if search_line in line:

                found_list.append(line)
        if len(found_list) > 0:

            message = random.choice(found_list)
    if message is None:

        message = "Извините, ничего не нашёл!"
    return message


def get_help(pconfig: dict, pchat_title: str) -> str:
    """Возвращает список команд, поддерживаемых модулем."""

    if is_enabled(pconfig, pchat_title):

        hokku_command_list: str = ""
        quotes_command_list: str = ""
        for command_idx, command in enumerate(RUSSIAN_HOKKU_COMMANDS):

            hokku_command_list += (f"{command}, "
                                   f"({SHORT_RUS_HOKKU_COMMANDS[command_idx]}, "
                                   f"{ENGLISH_HOKKU_COMMANDS[command_idx]}, "
                                   f"{SHORT_ENG_HOKKU_COMMANDS[command_idx]}). ")
            quotes_command_list += (f"{RUSSIAN_QUOTES_COMMANDS[command_idx]}, "
                                    f"({SHORT_RUS_QUOTES_COMMANDS[command_idx]}, "
                                    f"{ENGLISH_QUOTES_COMMANDS[command_idx]}, "
                                    f"{SHORT_ENG_QUOTES_COMMANDS[command_idx]}). ")

        return hokku_command_list + quotes_command_list
    return None


def is_enabled(pconfig: dict, pchat_title: str) -> bool:
    """Возвращает True, если библиотекарь разрешен на этом канале."""

    return pchat_title in pconfig[CHANNEL_LIST_KEY]


def load_book_from_file(pfile_name: str) -> list:
    """Загружает файл в список"""
    content: list = []
    # *** откроем файл
    with open(pfile_name, encoding="utf8") as text_file:

        # *** читаем в список
        for line in text_file:

            if line:

                content.append(line.strip())
    return content


def reload_library():
    """Перезагружает библиотеку."""
    global HOKKU_BOOK
    HOKKU_BOOK = load_book_from_file(HOKKU_FILE_NAME)
    print("Loaded ", len(HOKKU_BOOK), " hokku.")

    global QUOTES_BOOK
    QUOTES_BOOK = load_book_from_file(QUOTES_FILE_NAME)
    print("Loaded ", len(QUOTES_BOOK), " quotes.")


def save_book(pbook: list, pbook_name: str) -> str:
    """Сохраняет заданную книгу."""
    message: str = None
    new_file_name: str = f"{pbook_name}_{dtime.now().strftime('%Y%m%d-%H%M%S')}"
    os.rename(pbook_name, new_file_name)
    # try:

    with open(pbook_name, "w", encoding="utf8") as out_file:

        for line in pbook:

            out_file.write(line + "\n")
    message = "Книга сохранена."
    # except:

        # *** Ошибка. Восстанавливаем старую книгу.
        # os.rename(new_file_name, pbook_name)
        # message = "В процессе сохранения книги произошла ошибка."
    return message


def get_command(pword_list):
    """Возвращает заданную команду."""

    command: int = None
    # *** Нет, видимо, текст.
    if pword_list[0] in RUSSIAN_HOKKU_COMMANDS:

        command = RUSSIAN_HOKKU_COMMANDS.index(pword_list[0])
    elif pword_list[0] in SHORT_RUS_HOKKU_COMMANDS:

        command = SHORT_RUS_HOKKU_COMMANDS.index(pword_list[0])
    elif pword_list[0] in ENGLISH_HOKKU_COMMANDS:

        command = ENGLISH_HOKKU_COMMANDS.index(pword_list[0])
    elif pword_list[0] in SHORT_ENG_HOKKU_COMMANDS:

        command = SHORT_ENG_HOKKU_COMMANDS.index(pword_list[0])
    if pword_list[0] in RUSSIAN_QUOTES_COMMANDS:

        command = RUSSIAN_QUOTES_COMMANDS.index(pword_list[0]) + 10
    elif pword_list[0] in SHORT_RUS_QUOTES_COMMANDS:

        command = SHORT_RUS_QUOTES_COMMANDS.index(pword_list[0]) + 10
    elif pword_list[0] in ENGLISH_QUOTES_COMMANDS:

        command = ENGLISH_QUOTES_COMMANDS.index(pword_list[0]) + 10
    elif pword_list[0] in SHORT_ENG_QUOTES_COMMANDS:

        command = SHORT_ENG_QUOTES_COMMANDS.index(pword_list[0]) + 10
    return command


def execute_hokku_commands(pconfig: dict, pfrom_user_name: str, pword_list: list,
                           pcommand: int) -> str:
    """Выполняет команды, касающиеся базы хокку."""

    message: str = None
    if pcommand == ASK_HOKKU_CMD:

        # *** Пользователь хочет хокку....
        message = ask_book(HOKKU_BOOK, pword_list)
    elif pcommand == ADD_HOKKU_CMD:

        # *** Пользователь хочет добавить хокку в книгу
        HOKKU_BOOK.append(" ".join(pword_list[1:]))
        message = f"Спасибо, {pfrom_user_name}, хокку добавлено."
    elif pcommand == DEL_HOKKU_CMD:

        # *** Пользователь хочет удалить хокку из книги...
        if pfrom_user_name == pconfig["master"]:

            del HOKKU_BOOK[int(pword_list[1])]
            message = f"Хокку {pword_list[1]} удалена."
        else:

            # *** ... но не тут-то было...
            message = (f"Извини, {pfrom_user_name}, "
                       f"только {pconfig['master_name']} может удалять хокку.")
    elif pcommand == SAVE_HOKKU_CMD:

        # *** Пользователь хочет сохранить книгу хокку
        if pfrom_user_name == pconfig["master"]:

            message = save_book(HOKKU_BOOK, HOKKU_FILE_NAME)
        else:

            # *** ... но не тут-то было...
            message = (f"Извини, {pfrom_user_name}, только "
                       f"{pconfig['master_name']} может сохранять книгу.")
    elif pcommand == FIND_HOKKU_CMD:

        # *** Пользователь хочет найти хокку по заданной строке
        message = find_in_book(HOKKU_BOOK, pword_list)

    return message


def execute_quotes_commands(pconfig: dict, pfrom_user_name: str,
                            pword_list: list, pcommand: int) -> str:
    """Выполняет команды, касающиеся базы цитат."""

    message: str = None
    # *** В зависимости от команды выполняем действия
    if pcommand == ASK_QUOTE_CMD:

        message = ask_book(QUOTES_BOOK, pword_list)
    elif pcommand == ADD_QUOTE_CMD:

        # *** Пользователь хочет добавить цитату в книгу
        QUOTES_BOOK.append(" ".join(pword_list[1:]))
        message = f"Спасибо, {pfrom_user_name}, цитата добавлена."
    elif pcommand == DEL_QUOTE_CMD:

        # *** Пользователь хочет удалить цитату из книги...
        if pfrom_user_name == pconfig["master"]:

            del QUOTES_BOOK[int(pword_list[1])]
            message = f"Цитата {pword_list[1]} удалена."
        else:

            # *** ... но не тут-то было...
            message = (f"Извини, {pfrom_user_name}, "
                       f"только {pconfig['master_name']} может удалять цитаты.")
    elif pcommand == SAVE_QUOTE_CMD:

        # *** Пользователь хочет сохранить книгу цитат
        if pfrom_user_name == pconfig["master"]:

            message = save_book(HOKKU_BOOK, HOKKU_FILE_NAME)
        else:

            # *** ... но не тут-то было...
            message = (f"Извини, {pfrom_user_name}, только "
                       f"{pconfig['master_name']} может сохранять книгу.")
    elif pcommand == FIND_QUOTE_CMD:

        message = find_in_book(QUOTES_BOOK, pword_list)
    return message


def librarian(pconfig: dict, pfrom_user_name: str, pmessage_text: str) -> str:
    """Процедура разбора запроса пользователя."""

    # global HOKKU_BOOK
    # global QUOTES_BOOK
    command: int = None
    message: str = None
    word_list: list = func.parse_input(pmessage_text)
    # *** Возможно, запросили перезагрузку.
    if word_list[0] in RELOAD_LIBRARY:

        # *** Пользователь хочет перезагрузить библиотеку
        if pfrom_user_name == pconfig["master"]:

            reload_library()
            message = "Библиотека обновлена"
        else:

            message = (f"Извини, {pfrom_user_name}, "
                       f"только {pconfig['master_name']} может перезагружать библиотеку.")
    else:

        command = get_command(word_list)
        # print(command)
        message = execute_hokku_commands(pconfig, pfrom_user_name, word_list, command)
        if message is None:

            message = execute_quotes_commands(pconfig, pfrom_user_name, word_list, command)
        # print(message)

    return message
