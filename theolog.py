# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Модуль цитатника Библии."""

import re
import random
import functions as func

# *** Путь к файлам Библии
BIBLE_PATH: str = "data/bible/"

# *** Константы частей сообщения
COMMAND_ARG: int = 0
LINE_ARG: int = 1

# *** Основные команды
MAIN_COMMANDS: list = ["книги", "books", "вз", "нз"]

# *** Список книг Библии
BIBLE_BOOKS: list = [["бытие", "быт", "Книга Бытия"],
                     ["исход", "исх", "Книга Исход"],
                     ["левит", "лев", "Книга Левит"],
                     ["числа", "числ", "Книга Числа"],
                     ["второзаконие", "втор", "Книга Второзаконие"],
                     ["инавин", "нав", "Книга Иисуса Навина"],
                     ["судей", "суд"," Книга Судей"],
                     ["руфь", "руфь", "Книга Руфи"],
                     ["1царств", "1цар", "1-я книга Царств"],
                     ["2царств", "2цар", "2-я книга Царств"],
                     ["3царств", "3цар", "3-я книга Царств"],
                     ["4царств", "4цар", "4-я книга Царств"],
                     ["1паралипоменон", "1пар", "1-я книга Паралипоменон"],
                     ["2паралипоменон", "2пар", "2-я книга Паралипоменон"],
                     ["ездра", "езд", "Книга Ездры"],
                     ["неемия", "неем", "Книга Неемии"],
                     ["есфирь", "есф", "Книга Есфири"],
                     ["иов", "иов", "Книга Иова"],
                     ["псалтирь", "пс", "Псалтирь"],
                     ["притчи", "притч", "Книга Притчей"],
                     ["екклесиаст", "еккл", "Книга Екклесиаста"],
                     ["песни", "песн" ,"Песнь Песней"],
                     ["исаии", "ис", "Книга пророка Исайи"],
                     ["иеремии", "иер", "Книга пророка Иеремии"],
                     ["плачиеремии", "плач", "Плач Иеремии"],
                     ["иезекииль", "иез", "Книга пророка Иезекииля"],
                     ["даниил", "дан", "Книга пророка Даниила"],
                     ["осия", "ос", "Книга пророка Осии"],
                     ["иоиль", "иоиль", "Книга пророка Иоиля"],
                     ["амос", "ам", "Книга пророка Амоса"],
                     ["авдий", "ав", "Книга пророка Авдия"],
                     ["иона", "иона", "Книга пророка Ионы"],
                     ["михей", "мих", "Книга пророка Михея"],
                     ["наум", "наум", "Книга пророка Наума"],
                     ["аввакум", "авв", "Книга пророка Аввакума"],
                     ["софония", "соф", "Книга пророка Софонии"],
                     ["аггей", "агг", "Книга пророка Аггея"],
                     ["захария", "зах", "Книга пророка Захарии"],
                     ["малахия", "мал", "Книга пророка Малахии"],
                     ["матфей", "мф", "Евангелие от Матфея"],
                     ["марка", "мк", "Евангелие от Марка"],
                     ["луки", "лк", "Евангелие от Луки"],
                     ["иоанна", "ин", "Евангелие от Иоанна"],
                     ["деяния", "деян", "Деяния апостолов"],
                     ["иакова", "иак", "Послание Иакова"],
                     ["1петра", "1пет", "1-е послание Петра"],
                     ["2петра", "2пет", "2-е послание Петра"],
                     ["1иоанна", "1ин", "1-е послание Иоанна"],
                     ["2иоанна", "2ин", "2-е послание Иоанна"],
                     ["3иоанна", "3ин", "3-е послание Иоанна"],
                     ["иуды", "иуд", "1-е послание Иуды"],
                     ["римлянам", "рим", "Послание римлянам"],
                     ["1коринфянам", "1кор", "1-е послание коринфянам"],
                     ["2коринфянам", "2кор", "2-е послание коринфянам"],
                     ["галатам", "гал", "Послание галатам"],
                     ["ефесянам", "еф", "Послание ефесянам"],
                     ["филиппийцам", "флп", "Послание филиппийцам"],
                     ["колоссянам", "кол", "Послание колоссянам"],
                     ["1фессалоникийцам", "1фес", "1-е послание фессалоникийцам"],
                     ["2фессалоникийцам", "2фес", "2-е послание фессалоникийцам"],
                     ["1тимофею", "1тим", "1-е послание Тимофею"],
                     ["2тимофею", "2тим", "2-е послание Тимофею"],
                     ["титу", "тит", "Послание Титу"],
                     ["филимону", "флм" , "Послание Филимону"],
                     ["евреям", "евр", "Послание евреям"],
                     ["откровение", "откр", "Откровение Иоанна Богослова"]]

# *** Ключ для списка доступных каналов в словаре конфига
CHANNEL_LIST_KEY: str = "theolog_chats"

# *** Команды поиска текста по книгам Библии
NEW_TESTAMENT:str = "нз"
OLD_TESTAMENT:str = "вз"
OLD_TESTAMENT_BOOKS = range(1,40)
NEW_TESTAMENT_BOOKS = range(40,67)

def can_process(pconfig: dict, pchat_title: str, pmessage_text: str) -> bool:
    """Возвращает True, если теолог может обработать эту комманду."""

    if is_enabled(pconfig, pchat_title):

        word_list: list = func.parse_input(pmessage_text)
        if word_list[0] in MAIN_COMMANDS:

            return True

        for book in BIBLE_BOOKS:

            if word_list[0].lower() in book:

                return True
    return False


def get_help(pconfig: dict, pchat_title: str) -> str:
    """Возвращает список команд, поддерживаемых модулем."""

    if is_enabled(pconfig, pchat_title):

        return ", ".join(MAIN_COMMANDS)
    return None


def is_enabled(pconfig: dict, pchat_title: str) -> bool:
    """Возвращает True, если бармен разрешен на этом канале."""

    return pchat_title in pconfig[CHANNEL_LIST_KEY]


def list_books() -> str:
    """Выводит список книг."""

    books: str = ""
    for book in BIBLE_BOOKS:

        books += f"{book[0]}/{book[1]}, "
    return books


def global_search(ptestament: str, pphrase: str) -> str:
    """Ищет заданную строку по всем книгам заданного завета"""
    search_range: object = None
    result_list: list = []
    parsed_line: list = []

    if ptestament == NEW_TESTAMENT:

        search_range = NEW_TESTAMENT_BOOKS
    elif ptestament == OLD_TESTAMENT:

        search_range = OLD_TESTAMENT_BOOKS
    for book in search_range:

        # print(search_range)
        book_title: str = BIBLE_BOOKS[book-1][2]
        book_name: str = f"{BIBLE_PATH}{book}.txt"
        # print(f"*** {book} {book_title} {book_name}")
        with open(book_name, "r", encoding="utf-8") as book_file:

            for line in book_file:

                lower_line = line.lower()
                if pphrase in lower_line:

                    parsed_line = re.split(r'\:', line, maxsplit=2)
                    result_list.append(f"{book_title} глава {parsed_line[0]}"
                                       f" стих {parsed_line[1]} : {parsed_line[2]}")
    if len(result_list) > 0:

        return random.choice(result_list)
    return None


def find_in_book(pbook_idx: int, pline_id: str, pbook: str, pline_count: int) -> str:
    """Ищет заданную строку в файле."""

    message: str = None
    # *** Путь к файлу
    book_name: str = f"{BIBLE_PATH}{pbook_idx+1}.txt"
    with open(book_name, "r", encoding="utf-8") as book_file:

        for line in book_file:

            # *** Ищем в файле заданный идентификатор строки
            regexp = f"^{pline_id}:"
            if re.search(regexp, line) is not None:

                # parsed_line: str = line.split(":")
                if ":" in line:

                    chapter_position = line.index(":")
                    chapter = line[:chapter_position]
                    line_position = line.index(":", chapter_position + 1)
                    line_number = line[chapter_position+1:line_position]
                    text = line[line_position:]
                    message: str = f"{pbook} {chapter}:{line_number} {text}"
                if pline_count == 1:

                    break
            elif message:

                if pline_count > 1:

                    parsed_line: str = line.split(":")
                    message += "\n" + parsed_line[2]
                    pline_count -= 1
                else:

                    break
    return message


def execute_quote(pchapter: str, pbook_name: str, pline_count: int) -> str:
    """Выполняет поиск заданной главы в Библии."""
    message: str = None
    for book_idx, book in enumerate(BIBLE_BOOKS):

        if pbook_name.lower() in book:

            message = find_in_book(book_idx, pchapter, pbook_name, pline_count)
            if message is not None:

                break
    return message


def theolog(pmessage_text: str) -> str:
    """Обрабатывает запросы теолога."""

    message: str = None
    word_list: list = func.parse_input(pmessage_text)
    line_count: int = 1
    param_count = len(word_list)
    book_name: str = ""
    chapter: str = ""
    # *** Если есть один параметр, то запрос помощи должен быть это
    if param_count == 1:

        if word_list[COMMAND_ARG] in MAIN_COMMANDS:

            return list_books()
    # *** Если есть два параметра, то это книга и глава:стих.
    elif param_count > 1:

        # *** Передали книгу и главу - или команду поиска
        if word_list[0].lower() in [NEW_TESTAMENT, OLD_TESTAMENT]:

            testament = word_list[0]
            phrase = " ".join(word_list[1:]).lower()
            message = global_search(testament, phrase)
        else:

            book_name = word_list[0]
            chapter = word_list[1]
            # *** Есть третий параметр, то это количество строк
            if param_count > 2:

                # *** И это число?
                if word_list[2].isdigit():

                    # *** Значит, это количество выводимых строк
                    line_count = int(word_list[2])
                    line_count = 5 if line_count > 5 else line_count
            message = execute_quote(chapter, book_name, line_count)
    return message
