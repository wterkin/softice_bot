# process_callback(pmessage_text: str, puser_id: int, puser_name: str):
# Если сообщение из чата с ботом
# 'from_user': {'id': 1978360349, 'is_bot': True, 'first_name': 'SoftIce', 'username': 'SoftIceBot', 'last_name': None, 'language_code': None, 'can_join_groups': None, 'can_read_all_group_messages': None, 'supports_inline_queries': None}
# 'chat': {'id': -583831606, 'type': 'group', 'title': 'Ботовка', 'username': None, 'first_name': None, 'last_name': None, 'photo': None, 'bio': None, 'description': None, 'invite_link': None, 'pinned_message': None, 'permissions': None, 'slow_mode_delay': None, 'message_auto_delete_time': None, 'sticker_set_name': None, 'can_set_sticker_set': None, 'linked_chat_id': None, 'location': None},

# print(call.message)
# print(call.message.chat.id)
# print(call.message.message_id)
# print(call.inline_message_id)
# print(call.from_user.username)
# print(call.from_user.id)
# if call.message:

# if call.data == "test":

# SoftIceBot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Пыщь")
# Если сообщение из инлайн-режима
# if call.inline_message_id:
# call.message.chat.id
# call.message.message_id
# call.inline_message_id
# if call.data == "test":

# SoftIceBot.edit_message_text(inline_message_id=call.inline_message_id, text="Бдыщь")
june-johnny-caspian-19
01d	01n	Чистое небо
02d	02n	Малооблачно
03d	03n	Рваная облачность
04d	04n	Облачно с прояснениями
09d	09n	Ливневый дождь
10d	10n	Дождь
11d	11n	Гроза
13d	13n	Снег
50d	50n	Туман
    # def call_mafiozo(self, pchat_id: int, pchat_title: str,
    #                  puser_id: int, puser_title: str, pmessage_text: str):
    #     """По возможности обработать команду мафиози"""
    #     assert pchat_id is not None, \
    #         "Assert: [softice.call_mafiozo] " \
    #         "No <pchat_id> parameter specified!"
    #     assert pchat_title is not None, \
    #         "Assert: [softice.call_mafiozo] " \
    #         "No <pchat_title> parameter specified!"
    #     assert puser_id is not None, \
    #         "Assert: [softice.call_mafiozo] No <puser_id> parameter specified!"
    #     assert puser_title is not None, \
    #         "Assert: [softice.call_mafiozo] No <puser_title> parameter specified!"
    #     assert pmessage_text is not None, \
    #         "Assert: [softice.call_mafiozo] " \
    #         "No <pmessage_text> parameter specified!"
    #
    #     if mafiozo.can_process(self.config, pchat_title, pmessage_text):
    #
    #         message: str
    #         markup: object
    #         addressant: int
    #         # *** как пить дать.
    #         message, addressant, markup = mafiozo.mafiozo(self.config, pmessage_text, pchat_id,
    #                                                       puser_id, puser_title)
    #         if message:
    #
    #             print("Mafiozo answers.", addressant)
    #             if markup is None:
    #
    #                 self.robot.send_message(addressant, message)
    #             else:
    #
    #                 self.robot.send_message(addressant, message, reply_markup=markup)
    #             return True
    #     return False

    # def call_meteorolog(self, pchat_id: int, pchat_title: str,
    #                     pmessage_text: str):
    #     """По возможности обработать команду метеорологом"""
    #     assert pchat_id is not None, \
    #         "Assert: [softice.call_meteorolog] " \
    #         "No <pchat_id> parameter specified!"
    #     assert pchat_title is not None, \
    #         "Assert: [softice.call_meteorolog] " \
    #         "No <pchat_title> parameter specified!"
    #     assert pmessage_text is not None, \
    #         "Assert: [softice.call_meteorolog] " \
    #         "No <pmessage_text> parameter specified!"
    #     if meteorolog.can_process(self.config, pchat_title, pmessage_text):
    #
    #         # *** как пить дать.
    #         message = meteorolog.meteorolog(pmessage_text)
    #         if message is not None:
    #             print(" Meteorolog answers.")
    #             self.robot.send_message(pchat_id, message)
    #             return True
    #     return False
