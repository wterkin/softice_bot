# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Модуль игры Мафия."""

from telebot import types
import functions as func
import random

# Дон
DON_ROLE: int = 0
#DON_ROLE_TEXT: str = "Дон"
# Мафия 1-N
MAFIOZO_ROLE: int = 1
#MAFIOZO_ROLE_TEXT: str = "Мафиози"
# Маньяк
MANIAC_ROLE = 2
#MANIAC_ROLE_TEXT:str = "Маньяк"
# Катани
CATANI_ROLE: int = 3
#CATANI_ROLE_TEXT: str = "Комиссар Катани"
# Бомж
BOMZH_ROLE: int = 4
#BOMZH_ROLE_TEXT: str = "Бомж"
# Док
DOCTOR_ROLE: int = 5
#DOCTOR_ROLE_TEXT: str = "Доктор"
# Счастливчик
LUCKYMAN_ROLE: int = 6
#LUCKYMAN_ROLE_TEXT: str = "Счастливчик"
# Мир 1-N
PEACEFUL_ROLE: int = 7
#PEACEFUL_ROLE_TEXT: str = "Мирный житель"
#

ROLES_DESCRIPTIONS: list = [[0, "Дон"],
                            [1, "Мафиози"],
                            [2, "Маньяк"],
                            [3, "Катани"],
                            [4, "Бомж"],
                            [5, "Доктор"],
                            [6, "Счастливчик"],
                            [7, "Мирный житель"]
                           ]
#Дон,Маф,Ман,Кат,Бомж,Док,Счст,Мир
ROLES: list = [[],
               [1,0,0,0,0,0,0,0], ###
               [1,0,0,0,0,0,0,1], ###
               [1,0,0,0,0,1,0,1], #  3
               [1,0,0,0,0,1,0,2], #  4
               [1,0,0,1,0,1,0,2], #  5
               [1,0,0,1,1,1,0,2], #  6
               [1,0,0,1,1,1,1,2], #  7
               [1,1,0,1,1,1,1,2], #  8
               [1,1,1,1,1,1,1,2], #  9
               [1,2,1,1,1,1,1,2], # 10
               [1,2,1,1,1,1,1,3], # 11
               [1,2,1,1,2,1,1,3], # 12
               [1,2,2,1,2,1,1,3], # 13
               [1,2,2,1,2,1,2,3], # 14
               [1,2,2,1,2,1,2,4]  # 15
              ]

COMMAND_START = 0
COMMAND_REGISTER = 1
COMMAND_STOP = 2
COMMAND_PLAY = 3

MAFIA_COMMANDS: list = ["go", "mreg", "mstop", "mplay"]

CHANNEL_LIST_KEY = "mafiozo_chats"

GAME_OFF = 0
GAME_REGISTERING = 1
GAME_ON = 2

game_stage: int = GAME_OFF
users: list = []
chat_id: int = None



class CUser():

    def __init__(self, pid, pname):

        # self.channel_id = pchannel_id
        self.id: int = pid
        self.name: str = pname
        self.role: int = None
        self.alive: bool = True


    def __repr__(self):

        if self.alive:

            return f"User {self.name} id {self.id} with role {self.role} is alive"
        else:

            return f"User {self.name} id {self.id} with role {self.role} is dead"

    def give_role(self, prole):
        """Назначение роли."""
        self.role = prole

    def kill(self):
        """Лишение жизни."""

        self.alive = False


def can_process(pconfig: dict, pchat_title: str, pmessage_text: str) -> bool:
    """Возвращает True, если мафиози может обработать эту команду
    >>> can_process({'barman_chats':'Ботовка'}, 'Ботовка', '!vodka')
    True
    >>> can_process({'barman_chats':'Хокку'}, 'Ботовка', '!vodka')
    False
    >>> can_process({'barman_chats':'Ботовка'}, 'Ботовка', '!мартини')
    False
    """

    if is_enabled(pconfig, pchat_title):

        word_list: list = func.parse_input(pmessage_text)
        return word_list[0] in MAFIA_COMMANDS
    return False


def give_roles():
    """Процедура раздачи ролей."""
    temp_users = []
    temp_users.extend(users)
    roles = ROLES[len(users)] #  [1,2,1,1,1,1,1,2]
    for role_idx in range(len(roles)):

        print("** MFZ:gvrl:role:", role_idx, roles[role_idx])
        if roles[role_idx] > 0:

            for role_count in range(0, roles[role_idx]):

                print("** MFZ:gvrl:role:", role_count)
                random_number = random.randint(0, len(users)-1)
                random_user = temp_users[random_number]
                temp_users.remove(random_user)
                random_user.give_role(role_idx)
                print("** MFZ:gvrl:user:", random_user)
    for user in users:

        print("** MFZ:gvrl:users:", user)



def is_enabled(pconfig: dict, pchat_title: str) -> bool:
    """Возвращает True, если мафия разрешена на этом канале.
    >>> is_enabled({'barman_chats':'Ботовка'}, 'Ботовка')
    True
    >>> is_enabled({'barman_chats':'Хокку'}, 'Ботовка')
    False
    """
    return pchat_title in pconfig[CHANNEL_LIST_KEY]


#def process_callback(pmessage_text: str, puser_id: int, puser_name: str):
    #"""Процедура, обрабатывающая нажатия кнопок."""

    #word_list: list = func.parse_input(pmessage_text)
    #*** Регистрация в игру
    #if

# TODO: Сделать проверку по username, а не по title
# def mafiozo(pfrom_user_name: str, pmessage_text: str):
def mafiozo(pconfig: dict, pmessage_text: str, pchat_id: int,
            pfrom_user_id: int, pfrom_user_name: str) -> str:
    """Основная процедура модуля."""

    command: int = None
    message: str = None
    word_list: list = func.parse_input(pmessage_text)
    command = MAFIA_COMMANDS.index(word_list[0])
    markup: object = types.InlineKeyboardMarkup()
    # print("***********", pfrom_user_name)
    global users
    global game_stage
    global chat_id
    if command == COMMAND_START:

        #return start_game(pfrom_user_name)
        if game_stage == GAME_OFF:

            register_button: object = types.InlineKeyboardButton("Играть", callback_data="!mreg")
            markup.add(register_button)
            chat_id = pchat_id
            game_stage = GAME_REGISTERING
            return "Начинается регистрация в игру Мафия!", pchat_id, markup
        else:

            return "Игра уже идёт!", pchat_id, None

    elif command == COMMAND_REGISTER:

        if game_stage == GAME_REGISTERING:

            if pchat_id == chat_id:

                already_registered: bool = False
                for user in users:

                    if user.id == pfrom_user_id:
                        already_registered = True
                        break
                if already_registered:

                    return f"{pfrom_user_name}, ты уже в игре!", pfrom_user_id, None
                else:
                    user = CUser(pfrom_user_id, pfrom_user_name)
                    users.append(user)
                    return f"{pfrom_user_name}, ты играешь!", pfrom_user_id, None
            else:

                return "Игра уже начата на другом канале!", pchat_id, None
        else:

            return "Запустите игру для регистрации!", pchat_id, None
    elif command == COMMAND_PLAY:

        if game_stage == GAME_ON:

            return "Игра уже идёт!", pchat_id, None
        if game_stage ==  GAME_OFF:

            return "Запустите игру для регистрации!", pchat_id, None
        game_stage = GAME_ON
        give_roles()
        return "Игра начинается!", pchat_id, None

    elif command == COMMAND_STOP:

        if game_stage != GAME_OFF:

            if pfrom_user_name == pconfig["master_name"]:

                game_stage = GAME_OFF
                users = []
                return "Игра остановлена.", pchat_id, None
            return "У вас нет прав для остановки игры.", pfrom_user_id, None
        return "Игра не была запущена.", pfrom_user_id, None
