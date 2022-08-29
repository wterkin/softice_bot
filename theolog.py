# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Модуль цитатника Библии."""

import re
import random
# import string
import functions as func
import prototype

# *** Путь к файлам Библии
# BIBLE_PATH: str = "data/bible/"
THEOLOG_FOLDER: str = "theolog/"
# *** Константы частей сообщения
COMMAND_ARG: int = 0
LINE_ARG: int = 1

# *** Основные команды X
# MAIN_COMMANDS: list = ["книги", "books", "вз", "нз"]

# *** Список книг Библии
BIBLE_BOOKS: list = [["бытие", "быт", "Книга Бытия"],
                     ["исход", "исх", "Книга Исход"],
                     ["левит", "лев", "Книга Левит"],
                     ["числа", "числ", "Книга Числа"],
                     ["второзаконие", "втор", "Книга Второзаконие"],
                     ["инавин", "нав", "Книга Иисуса Навина"],
                     ["судей", "суд", " Книга Судей"],
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
                     ["песни", "песн", "Песнь Песней"],
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
                     ["филимону", "флм", "Послание Филимону"],
                     ["евреям", "евр", "Послание евреям"],
                     ["откровение", "откр", "Откровение Иоанна Богослова"]]

# *** Ключ для списка доступных каналов в словаре конфига
CHANNEL_LIST_KEY: str = "theolog_chats"

# *** Команды поиска текста по книгам Библии
NEW_TESTAMENT: str = "найтинз"
OLD_TESTAMENT: str = "найтивз"
FIND_IN_BOOK: str = "найти"
OLD_TESTAMENT_BOOKS = range(1, 40)
NEW_TESTAMENT_BOOKS = range(40, 67)

THEOLOG_HINT: list = ["книги", "books", f"{OLD_TESTAMENT}", f"{NEW_TESTAMENT}", f"{FIND_IN_BOOK}"]


class CTheolog(prototype.CPrototype):
    """Класс теолога."""

    def __init__(self, pconfig: dict, pdata_path):
        """"Конструктор."""
        super().__init__()
        self.config: dict = pconfig
        self.data_path: str = pdata_path + THEOLOG_FOLDER

    def can_process(self, pchat_title: str, pmessage_text: str) -> bool:
        """Возвращает True, если теолог может обработать эту команду."""
        assert pchat_title is not None, \
            "Assert: [theolog.can_process] No <pchat_title> parameter specified!"
        assert pmessage_text is not None, \
            "Assert: [theolog.can_process] No <pchat_title> parameter specified!"
        if self.is_enabled(pchat_title):

            word_list: list = func.parse_input(pmessage_text)
            if word_list[0].lower() in THEOLOG_HINT:
                return True

            for book in BIBLE_BOOKS:

                if word_list[0].lower() in book:
                    return True
        return False

    def execute_quote(self, pchapter: str, pbook_name: str, pline_count: int) -> str:  # noqa
        """Выполняет поиск заданной главы в Библии."""
        assert pchapter is not None, \
            "Assert: [theolog.execute_quote] No <pchapter> parameter specified!"
        assert pbook_name is not None, \
            "Assert: [theolog.execute_quote] No <pbook_name> parameter specified!"
        message: str = ""
        for book_idx, book in enumerate(BIBLE_BOOKS):

            if pbook_name.lower() in book:

                message = self.find_in_book(book_idx, pchapter, pbook_name, pline_count)
                if message:

                    break
        if not message:

            message = "Нет такой главы и/или стиха в этой книге."

        return message

    def find_in_book(self, pbook_idx: int, pline_id: str, pbook: str,
                     pline_count: int) -> str:  # noqa
        """Ищет заданную строку в файле."""
        assert pbook_idx is not None, \
            "Assert: [theolog.find_in_book] No <pbook_idx> parameter specified!"
        assert pline_id is not None, \
            "Assert: [theolog.find_in_book] No <pline_id> parameter specified!"
        assert pbook is not None, \
            "Assert: [theolog.find_in_book] No <pbook> parameter specified!"
        assert pline_count is not None, \
            "Assert: [theolog.find_in_book] No <pline_count> parameter specified!"
        message: str = ""
        # *** Путь к файлу
        book_name: str = f"{self.data_path}{pbook_idx + 1}.txt"
        with open(book_name, "r", encoding="utf-8") as book_file:

            for line in book_file:

                # *** Ищем в файле заданный идентификатор строки
                regexp = f"^{pline_id}:"
                if re.search(regexp, line) is not None:

                    if ":" in line:

                        chapter_position = line.index(":")
                        chapter = line[:chapter_position]
                        line_position = line.index(":", chapter_position + 1)
                        line_number = line[chapter_position + 1:line_position]
                        text = line[line_position:]
                        message = f"{pbook} {chapter}:{line_number} {text}"
                    if pline_count == 1:

                        break
                elif message:

                    if pline_count > 1:

                        parsed_line: list = line.split(":")
                        message += "\n" + parsed_line[2]
                        pline_count -= 1
                    else:

                        break
        return message

    def get_help(self, pchat_title: str) -> str:
        """Возвращает список команд, поддерживаемых модулем."""

        books: str = ""
        if self.is_enabled(pchat_title):

            for book in BIBLE_BOOKS:

                if not book[0][0].isdigit():

                    books += f"{book[0].capitalize()}({book[1]}), "
                else:

                    books += f"{book[0]}({book[1]}), "
        return books

    def get_hint(self, pchat_title: str) -> str:  # [arguments-differ]
        """Возвращает список команд, поддерживаемых модулем."""
        assert pchat_title is not None, \
            "Assert: [theolog.get_hint] " \
            "No <pchat_title> parameter specified!"
        if self.is_enabled(pchat_title):

            return ", ".join(THEOLOG_HINT)
        return ""

    def global_search(self, ptestament: str, pphrase: str) -> str:  # noqa
        """Ищет заданную строку по всем книгам заданного завета"""
        assert ptestament is not None, \
            "Assert: [theolog.global_search] No <ptestament> parameter specified!"
        assert pphrase is not None, \
            "Assert: [theolog.global_search] No <pphrase> parameter specified!"
        result_list: list = []
        parsed_line: list
        answer: str = ""
        book_name: str = ""
        if ptestament == NEW_TESTAMENT:

            search_range = NEW_TESTAMENT_BOOKS
        elif ptestament == OLD_TESTAMENT:

            search_range = OLD_TESTAMENT_BOOKS
        for book in search_range:
            # print("** ", pphrase)
            book_title: str = BIBLE_BOOKS[book-1][2]
            book_name = f"{self.data_path}{book}.txt"
            with open(book_name, "r", encoding="utf-8") as book_file:

                for line in book_file:

                    lower_line = line.lower()
                    if pphrase in lower_line:

                        parsed_line = re.split(r'\:', line, maxsplit=2)
                        result_list.append(f"{book_title} глава {parsed_line[0]}"
                                           f" стих {parsed_line[1]} : {parsed_line[2]}")
        if len(result_list) > 0:

            answer = random.choice(result_list)
        return answer

    def is_enabled(self, pchat_title: str) -> bool:
        """Возвращает True, если бармен разрешен на этом канале."""
        assert pchat_title is not None, \
            "Assert: [theolog.is_enabled] No <pchat_title> parameter specified!"
        return pchat_title in self.config[CHANNEL_LIST_KEY]

    def reload(self):
        pass

    def search_in_book(self, pbook_file: str, pbook_title: str, pphrase: str):
        """Ищет заданную строку в заданном файле."""
        result_list: list = []
        with open(pbook_file, "r", encoding="utf-8") as book_file:

            for line in book_file:

                lower_line = line.lower()
                parsed_line = re.split(r':', lower_line, maxsplit=2)
                joined_line: str = " ".join(parsed_line[2:])
                if pphrase in joined_line:

                    parsed_line = re.split(r':', line, maxsplit=2)
                    # print(parsed_line, pbook_title)
                    result_line: str = " ".join(parsed_line[2:])
                    result_list.append(f"{pbook_title} глава {parsed_line[0]} стих "
                                       f"{parsed_line[1]}: {result_line}")
        return "\n".join(result_list)

    def theolog(self, pchat_title: str, pmessage_text: str) -> str:
        """Обрабатывает запросы теолога."""
        assert pchat_title is not None, \
            "Assert: [theolog.theolog] No <pchat_title> parameter specified!"
        answer: str = ""
        word_list: list = func.parse_input(pmessage_text)
        line_count: int = 1
        param_count = len(word_list)
        book_name: str
        chapter: str

        if self.can_process(pchat_title, pmessage_text):
            # print("* ", pmessage_text)
            # *** Если есть один параметр, то запрос помощи должен быть это
            if param_count == 1:

                if word_list[COMMAND_ARG] in THEOLOG_HINT:

                    return self.get_help(pchat_title)
            # *** Если есть два параметра, то это книга и глава/стих.
            elif param_count > 1:

                # *** Передали книгу и главу - или команду поиска
                if word_list[0].lower() in [NEW_TESTAMENT, OLD_TESTAMENT]:

                    # *** Команду поиска.
                    testament = word_list[0]
                    phrase = " ".join(word_list[1:]).lower()
                    answer = self.global_search(testament, phrase)
                elif word_list[0].lower() == FIND_IN_BOOK:

                    # *** Искать в книге
                    book_name = word_list[1]
                    book_index: int = -1
                    for index, book in enumerate(BIBLE_BOOKS):

                        if book_name.lower() in book:

                            book_index = index
                            break
                    if book_index >= 0:

                        book_file = f"{self.data_path}/{book_index+1}.txt"
                        answer = self.search_in_book(book_file, BIBLE_BOOKS[book_index][2],
                                                     " ".join(word_list[2:]))
                else:
                    # *** Книгу и главу
                    book_name = word_list[0]
                    chapter = word_list[1]
                    # *** Есть третий параметр, то это количество строк
                    if param_count > 2:

                        # *** И это число?
                        if word_list[2].isdigit():

                            # *** Значит, это количество выводимых строк
                            line_count = int(word_list[2])
                            line_count = 5 if line_count > 5 else line_count
                    answer = self.execute_quote(chapter, book_name, line_count)
            if len(answer) > 0:

                print(f"Theolog answers: {answer[:16]}...")
            else:

                answer = "Ничего не нашёл."
        return answer
