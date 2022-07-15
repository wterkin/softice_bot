# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Модуль бармена."""

import random

import functions as func
import prototype

# *** Идентификаторы, они же индексы, напитков
BEER_ID: int = 0
VODKA_ID: int = 1
COGNAC_ID: int = 2
COCKTAIL_ID: int = 3
TEA_ID: int = 4
COFFEE_ID: int = 5
COOKIES_ID: int = 6

COMMANDS: list = [["пиво", "beer", "пв", "br"],
                  ["водка", "vodka", "вк", "vk"],
                  ["коньяк", "cognac", "кн", "cn"],
                  ["коктейль", "cocktail", "кт", "ct"],
                  ["чай", "tea", "чй", "te"],
                  ["кофе", "coffee", "кф", "cf"],
                  ["печеньки", "cookies", "пч", "ck"]]

BEER_EMODJI: str = "🍺"
COFFEE_EMODJI: str = "☕️"
COGNAC_EMODJI: str = "🥃"
COCKTAIL_EMODJI: str = "🍹"
COOKIE_EMODJI: str = "🍪"
BARMAN_FOLDER: str = "barman/"
# *** Команда перегрузки текстов
BAR_RELOAD: list = ["barreload", "brl"]

BEER_CANS_PATH: str = "beer_cans.txt"
BEER_MARKS_PATH: str = "beer_marks.txt"
BEER_CANS_KEY: str = "bcans"
BEER_MARKS_KEY: str = "bmarks"

COCKTAIL_MARKS_PATH: str = "cocktail_marks.txt"

COFFEE_MARKS_PATH: str = "coffee_marks.txt"
COFFEE_MARKS_KEY: str = "cfmarks"
COFFEE_FILLS_PATH: str = "coffee_fills.txt"
COFFEE_FILLS_KEY: str = "cffills"

COGNAC_CANS_PATH: str = "cognac_cans.txt"
COGNAC_CANS_KEY: str = "cgcans"
COGNAC_MARKS_PATH: str = "cognac_marks.txt"
COGNAC_MARKS_KEY: str = "cgmarks"
COGNAC_FILLS_PATH: str = "cognac_fills.txt"
COGNAC_FILLS_KEY: str = "cgfills"

COOKIES_SOURCES_PATH: str = "cookies_sources.txt"
COOKIES_SOURCES_KEY: str = "cksrc"
COOKIES_MARKS_PATH: str = "cookies_marks.txt"
COOKIES_MARKS_KEY: str = "ckmrk"
COOKIES_TRANSFER_PATH: str = "cookies_transfer.txt"
COOKIES_TRANSFER_KEY: str = "cktrf"

DRINKS_SOURCES_PATH: str = "drink_sources.txt"
DRINKS_SOURCES_KEY: str = "drsrc"
DRINKS_TRANSFER_PATH: str = "drink_transfer.txt"
DRINKS_TRANSFER_KEY: str = "drtrf"

TEA_MARKS_PATH: str = "tea_marks.txt"
TEA_MARKS_KEY: str = "teamr"
TEA_FILLS_PATH: str = "tea_fills.txt"
TEA_FILLS_KEY: str = "teafl"

VODKA_CANS_PATH: str = "vodka_cans.txt"
VODKA_CANS_KEY: str = "vdcans"
VODKA_MARKS_PATH: str = "vodka_marks.txt"
VODKA_MARKS_KEY: str = "vdmarks"
VODKA_FILLS_PATH: str = "vodka_fills.txt"
VODKA_FILLS_KEY: str = "vdfills"

# *** Ключ для списка доступных каналов в словаре конфига
ENABLED_IN_CHATS_KEY: str = "barman_chats"
BAR_HINT: list = ["бар", "bar"]


class CBarman(prototype.CPrototype):
    """Класс бармена."""

    def __init__(self, pconfig, pdata_path):

        super().__init__()
        self.config = pconfig
        self.data_path = pdata_path+BARMAN_FOLDER
        print(self.data_path)
        self.beer: dict = {}
        self.cocktail: list = []
        self.cognac: dict = {}
        self.vodka: dict = {}
        self.coffee: dict = {}
        self.cookies: dict = {}
        self.tea: dict = {}
        self.drinks: dict = {}
        self.reload()

    def barman(self, pchat_title: str, pmessage_text: str, puser_title: str) -> str:
        """Процедура разбора запроса пользователя."""
        assert pchat_title is not None, \
            "Assert: [barman.barman] No <pchat_title> parameter specified!"
        assert puser_title is not None, \
            "Assert: [barman.barman] No <puser_title> parameter specified!"
        assert pmessage_text is not None, \
            "Assert: [barman.barman] No <pmessage_text> parameter specified!"
        command: int
        message: str = ""
        word_list: list = func.parse_input(pmessage_text)

        if self.can_process(pchat_title, pmessage_text):

            # *** Возможно, запросили меню.
            if word_list[0] in BAR_HINT:

                message = "Сегодня в баре имеется следующий ассортимент: \n" + \
                          self.get_help(pchat_title)
            elif word_list[0] in BAR_RELOAD:

                self.reload()
                message = "Содержимое бара обновлено"
            else:

                # *** Нет, видимо, напиток.
                command = self.get_command(word_list[0])
                name_to = puser_title
                if len(word_list) > 1:

                    name_to = word_list[1]
                # *** В зависимости от команды выполняем действия
                message = self.execute_command(command, name_to)
        if len(message) > 0:

            print(f"Barman answers: {message[:16]}")
        return message

    def bring_beer(self, puser_name: str) -> str:
        """Пользователь запросил пиво."""
        assert puser_name is not None, \
            "Assert: [barman.bring_beer] No <puser_name> parameter specified!"
        if (BEER_CANS_KEY in self.beer and
                BEER_MARKS_KEY in self.beer and
                DRINKS_SOURCES_KEY in self.drinks and
                DRINKS_TRANSFER_KEY in self.drinks):

            can: str = random.choice(self.beer[BEER_CANS_KEY])
            beer: str = random.choice(self.beer[BEER_MARKS_KEY])
            source: str = random.choice(self.drinks[DRINKS_SOURCES_KEY])
            transfer: str = random.choice(self.drinks[DRINKS_TRANSFER_KEY])
            return f"Softice {source} {can} пива \"{beer}\" {transfer} {puser_name} {BEER_EMODJI}"
        return "А нету пива! :("

    def bring_cocktail(self, puser_name: str) -> str:
        """Пользователь запросил коктейль."""
        assert puser_name is not None, \
            "Assert: [barman.bring_cocktail] No <puser_name> parameter specified!"

        if (DRINKS_SOURCES_KEY in self.drinks and
                self.cocktail is not None and
                VODKA_FILLS_KEY in self.vodka):

            source: str = random.choice(self.drinks[DRINKS_SOURCES_KEY])
            cocktail: str = random.choice(self.cocktail)
            transfer: str = random.choice(self.vodka[VODKA_FILLS_KEY])
            return f"Softice {source} {cocktail} и {transfer} {puser_name} {COCKTAIL_EMODJI}"
        return "Кончились коктейли! =("

    def bring_coffee(self, puser_name: str) -> str:
        """Пользователь запросил кофе."""
        assert puser_name is not None, \
            "Assert: [barman.bring_coffee] No <puser_name> parameter specified!"
        if (COFFEE_FILLS_KEY in self.coffee and
                COFFEE_MARKS_KEY in self.coffee and
                DRINKS_TRANSFER_KEY in self.drinks):

            fill: str = random.choice(self.coffee[COFFEE_FILLS_KEY])
            coffee: str = random.choice(self.coffee[COFFEE_MARKS_KEY])
            transfer: str = random.choice(self.drinks[DRINKS_TRANSFER_KEY])
            return f"Softice {fill} кофе \"{coffee}\" {transfer} {puser_name} {COFFEE_EMODJI}"
        return "Кофе весь вышел. :-\\"

    def bring_cognac(self, puser_name: str) -> str:
        """Пользователь запросил коньяк."""
        assert puser_name is not None, \
            "Assert: [barman.bring_cognac] No <puser_name> parameter specified!"
        if (DRINKS_SOURCES_KEY in self.drinks and
                COGNAC_CANS_KEY in self.cognac and
                COGNAC_MARKS_KEY in self.cognac and
                COGNAC_FILLS_KEY in self.cognac):

            source: str = random.choice(self.drinks[DRINKS_SOURCES_KEY])
            can: str = random.choice(self.cognac[COGNAC_CANS_KEY])
            cognac: str = random.choice(self.cognac[COGNAC_MARKS_KEY])
            transfer: str = random.choice(self.cognac[COGNAC_FILLS_KEY])
            return f"Softice {source} {can} {cognac} и {transfer} {puser_name} {COGNAC_EMODJI}"
        return "Выпили весь коньяк. 8("

    def bring_cookies(self, puser_name: str) -> str:
        """Пользователь запросил печеньки."""
        assert puser_name is not None, \
            "Assert: [barman.bring_cookies] No <puser_name> parameter specified!"
        if (COOKIES_SOURCES_KEY in self.cookies and
                COOKIES_MARKS_KEY in self.cookies and
                COOKIES_TRANSFER_KEY in self.cookies):

            source: str = random.choice(self.cookies[COOKIES_SOURCES_KEY])
            # can: str = "пачку"
            cookies: str = random.choice(self.cookies[COOKIES_MARKS_KEY])
            transfer: str = random.choice(self.cookies[COOKIES_TRANSFER_KEY])
            # print(cookies, COOKIES_MARKS_KEY, self.cookies[COOKIES_MARKS_KEY])
            return (f"Softice {source} печенье \"{cookies}\" {transfer} "
                    f"{puser_name} {COOKIE_EMODJI}")
        return "Нету печенья. Мыши съели. B("

    def bring_tea(self, puser_name: str) -> str:
        """Пользователь запросил чай."""
        assert puser_name is not None, \
            "Assert: [barman.bring_tea] No <puser_name> parameter specified!"
        if (TEA_FILLS_KEY in self.tea and
                TEA_MARKS_KEY in self.tea and
                DRINKS_TRANSFER_KEY in self.drinks):

            fill: str = random.choice(self.tea[TEA_FILLS_KEY])
            tea: str = random.choice(self.tea[TEA_MARKS_KEY])
            transfer: str = random.choice(self.drinks[DRINKS_TRANSFER_KEY])
            return f"Softice {fill} {tea} {transfer} {puser_name}"
        return "Чаю нет. 8()"

    def bring_vodka(self, puser_name: str) -> str:
        """Пользователь запросил пиво."""
        assert puser_name is not None, \
            "Assert: [barman.bring_vodka] No <puser_name> parameter specified!"
        if (DRINKS_SOURCES_KEY in self.drinks and
                VODKA_CANS_KEY in self.vodka and
                VODKA_MARKS_KEY in self.vodka and
                VODKA_FILLS_KEY in self.vodka):

            source: str = random.choice(self.drinks[DRINKS_SOURCES_KEY])
            can: str = random.choice(self.vodka[VODKA_CANS_KEY])
            vodka: str = random.choice(self.vodka[VODKA_MARKS_KEY])
            transfer: str = random.choice(self.vodka[VODKA_FILLS_KEY])
            return f"Softice {source} {can} {vodka} и {transfer} {puser_name}"
        return "А водочка-то тютю. Кончилась вся. 8(  ]"

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
            "Assert: [barman.can_process] " \
            "No <pchat_title> parameter specified!"
        assert pmessage_text is not None, \
            "Assert: [barman.can_process] " \
            "No <pmessage_text> parameter specified!"
        found: bool = False
        if self.is_enabled(pchat_title):

            word_list: list = func.parse_input(pmessage_text)
            for command in COMMANDS:

                found = word_list[0] in command
                if found:

                    break
            if not found:

                for command in BAR_HINT:

                    found = word_list[0] in command
                    if found:

                        break
        return found

    def execute_command(self, pcommand: int, pname_to: str) -> str:
        """Возвращает текстовый эквивалент команды."""
        assert pcommand is not None, \
            "Assert: [barman.execute_process] " \
            "No <pcommand> parameter specified!"
        assert pname_to is not None, \
            "Assert: [barman.execute_process] " \
            "No <pname_to> parameter specified!"
        message: str = f"{COMMANDS[pcommand][0]}, сэр!"
        if pcommand == BEER_ID:

            message = self.bring_beer(pname_to)
        if pcommand == COCKTAIL_ID:

            message = self.bring_cocktail(pname_to)
        if pcommand == COFFEE_ID:

            message = self.bring_coffee(pname_to)
        if pcommand == COGNAC_ID:

            message = self.bring_cognac(pname_to)
        if pcommand == COOKIES_ID:

            message = self.bring_cookies(pname_to)
        if pcommand == TEA_ID:

            message = self.bring_tea(pname_to)
        if pcommand == VODKA_ID:

            message = self.bring_vodka(pname_to)
        return message

    def get_command(self, pword: str) -> int:  # noqa
        """Распознает команду и возвращает её код, в случае неудачи - None.
        >>> self.get_command("пиво")
        0
        >>> self.get_command("cognac")
        4
        >>> self.get_command("вк")
        1
        >>> self.get_command("ck")
        6
        >>> type(self.get_command("абракадабра"))
        <class 'NoneType'>
        """
        assert pword is not None, \
            "Assert: [barman.get_command] " \
            "No <pword> parameter specified!"
        result: int = 0
        for command_idx, command in enumerate(COMMANDS):

            if pword in command:

                result = command_idx
        return result

    def get_help(self, pchat_title: str) -> str:  # noqa
        """Пользователь запросил список команд."""
        if self.is_enabled(pchat_title):

            command_list: str = ""
            for command in COMMANDS:

                for kind in command:

                    command_list += kind + ", "
                command_list = command_list[:-2]
                command_list += "\n"
            return command_list

    def get_hint(self, pchat_title: str) -> str:  # [arguments-differ]
        """Возвращает список команд, поддерживаемых модулем.  """
        assert pchat_title is not None, \
            "Assert: [barman.get_hint] " \
            "No <pchat_title> parameter specified!"
        if self.is_enabled(pchat_title):

            return ", ".join(BAR_HINT)
        return ""

    def is_enabled(self, pchat_title: str) -> bool:
        """Возвращает True, если бармен разрешен на этом канале.
        >>> self.is_enabled({'barman_chats':'Ботовка'}, 'Ботовка')
        True
        >>> self.is_enabled({'barman_chats':'Хокку'}, 'Ботовка')
        False
        """
        assert pchat_title is not None, \
            "Assert: [barman.is_enabled] " \
            "No <pchat_title> parameter specified!"

        return pchat_title in self.config[ENABLED_IN_CHATS_KEY]

    def load_beer(self):
        """Загружает данные пива."""
        beer_cans: list = func.load_from_file(self.data_path + BEER_CANS_PATH)
        if beer_cans:

            print("Barmen loads ", len(beer_cans), " beer cans.")
            self.beer[BEER_CANS_KEY] = beer_cans

            beer_marks: list = func.load_from_file(self.data_path + BEER_MARKS_PATH)
            if beer_marks:

                print("Barmen loads ", len(beer_marks), " beer marks.")
                self.beer[BEER_MARKS_KEY] = beer_marks
                return True
        return False

    def load_coffee(self):
        """Загружает данные пива."""
        coffee_marks: list = func.load_from_file(self.data_path + COFFEE_MARKS_PATH)
        if coffee_marks:

            print("Barmen loads ", len(coffee_marks), " coffee marks.")
            self.coffee[COFFEE_MARKS_KEY] = coffee_marks

            coffee_fills: list = func.load_from_file(self.data_path + COFFEE_FILLS_PATH)
            if coffee_fills:

                print("Barmen loads ", len(coffee_fills), " coffee fills.")
                self.coffee[COFFEE_FILLS_KEY] = coffee_fills
                return True
        return False

    def load_cocktail(self):
        """Загружает данные коктейлей"""
        self.cocktail = func.load_from_file(self.data_path + COCKTAIL_MARKS_PATH)
        if self.cocktail:

            print("Barmen loads ", len(self.cocktail), " cocktail marks.")
            return True
        return False

    def load_cognac(self):
        """Загружает данные пива."""
        cognac_cans: list = func.load_from_file(self.data_path + COGNAC_CANS_PATH)
        if cognac_cans:

            print("Barmen loads ", len(cognac_cans), " cognac cans.")
            self.cognac[COGNAC_CANS_KEY] = cognac_cans

            cognac_marks: list = func.load_from_file(self.data_path + COGNAC_MARKS_PATH)
            if cognac_marks:

                print("Barmen loads ", len(cognac_marks), " cognac marks.")
                self.cognac[COGNAC_MARKS_KEY] = cognac_marks

                cognac_fills: list = func.load_from_file(self.data_path + COGNAC_FILLS_PATH)
                if cognac_fills:

                    print("Barmen loads ", len(cognac_fills), " cognac fills.")
                    self.cognac[COGNAC_FILLS_KEY] = cognac_fills
                    return True
        return False

    def load_cookies(self):
        """Загружает данные пива."""
        cookies_sources: list = func.load_from_file(self.data_path + COOKIES_SOURCES_PATH)
        if cookies_sources:

            print("Barmen loads ", len(cookies_sources), " cookies sources.")
            self.cookies[COOKIES_SOURCES_KEY] = cookies_sources

            cookies_marks: list = func.load_from_file(self.data_path + COOKIES_MARKS_PATH)
            if cookies_marks:

                print("Barmen loads ", len(cookies_marks), " cookies marks.")
                self.cookies[COOKIES_MARKS_KEY] = cookies_marks

                cookies_transfer: list = func.load_from_file(self.data_path + COOKIES_TRANSFER_PATH)
                if cookies_transfer:

                    print("Barmen loads ", len(cookies_transfer), " cookies transfer.")
                    self.cookies[COOKIES_TRANSFER_KEY] = cookies_transfer
                    return True
        return False

    def load_drinks(self):
        """Загружает данные пива."""
        drinks_sources: list = func.load_from_file(self.data_path + DRINKS_SOURCES_PATH)
        if drinks_sources:

            print("Barmen loads ", len(drinks_sources), " drinks sources.")
            self.drinks[DRINKS_SOURCES_KEY] = drinks_sources

            drinks_transfer: list = func.load_from_file(self.data_path + DRINKS_TRANSFER_PATH)
            if drinks_transfer:

                print("Barmen loads ", len(drinks_transfer), " drinks transfer.")
                self.drinks[DRINKS_TRANSFER_KEY] = drinks_transfer
                return True
        return False

    def load_tea(self):
        """Загружает данные пива."""
        tea_marks: list = func.load_from_file(self.data_path + TEA_MARKS_PATH)
        if tea_marks:

            print("Barmen loads ", len(tea_marks), " tea marks.")
            self.tea[TEA_MARKS_KEY] = tea_marks

            tea_fills: list = func.load_from_file(self.data_path + TEA_FILLS_PATH)
            if tea_fills:

                print("Barmen loads ", len(tea_fills), " tea fills.")
                self.tea[TEA_FILLS_KEY] = tea_fills
                return True
        return False

    def load_vodka(self):
        """Загружает данные пива."""
        vodka_cans: list = func.load_from_file(self.data_path + VODKA_CANS_PATH)
        if vodka_cans:

            print("Barmen loads ", len(vodka_cans), " vodka cans.")
            self.vodka[VODKA_CANS_KEY] = vodka_cans

            vodka_marks: list = func.load_from_file(self.data_path + VODKA_MARKS_PATH)
            if vodka_marks:

                print("Barmen loads ", len(vodka_marks), " vodka marks.")
                self.vodka[VODKA_MARKS_KEY] = vodka_marks

                vodka_fills: list = func.load_from_file(self.data_path + VODKA_FILLS_PATH)
                if vodka_fills:

                    print("Barmen loads ", len(vodka_fills), " vodka fills.")
                    self.vodka[VODKA_FILLS_KEY] = vodka_fills
                    return True
        return False

    def reload(self):
        """Перегружает все содержимое бара."""
        if (self.load_beer() and
                self.load_coffee() and
                self.load_cocktail() and
                self.load_cognac()):

            if (self.load_cookies() and
                    self.load_drinks() and
                    self.load_tea() and
                    self.load_vodka()):

                print("Barman successfully reload bar assortiment.")
