# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Модуль антимата для бота."""
import re
from pathlib import Path
# import random
import functions as func
import prototype

RELOAD_BAD_WORDS: list = ["bwreload", "bwrl"]
HINT = ["адм", "adm"]
ENABLED_IN_CHATS_KEY: str = "moderator_chats"
DATA_FOLDER: str = "moderator"
BAD_WORDS_FILE: str = "bad_words.txt"
CENSOR_PREFIX = r"\[\*\*"
CENSOR_POSTFIX = r"\*\*\]"
# BAD_WORDS_MESSAGES: list = ["[ censored ]",
#                             "[ Бип. Бип. Бииииип. ]",
#                             "[ beep. ]",
#                             "[ Мат вырезан. ]"
#                             ]


class CModerator(prototype.CPrototype):
    """Класс модератора."""

    def __init__(self, pbot, pconfig, pdata_path: str):

        super().__init__()
        self.config = pconfig
        self.data_path: str = pdata_path + DATA_FOLDER + "/"
        self.bot = pbot
        self.bad_words: list = []
        self.reload()

    def can_process(self, pchat_title: str, pmessage_text: str) -> bool:
        """Возвращает True, если модуль может обработать команду."""
        word_list: list = func.parse_input(pmessage_text)
        return self.is_enabled(pchat_title) and ((word_list[0] in RELOAD_BAD_WORDS)
                                                 or (word_list[0] in HINT))

    def check_bad_words(self, pmessage) -> bool:
        """Проверяет сообщение на наличие мата."""
        result: bool = False
        if pmessage is not None:

            for word in self.bad_words:

                result = re.match(word, pmessage.lower()) is not None
                if result:
                    break
        return result

    def check_bad_words_ex(self, pmessage) -> str:
        """Проверяет сообщение на наличие мата."""
        answer: str = ""
        detected: bool = False
        if pmessage is not None:

            text: str = pmessage.lower()
            for index, bad_word in enumerate(self.bad_words):

                result: bool = True
                while result:

                    result = re.match(bad_word, text) is not None
                    if result:

                        detected = True
                        words: list = text.split(" ")
                        for wordindex, word in enumerate(words):

                            if re.match(bad_word, word) is not None:

                                words[wordindex] = "*\[beep\]*"
                        text = " ".join(words)
            if detected:

                answer = text

        return answer

    def control_talking(self, pmessage):
        """Следит за матершинниками."""
        answer: str = ""
        text: str
        if pmessage.content_type == "text":

            text = pmessage.text
        else:

            text = pmessage.caption
        if self.is_enabled(pmessage.chat.title):

            text = self.check_bad_words_ex(text)
            if text:

                self.bot.delete_message(chat_id=pmessage.chat.id, message_id=pmessage.message_id)
                answer = pmessage.from_user.first_name
                if pmessage.from_user.last_name:

                    answer += pmessage.from_user.last_name
                print(f"Пользователь {answer} матерился в чате {pmessage.chat.title}.")
                print(f"Он сказал: {text}")
                answer += f" хотел сказать \"{text}\""
        return answer

    def delete_message(self, pmessage):
        """Удаляет сообщение пользователя."""
        # self.bot.delete_message(chat_id=pmessage.chat.id, message_id=pmessage.message_id)
        # print(f"> Сообщение пользователя {pmessage.from_user.username} в чате "
        # "'{pmessage.chat.title}' удалено.")

    def get_help(self, pchat_title: str) -> str:
        """Возвращает список команд модуля, доступных пользователю."""
        return ""

    def get_hint(self, pchat_title: str) -> str:
        """Возвращает команду верхнего уровня, в ответ на которую
           модуль возвращает полный список команд, доступных пользователю."""
        return ", ".join(HINT)

    def is_enabled(self, pchat_title: str) -> bool:
        """Возвращает True, если на этом канале этот модуль разрешен."""
        # print(pchat_title, self.config[ENABLED_IN_CHATS_KEY])
        return pchat_title in self.config[ENABLED_IN_CHATS_KEY]

    def is_master(self, puser_name, puser_title):
        """Проверяет, является ли пользователь хозяином бота."""

        if puser_name == self.config["master"]:
            return True, ""
        # *** Низзя
        print("> Moderator: Запрос на перезагрузку регэкспов "
              f"матерных выражений от нелегитимного лица {puser_title}.")
        return False, f"У вас нет на это прав, {puser_title}."

    def moderator(self, pmessage) -> str:
        """Процедура разбора запроса пользователя."""
        # *** Проверим, всё ли в порядке в чате
        answer: str = self.control_talking(pmessage)
        if not answer:

            if pmessage.text is not None:

                # *** Порядок. Возможно, запрошена команда. Мы ее умеем?
                if self.can_process(pmessage.chat.title, pmessage.text):

                    # *** Да. Возможно, запросили перезагрузку.
                    word_list: list = func.parse_input(pmessage.text)
                    if word_list[0] in RELOAD_BAD_WORDS:

                        # *** Пользователь хочет перезагрузить словарь мата.
                        can_reload, answer = self.is_master(pmessage.from_user.username,
                                                            pmessage.from_user.first_name)
                        if can_reload:

                            self.reload()
                            answer = "Словарь мата обновлен"
                        else:

                            # *** ... но не тут-то было...
                            print(f"> Moderator: Запрос на перегрузку словаря мата от "
                                  f"нелегитимного лица {pmessage.from_user.first_name}.")
                            answer = (f"Извини, {pmessage.from_user.first_name}, "
                                      f"только {self.config['master_name']} может "
                                      "перегружать словарь мата!")
        return answer

    def reload(self):
        """Загружает словарь антимата."""
        # *** Собираем пути
        assert Path(self.data_path).is_dir(), f"{DATA_FOLDER} must be folder"
        data_path = Path(self.data_path) / BAD_WORDS_FILE
        self.bad_words.clear()
        self.bad_words = func.load_from_file(str(data_path))
        print(f"> Moderator успешно (пере)загрузил {len(self.bad_words)} "
              "регэкспов матерных выражений.")
