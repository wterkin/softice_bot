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