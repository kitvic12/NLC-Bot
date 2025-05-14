from api import bot
from database import user
from log import log
from database import user
from telebot import types
from always_check import main_handler
from always_check import moscow_time

def place(message, _):
    if user.get_state(message.chat.id, "see nlc"):
        bot.send_message(message.chat.id, "Спасибо за информацию, мы воспользуемся ею и оповестим остальных пользователей!", reply_markup=types.InlineKeyboardMarkup(
            [[types.InlineKeyboardButton("В меню", callback_data="menu")]]
        ))
        user.update_state(message.chat.id, "see nlc", False)
        id = message.chat.id
        for users in user.get_all_users():
            if users['user_id'] != id:
                if users['notification'] == "on":
                    bot.send_message(users['user_id'], f"Есть сообщения о видимости серебристых облаков в {message.text}! Удачных вам наблюдений!")
        log("----------------", "CHECK")
        log(f"Start check at {moscow_time()}", "CHECK")
        main_handler()
        log("----------------", "CHECK")
        return True