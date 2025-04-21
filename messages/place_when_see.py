from api import bot
import userstate
from log import log
from inline.subscribe import load_data
from telebot import types
from always_check import main_handler
from always_check import moscow_time

def place(message, _):
    if userstate.get_state(message.chat.id, "see nlc"):
        bot.send_message(message.chat.id, "Спасибо за информацию, мы воспользуемся ею и оповестим остальных пользователей!", reply_markup=types.InlineKeyboardMarkup(
            [[types.InlineKeyboardButton("В меню", callback_data="menu")]]
        ))
        userstate.update_state(message.chat.id, "see nlc", False)
        id = message.chat.id
        for chat in load_data():
            if chat != id:
                bot.send_message(chat, f"Есть сообщения о видимости серебристых облаков в {message.text}! Удачных вам наблюдений!")
        log("----------------", "CHECK")
        log(f"Start check at {moscow_time()}", "CHECK")
        main_handler()
        log("----------------", "CHECK")
        return True