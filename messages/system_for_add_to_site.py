from api import bot
from database import user
from telebot import types
from main import change

from telebot import types



def get_place (message, _):
    if user.get_state(message.chat.id, "wait for place and date"):
        fn = message.from_user.first_name
        ln = message.from_user.last_name
        if fn is not None:
            if ln is not None:
                name = fn + ln
            else:
                name = fn
        else:
            name = message.from_user.username
        user.update_state(message.chat.id, "date and place", message.text)
        bot.send_message(message.chat.id, "Укажите пожалуйста время вашей записи в формате ЧЧ:ММ")
        user.update_state(message.chat.id, "wait for place and date", False)
        user.update_state(message.chat.id, "waiting for time", True)
        user.update_state(message.chat.id, "name", name)
        user.update_state(message.chat.id, "count send", 1)
        user.update_state(message.chat.id, "data", {})
        return True
    
    elif user.get_state(message.chat.id, "waiting for time"):
        data = user.get_state(message.chat.id, "data")
        count = user.get_state(message.chat.id, "count send")
        data[count] = message.text
        bot.send_message(message.chat.id, "Хорошо, теперь укажите яркость, для понимания шкалы яркости ее можно посмотреть в команде /about -> 'Дневник наблюдателя' -> 'Шкала яркости'.", reply_markup=types.InlineKeyboardMarkup([   
            [types.InlineKeyboardButton("1", callback_data="brightness 1")],
            [types.InlineKeyboardButton("2", callback_data="brightness 2")],
            [types.InlineKeyboardButton("3", callback_data="brightness 3")],
            [types.InlineKeyboardButton("4", callback_data="brightness 4")],
            [types.InlineKeyboardButton("5", callback_data="brightness 5")]
            ]))
        user.update_state(message.chat.id, "waiting for time", False)
        return True