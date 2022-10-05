# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Модуль - цитатник хокку. 俳人"""

# import os
# import random
# from datetime import datetime as dtime
import functions as func
import prototype
import librarian

# *** Команды для цитатника хокку
ASK_HOKKU_CMD: int = 0
FIND_HOKKU_CMD: int = 1
ADD_HOKKU_CMD: int = 2
DEL_HOKKU_CMD: int = 3

RELOAD_BOOK: list = ["hokkureload", "hkrl"]
SAVE_BOOK: list = ["hokkuksave", "hksv"]
HAIJIN_FOLDER: str = "haijin/"
HAIJIN_FILE_NAME: str = "hokku.txt"

HAIJIN_DESC: list = ["Получить случайное хокку",
                     "Найти хокку по фрагменту текста",
                     "Добавить хокку в базу",
                     "Удалить хокку из базы"]

HAIJIN_COMMANDS: list = [["!хк", "!hk"],
                         ["!хк?", "!hk?"],
                         ["!хк+", "!hk+"],
                         ["!хк-", "!hk-"]]

HINT = ["хокку", "hokku"]
ENABLED_IN_CHATS_KEY: str = "haijin_chats"


def get_command(pword: str) -> int:
    """Распознает команду и возвращает её код, в случае неудачи - None.
    """
    assert pword is not None, \
        "Assert: [haijin.get_command] " \
        "No <pword> parameter specified!"
    result: int = -1
    for command_idx, command in enumerate(HAIJIN_COMMANDS):

        if pword in command:
            result = command_idx

    return result


class CHaijin(prototype.CPrototype):
    """Класс хайдзина."""

    def __init__(self, pconfig: dict, pdata_path: str):

        super().__init__()
        self.config = pconfig
        self.data_path = pdata_path + HAIJIN_FOLDER
        self.hokku: list = []
        self.reload()

    def can_process(self, pchat_title: str, pmessage_text: str) -> bool:
        """Возвращает True, если хайдзин может обработать эту команду."""
        assert pchat_title is not None, \
            "Assert: [haijin.can_process] " \
            "No <pchat_title> parameter specified!"
        assert pmessage_text is not None, \
            "Assert: [haijin.can_process] " \
            "No <pmessage_text> parameter specified!"
        found: bool = False
        if self.is_enabled(pchat_title):

            word_list: list = func.parse_input(pmessage_text)
            for command in HAIJIN_COMMANDS:

                found = word_list[0] in command
                if found:

                    break

            if not found:

                found = word_list[0] in HINT
                if not found:

                    found = word_list[0] in RELOAD_BOOK
                    if not found:

                        found = word_list[0] in SAVE_BOOK
        return found

    def get_help(self, pchat_title: str) -> str:
        """Пользователь запросил список команд."""
        assert pchat_title is not None, \
            "Assert: [librarian.get_help] " \
            "No <pchat_title> parameter specified!"
        command_list: str = ""
        if self.is_enabled(pchat_title):

            for idx, command in enumerate(HAIJIN_COMMANDS):

                if idx+1 != len(HAIJIN_COMMANDS):

                    command_list += ", ".join(command) + " : " + HAIJIN_DESC[idx]
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

    def haijin(self, pchat_title, puser_name: str, puser_title: str, pmessage_text: str) -> str:
        """Процедура разбора запроса пользователя."""
        assert pchat_title is not None, \
            "Assert: [haijin.haijin] " \
            "No <pchat_title> parameter specified!"
        assert puser_title is not None, \
            "Assert: [haijin.haijin] " \
            "No <puser_title> parameter specified!"
        command: int
        answer: str = ""
        word_list: list = func.parse_input(pmessage_text)
        if self.can_process(pchat_title, pmessage_text):

            # *** Возможно, запросили перезагрузку.
            if word_list[0] in RELOAD_BOOK:

                # *** Пользователь хочет перезагрузить книгу хокку
                can_reload, answer = self.is_master(puser_name, puser_title)
                if can_reload:

                    self.reload()
                    answer = "Книга загружена"
            elif word_list[0] in SAVE_BOOK:

                # *** Пользователь хочет сохранить книгу хокку
                can_reload, answer = self.is_master(puser_name, puser_title)
                if can_reload:

                    librarian.save_book(self.hokku, self.data_path + HAIJIN_FILE_NAME)
                    answer = "Книга сохранена"
            elif word_list[0] in HINT:

                answer = self.get_help(pchat_title)
            else:

                # *** Получим код команды
                command = get_command(word_list[0])
                if command >= 0:

                    # *** Хокку запрашивали?
                    if command == ASK_HOKKU_CMD:

                        # *** Пользователь хочет хокку....
                        answer = librarian.quote(self.hokku, word_list)
                    elif command == ADD_HOKKU_CMD:

                        # *** Пользователь хочет добавить хокку в книгу
                        self.hokku.append(" ".join(word_list[1:]))
                        answer = f"Спасибо, {puser_title}, хокку добавлено."
                    elif command == DEL_HOKKU_CMD:

                        # *** Пользователь хочет удалить хокку из книги...
                        if puser_name == self.config["master"]:

                            del self.hokku[int(word_list[1])]
                            answer = f"Хокку {word_list[1]} удалена."
                        else:

                            # *** ... но не тут-то было...
                            answer = (f"Извини, {puser_title}, "
                                      f"только {self.config['master_name']} может удалять хокку.")
                    elif command == FIND_HOKKU_CMD:

                        # *** Пользователь хочет найти хокку по заданной строке
                        answer = librarian.find_in_book(self.hokku, word_list)
            if answer:

                print("Haijin answers: ", answer[:16])

        return answer

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
        print("Haijin - нет прав")
        return False, f"У вас нет на это прав, {puser_title}."

    def reload(self):
        """Перезагружает библиотеку."""
        self.hokku = librarian.load_book_from_file(self.data_path + HAIJIN_FILE_NAME)
        print(f"Haijin successfully reload library - {len(self.hokku)} hokku ")
