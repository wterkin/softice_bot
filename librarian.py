# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Модуль - цитатник для бота."""
import os
import random
from datetime import datetime as dtime
import functions as func
import prototype
import messages

# *** Команды для цитатника высказываний
ASK_QUOTE_CMD: int = 0
FIND_QUOTE_CMD: int = 1
ADD_QUOTE_CMD: int = 2
DEL_QUOTE_CMD: int = 3

RELOAD_LIBRARY: list = ["lbreload", "lbrl"]
SAVE_LIBRARY: list = ["lbsave", "lbsv"]
LIBRARIAN_FOLDER: str = "librarian/"
QUOTES_FILE_NAME: str = "quotes.txt"

QUOTES_DESC: list = [" : получить случайную цитату",
                     " : найти цитату по фрагменту текста",
                     " : добавить цитату"]

QUOTES_COMMANDS: list = [["цитата", "цт", "quote", "qt"],
                         ["цитиск", "цт?", "quotefind", "qt?"],
                         ["цитдоб", "цт+", "quoteadd", "qt+"],
                         ["цитудал", "цт-", "quotedel", "qt-"]
                         ]

HINT = ["библиотека", "биб", "library", "lib"]
ENABLED_IN_CHATS_KEY: str = "librarian_chats"


def find_in_book(pbook: list, pword_list: list) -> str:
    """Ищет хокку или цитату в книге по заданной строке"""
    assert pbook is not None, \
        "Assert: [librarian.find_in_book] " \
        "No <pbook> parameter specified!"
    assert pword_list is not None, \
        "Assert: [librarian.find_in_book] " \
        "No <pword_list> parameter specified!"
    answer: str = ""
    result: int = -1
    if len(pword_list) > 1:

        found_list: list = []
        search_line: str = " ".join(pword_list[1:])
        for idx, line in enumerate(pbook):

            if search_line.upper() in line.upper():

                found_list.append(f"[{idx+1}]{line}")
        if len(found_list) > 0:

            answer = random.choice(found_list)
            result = 1
    if not answer:

        answer = messages.MESSAGE_NOT_FOUND
    return answer, result


def get_command(pword: str) -> int:
    """Распознает команду и возвращает её код, в случае неудачи - None.
    """
    assert pword is not None, \
        "Assert: [librarian.get_command] " \
        "No <pword> parameter specified!"
    result: int = -1
    for command_idx, command in enumerate(QUOTES_COMMANDS):

        if pword in command:

            result = command_idx
    return result


def load_book_from_file(pfile_name: str) -> list:  # noqa
    """Загружает файл в список"""
    assert pfile_name is not None, \
        "Assert: [librarian.load_book_from_file] " \
        "No <pfile_name> parameter specified!"
    content: list = []
    # *** откроем файл
    with open(pfile_name, encoding="utf8") as text_file:

        # *** читаем в список
        for line in text_file:

            if line:

                content.append(line.strip())
    return content


def quote(pbook: list, pword_list: list) -> str:
    """ Возвращает хокку или цитату с заданным номером, если номер не задан, то случайную."""
    assert pbook is not None, \
        "Assert: [librarian.quote] " \
        "No <pbook> parameter specified!"
    assert pword_list is not None, \
        "Assert: [librarian.quote] " \
        "No <pword_list> parameter specified!"
    result: int = -1
    if len(pword_list) > 1:

        # *** ... с заданным номером.
        if pword_list[1].isdigit():

            number: int = abs(int(pword_list[1]))
            if number > 0:

                print(f"*** [{number}]")
                if len(pbook) >= number:

                    answer = f"[{number}] {pbook[number-1]}"
                    result = 1
                else:

                    answer = f"Номер должен быть от 1 до {len(pbook)}"
            else:

                answer = "Номер должен быть больше нуля."
        else:

            # answer = messages.MESSAGE_NOT_FOUND
            answer, result = find_in_book(pbook, pword_list)
    else:

        # *** случайную.
        answer = random.choice(pbook)
        answer = f"[{pbook.index(answer)+1}] {answer}"
        result = 1
    return answer, result


def save_book(pbook: list, pbook_name: str): # noqa
    """Сохраняет заданную книгу."""
    assert pbook is not None, \
        "Assert: [librarian.save_book] " \
        "No <pbook> parameter specified!"
    assert pbook_name is not None, \
        "Assert: [librarian.save_book] " \
        "No <pbook_name> parameter specified!"
    new_file_name: str = f"{pbook_name}_{dtime.now().strftime('%Y%m%d-%H%M%S')}"
    os.rename(pbook_name, new_file_name)
    with open(pbook_name, "w", encoding="utf8") as out_file:

        for line in pbook:

            out_file.write(line + "\n")


class CLibrarian(prototype.CPrototype):
    """Класс библиотекаря."""

    def __init__(self, pconfig: dict, pdata_path: str):

        super().__init__()
        self.config = pconfig
        self.data_path = pdata_path + LIBRARIAN_FOLDER
        # self.hokku: list = []
        self.quotes: list = []
        self.reload()

    def can_process(self, pchat_title: str, pmessage_text: str) -> bool:
        """Возвращает True, если библиотекарь может обработать эту команду."""
        assert pchat_title is not None, \
            "Assert: [librarian.can_process] " \
            "No <pchat_title> parameter specified!"
        assert pmessage_text is not None, \
            "Assert: [librarian.can_process] " \
            "No <pmessage_text> parameter specified!"
        found: bool = False
        if self.is_enabled(pchat_title):

            word_list: list = func.parse_input(pmessage_text)
            for command in QUOTES_COMMANDS:

                found = word_list[0] in command
                if found:

                    break
            if not found:

                found = word_list[0] in HINT
                if not found:

                    found = word_list[0] in RELOAD_LIBRARY
                    if not found:

                        found = word_list[0] in SAVE_LIBRARY
        return found

    def execute_quotes_commands(self, puser_name: str, puser_title: str,
                                pword_list: list, pcommand: int) -> str:
        """Выполняет команды, касающиеся базы цитат."""
        assert pword_list is not None, \
            "Assert: [librarian.execute_quotes_commands] " \
            "No <pword_list> parameter specified!"
        assert pcommand is not None, \
            "Assert: [librarian.execute_quotes_commands] " \
            "No <pcommand> parameter specified!"
        answer: str = ""
        result: int = -1
        # *** В зависимости от команды выполняем действия
        if pcommand == ASK_QUOTE_CMD:

            answer = quote(self.quotes, pword_list)
        elif pcommand == ADD_QUOTE_CMD:

            # *** Пользователь хочет добавить цитату в книгу
            self.quotes.append(" ".join(pword_list[1:]))
            answer = f"Спасибо, {puser_title}, цитата добавлена под номером {len(self.quotes)}."
        elif pcommand == DEL_QUOTE_CMD:

            # *** Пользователь хочет удалить цитату из книги...
            if puser_name == self.config["master"]:

                del self.quotes[int(pword_list[1])-1]
                answer = f"Цитата {pword_list[1]} удалена."
            else:

                # *** ... но не тут-то было...
                answer = (f"Извини, {puser_title}, "
                          f"только {self.config['master_name']} может удалять цитаты.")
        elif pcommand == FIND_QUOTE_CMD:

            answer, result = find_in_book(self.quotes, pword_list)
        return answer

    def get_help(self, pchat_title: str) -> str:
        """Пользователь запросил список команд."""
        assert pchat_title is not None, \
            "Assert: [librarian.get_help] " \
            "No <pchat_title> parameter specified!"
        command_list: str = ""
        if self.is_enabled(pchat_title):

            for command in QUOTES_COMMANDS:

                command_list += ", ".join(command)
                command_list += "\n"
        return command_list

    def get_hint(self, pchat_title: str) -> str:  # [arguments-differ]
        """Возвращает список команд, поддерживаемых модулем.  """
        assert pchat_title is not None, \
            "Assert: [barman.get_hint] " \
            "No <pchat_title> parameter specified!"
        if self.is_enabled(pchat_title):

            return ", ".join(HINT)
        return ""

    def is_enabled(self, pchat_title: str) -> bool:
        """Возвращает True, если библиотекарь разрешен на этом канале."""
        assert pchat_title is not None, \
            "Assert: [librarian.is_enabled] " \
            "No <pchat_title> parameter specified!"
        return pchat_title in self.config[ENABLED_IN_CHATS_KEY]

    def is_master(self, puser_name, puser_title):
        """Проверяет, является ли пользователь хозяином бота."""

        if puser_name == self.config["master"]:

            return True, ""
        # *** Низзя
        print("Библиотекарь - нет прав")
        return False, f"У вас нет на это прав, {puser_title}."

    def librarian(self, pchat_title, puser_name: str, puser_title: str, pmessage_text: str) -> str:
        """Процедура разбора запроса пользователя."""
        assert pchat_title is not None, \
            "Assert: [librarian.librarian] " \
            "No <pchat_title> parameter specified!"
        assert puser_title is not None, \
            "Assert: [librarian.librarian] " \
            "No <puser_title> parameter specified!"
        command: int
        answer: str = ""
        word_list: list = func.parse_input(pmessage_text)
        if self.can_process(pchat_title, pmessage_text):

            # *** Возможно, запросили перезагрузку.
            if word_list[0] in RELOAD_LIBRARY:

                # *** Пользователь хочет перезагрузить библиотеку
                can_reload, answer = self.is_master(puser_name, puser_title)
                if can_reload:

                    self.reload()
                    answer = "Книга обновлена"
            elif word_list[0] in SAVE_LIBRARY:

                # *** Пользователь хочет сохранить книгу хокку
                can_reload, answer = self.is_master(puser_name, puser_title)
                if can_reload:

                    save_book(self.quotes, self.data_path + QUOTES_FILE_NAME)
                    answer = "Книга сохранена"
            elif word_list[0] in HINT:

                answer = self.get_help(pchat_title)
            else:
                # *** Получим код команды
                command = get_command(word_list[0])
                # *** Не, цитату
                answer = self.execute_quotes_commands(puser_name, puser_title,
                                                      word_list, command)
            if answer:

                print("Librarian answers: ", answer[:16])

        return answer

    def reload(self):
        """Перезагружает библиотеку."""
        self.quotes = load_book_from_file(self.data_path + QUOTES_FILE_NAME)
        print(f"Librarian successfully reload library - {len(self.quotes)} quotes")
