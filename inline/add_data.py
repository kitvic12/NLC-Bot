from api import bot
from main import change
from database import user
from telebot import types
import log



def get_us(message):
    return user.get_state(message.chat.id, "data"), user.get_state(message.chat.id, "count send")

def get_brightness(call, query):
    data, count = get_us(call.message)    
    data[count] += f",{query[0]}"
    user.update_state(call.message.chat.id, "data", data)

    change(call.message, "Хорошо, а теперь выберите погодные условия, о их шкале также можно узнать в комагде /about -> 'Календарь наблюдателя' -> 'Погодные условия'", reply_markup=types.InlineKeyboardMarkup([
        [types.InlineKeyboardButton("А", callback_data="weather А")],
        [types.InlineKeyboardButton("Б", callback_data="weather Б")],
        [types.InlineKeyboardButton("В", callback_data="weather В")],
        [types.InlineKeyboardButton("Г", callback_data="weather Г")],
        [types.InlineKeyboardButton("Д", callback_data="weather Д")]
    ]))

def get_weather(call, query):
    data, count = get_us(call.message)
    data[count] += f",{query[0]}"
    user.update_state(call.message.chat.id, "data", data)

    change(call.message, "Хорошо, а теперь выберите интенсивность СО, о их шкале также можно узнать в команде /about -> 'Дневник наблюдателя' -> 'Интенсивность СО'.", reply_markup=types.InlineKeyboardMarkup([
        [types.InlineKeyboardButton("1", callback_data="intensity 1")],
        [types.InlineKeyboardButton("2", callback_data="intensity 2")],
        [types.InlineKeyboardButton("3", callback_data="intensity 3")],
        [types.InlineKeyboardButton("4", callback_data="intensity 4")],
        [types.InlineKeyboardButton("5", callback_data="intensity 5")],
        [types.InlineKeyboardButton("6", callback_data="intensity 6")],
        [types.InlineKeyboardButton("7", callback_data="intensity 7")],
        [types.InlineKeyboardButton("8", callback_data="intensity 8")],
        [types.InlineKeyboardButton("9", callback_data="intensity 9")],
        [types.InlineKeyboardButton("10", callback_data="intensity 10")],
    ]))



def get_intensity(call, query):
    data, count = get_us(call.message)
    data[count] += f",{query[0]}"
    user.update_state(call.message.chat.id, "data", data)

    change(call.message, "Прекрасно, еще одна часть ваших наблюдений записана! Если это не последняя запись в вашем дневнике - напишите следующее время и все начнеться по новой, а если это последняя - нажмите кнопку 'Готово'.", reply_markup=types.InlineKeyboardMarkup([
        [types.InlineKeyboardButton("Готово", callback_data="give cancel")]
    ]))

    user.update_state(call.message.chat.id, "wait for time", True)