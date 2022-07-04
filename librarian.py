# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Модуль - цитатник для бота."""
import os
import random
from datetime import datetime as dtime
import functions as func
import prototype

# *** Команды для цитатника хокку
ASK_HOKKU_CMD: int = 0
ADD_HOKKU_CMD: int = 1
DEL_HOKKU_CMD: int = 2
FIND_HOKKU_CMD: int = 3

# *** Команды для цитатника высказываний
ASK_QUOTE_CMD: int = 10
ADD_QUOTE_CMD: int = 11
DEL_QUOTE_CMD: int = 12
FIND_QUOTE_CMD: int = 13

RELOAD_LIBRARY: list = ["libreload", "lrl"]
SAVE_LIBRARY: list = ["libresave", "lsv"]
# *** Ключ для списка доступных каналов в словаре конфига
HOKKU_FILE_NAME: str = "data/hokku.txt"
QUOTES_FILE_NAME: str = "data/quotes.txt"
HOKKU_COMMANDS: list = [["хокку", "хк", "hokku", "hk"],
                        ["хоккудоб", "хк+", "hokkuadd", "hk+"],
                        ["хоккуудал", "хк-", "hokkudel", "hk-"],
                        ["хоккуиск", "хк?", "hokkufind", "hk?"]]
QUOTES_COMMANDS: list = [["цитата", "цт", "quote", "qt"],
                         ["цитатдоб", "цт+", "quoteadd", "qt+"],
                         ["цитатудал", "цт-", "quotedel", "qt-"],
                         ["цитатиск", "цт?", "quotefind", "qt?"]]

HINT = ["библиотека", "ббл", "library", "lib"]
ENABLED_IN_CHATS_KEY: str = "librarian_chats"


class CLibrarian(prototype.CPrototype):
    """Класс библиотекаря."""

    def __init__(self, pconfig):

        super().__init__()
        self.config = pconfig
        self.hokku: list = []
        self.quotes: list = []
        self.reload()

    def can_process(self, pchat_title: str, pmessage_text: str) -> bool:
        """Возвращает True, если бармен может обработать эту команду
        >>> self.can_process({'barman_chats':'Ботовка'}, 'Ботовка', '!vodka')
        True
        >>> self.can_process({'barman_chats':'Хокку'}, 'Ботовка', '!vodka')
        False
        >>> self.can_process({'barman_chats':'Ботовка'}, 'Ботовка', '!мартини')
        False
        """
        assert pchat_title is not None, \
            "Assert: [librarian.can_process] " \
            "No <pchat_title> parameter specified!"
        assert pmessage_text is not None, \
            "Assert: [librarian.can_process] " \
            "No <pmessage_text> parameter specified!"
        found: bool = False
        if self.is_enabled(pchat_title):

            word_list: list = func.parse_input(pmessage_text)
            for command in HOKKU_COMMANDS:

                found = word_list[0] in command
                if found:
                    break
            if not found:

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

    def execute_hokku_commands(self, pfrom_user_name: str, pword_list: list,
                               pcommand: int) -> str:
        """Выполняет команды, касающиеся базы хокку."""

        message: str = ""

        if pcommand == ASK_HOKKU_CMD:

            # *** Пользователь хочет хокку....
            message = self.quote(self.hokku, pword_list)
        elif pcommand == ADD_HOKKU_CMD:

            # *** Пользователь хочет добавить хокку в книгу
            self.hokku.append(" ".join(pword_list[1:]))
            message = f"Спасибо, {pfrom_user_name}, хокку добавлено."
        elif pcommand == DEL_HOKKU_CMD:

            # *** Пользователь хочет удалить хокку из книги...
            if pfrom_user_name == self.config["master"]:

                del self.hokku[int(pword_list[1])]
                message = f"Хокку {pword_list[1]} удалена."
            else:

                # *** ... но не тут-то было...
                message = (f"Извини, {pfrom_user_name}, "
                           f"только {self.config['master_name']} может удалять хокку.")
        elif pcommand == FIND_HOKKU_CMD:

            # *** Пользователь хочет найти хокку по заданной строке
            message = self.find_in_book(self.hokku, pword_list)

        return message

    def execute_quotes_commands(self, pfrom_user_name: str,
                                pword_list: list, pcommand: int) -> str:
        """Выполняет команды, касающиеся базы цитат."""

        message: str = ""
        # *** В зависимости от команды выполняем действия
        if pcommand == ASK_QUOTE_CMD:

            message = self.quote(self.quotes, pword_list)
        elif pcommand == ADD_QUOTE_CMD:

            # *** Пользователь хочет добавить цитату в книгу
            self.quotes.append(" ".join(pword_list[1:]))
            message = f"Спасибо, {pfrom_user_name}, цитата добавлена."
        elif pcommand == DEL_QUOTE_CMD:

            # *** Пользователь хочет удалить цитату из книги...
            if pfrom_user_name == self.config["master"]:

                del self.quotes[int(pword_list[1])]
                message = f"Цитата {pword_list[1]} удалена."
            else:

                # *** ... но не тут-то было...
                message = (f"Извини, {pfrom_user_name}, "
                           f"только {self.config['master_name']} может удалять цитаты.")
        elif pcommand == FIND_QUOTE_CMD:

            message = self.find_in_book(self.quotes, pword_list)
        return message

    def find_in_book(self, pbook: list, pword_list: list) -> str:  # noqa
        """Ищет хокку или цитату в книге по заданной строке"""
        message: str = ""
        if len(pword_list) > 1:

            found_list: list = []
            search_line: str = " ".join(pword_list[1:])
            for line in pbook:

                if search_line in line:

                    found_list.append(line)
            if len(found_list) > 0:

                message = random.choice(found_list)
        if len(message) == 0:

            message = "Извините, ничего не нашёл!"
        return message

    def get_command(self, pword: str) -> int:  # noqa
        """Распознает команду и возвращает её код, в случае неудачи - None.
        """
        assert pword is not None, \
            "Assert: [librarian.get_command] " \
            "No <pword> parameter specified!"
        result: int = -1
        for command_idx, command in enumerate(HOKKU_COMMANDS):

            if pword[0] in command:

                result = command_idx

        if result is None:

            for command_idx, command in enumerate(QUOTES_COMMANDS):

                if pword[0] in command:

                    result = command_idx + 10

        return result

    def get_help(self) -> str:  # noqa
        """Пользователь запросил список комманд."""
        command_list: str = ""
        for command in HOKKU_COMMANDS:

            command_list += ", ".join(command)
            command_list += "\n"
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

        return pchat_title in self.config[ENABLED_IN_CHATS_KEY]

    def librarian(self, pchat_title, puser_name: str, puser_title: str, pmessage_text: str) -> str:
        """Процедура разбора запроса пользователя."""

        command: int
        message: str = ""
        word_list: list = func.parse_input(pmessage_text)
        if self.can_process(pchat_title, pmessage_text):

            # *** Возможно, запросили перезагрузку.
            if word_list[0] in RELOAD_LIBRARY:

                # *** Пользователь хочет перезагрузить библиотеку
                if puser_name == self.config["master"]:

                    self.reload()
                    message = "Библиотека обновлена"
                else:

                    # *** Низзя
                    message = (f"Извини, {puser_title}, "
                               f"только {self.config['master_name']} может перезагружать библиотеку.")
            elif word_list[0] in SAVE_LIBRARY:

                # *** Пользователь хочет сохранить книгу хокку
                if puser_name == self.config["master"]:

                    self.save_book(self.hokku, HOKKU_FILE_NAME)
                    self.save_book(self.quotes, QUOTES_FILE_NAME)
                    message = "Библиотека сохранена"
                else:

                    # *** ... но не тут-то было...
                    message = (f"Извини, {puser_title}, только "
                               f"{self.config['master_name']} может сохранять библиотеку.")

            elif word_list[0] in HINT:

                message = self.get_help()

            else:
                # *** Получим код команды
                command = self.get_command(word_list[0])
                if command >= 0:

                    if command < ASK_QUOTE_CMD:

                        # *** Хокку запрашивали?
                        message = self.execute_hokku_commands(puser_name, word_list, command)
                    else:

                        # *** Не, цитату
                        message = self.execute_quotes_commands(puser_name, word_list, command)

            if len(message) > 0:

                print("Librarian answers: ", message[:16])

        return message

    def load_book_from_file(self, pfile_name: str) -> list:  # noqa
        """Загружает файл в список"""
        content: list = []
        # *** откроем файл
        with open(pfile_name, encoding="utf8") as text_file:

            # *** читаем в список
            for line in text_file:

                if line:

                    content.append(line.strip())
        return content

    def quote(self, pbook: list, pword_list: list) -> str:  # noqa
        """ Возвращает хокку или цитату с заданным номером, если номер не задан, то случайную."""
        message: str
        if len(pword_list) > 1:

            # *** ... с заданным номером.
            number: int = int(pword_list[1])
            message = f"[{number}] {pbook[number]}"
        else:

            # *** случайную.
            message = random.choice(pbook)
            message = f"[{pbook.index(message)}] {message}"
        return message

    def reload(self):
        """Перезагружает библиотеку."""
        self.hokku = self.load_book_from_file(HOKKU_FILE_NAME)
        self.quotes = self.load_book_from_file(QUOTES_FILE_NAME)
        print(f"Librarian successfully reload library - {len(self.hokku)} hokku and {len(self.quotes)}. quotes")

    def save_book(self, pbook: list, pbook_name: str): # noqa
        """Сохраняет заданную книгу."""
        new_file_name: str = f"{pbook_name}_{dtime.now().strftime('%Y%m%d-%H%M%S')}"
        os.rename(pbook_name, new_file_name)
        with open(pbook_name, "w", encoding="utf8") as out_file:

            for line in pbook:

                out_file.write(line + "\n")
