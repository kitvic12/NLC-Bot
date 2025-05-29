from api import bot
from database import user
from log import log
from database import user
from telebot import types
from always_check import main_handler
from always_check import moscow_time

def send_all(message):
    if not message.photo and not user.get_state(message.chat.id, 'nlc place'):
        id = message.chat.id
        for users in user.get_all_users():
            if users['user_id'] != id:
                if users['notification'] == "on":
                    bot.send_message(users['user_id'], f"Есть сообщения о видимости серебристых облаков в {message.text}! Удачных вам наблюдений!")
        log("----------------", "CHECK")
        log(f"Start check at {moscow_time()}", "CHECK")
        main_handler()
        log("----------------", "CHECK")
        return
    
    if message.photo:
        id = message.chat.id
        for users in user.get_all_users():
            if users['user_id'] != id:
                if users['notification'] == "on":
                    bot.send_photo(users['user_id'], message.photo, f"Есть сообщения о видимости серебристых облаков в {message.text}! Удачных вам наблюдений!")
        log("----------------", "CHECK")
        log(f"Start check at {moscow_time()}", "CHECK")
        main_handler()
        log("----------------", "CHECK")
        return

    if user.get_state(message.chat.id, "nlc place"):
        photo = user.get_state(message.chat.id, "nlc photo")
        for users in user.get_all_users():
            if users['user_id'] != id:
                if users['notification'] == "on":
                    bot.send_photo(users['user_id'], photo, f"Есть сообщения о видимости серебристых облаков в {message.text}! Удачных вам наблюдений!")
        log("----------------", "CHECK")
        log(f"Start check at {moscow_time()}", "CHECK")
        main_handler()
        log("----------------", "CHECK")
        return


def place(message, _):
    if user.get_state(message.chat.id, "see nlc"):
        bot.send_message(message.chat.id, "Спасибо за информацию, мы воспользуемся ею и оповестим остальных пользователей!", reply_markup=types.InlineKeyboardMarkup(
            [[types.InlineKeyboardButton("В меню", callback_data="menu")]]
        ))
        user.update_state(message.chat.id, "see nlc", False)
        return True
    

def place_photo(message, _):
    if user.get_state(message.chat.id, "see nlc"):
        if not message.text:
            bot.send_message(message.chat.id, "Пожалуйста, укажите место, где вы видите СО, просто отдельным сообщением с текстом!")
            user.update_state(message.chat.id, "need place", True)
            user.update_state(message.chat.id, "nlc photo", message.photo)
            return
        else: 
            bot.send_message(message.chat.id, "Спасибо за информацию! Мы оповестим ей других пользователей.")
            send_all(message)