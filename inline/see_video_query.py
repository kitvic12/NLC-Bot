from api import bot
from telebot import types

import pytz
from datetime import datetime

import log

from database import user

from camera.weather import locations, check_cloudiness
from camera.get_image import get_camera_image, send_image_to_telegram

from commands.menu import menu

places = ["ЦФО", "Северо-Запад(СЗФО)", "Юг России", "Поволжье", "Урал", "Сибирь", "Дальний Восток"]

place = [
    "Калуга", "Москва", "Попово", "Рязань", "Тула", "Уткино", "Ярославль", "Васкелово",
    "Гулькевичи", "Краснодар", "Тырнауз", "Вологда", "Калининград", "Русское", 
    "Азево", "Альметьевск", "Березники", "Ирбит", "Каменск-Уральский", "Пермь",
    "Остроленский", "Челябинск", "Айхал", "Багдарин", "Стрежевой", "Юрга", "Пятиречье", "Провидения"
    ]

place_dict = {
    "ЦФО":["Калуга", "Москва", "Попово", "Рязань", "Тула", "Уткино", "Ярославль"],
    "Северо-Запад(СЗФО)":["Васкелово", "Вологда", "Калининград", "Русское"],
    "Юг":["Гулькевичи", "Краснодар", "Тырнауз"],
    "Поволжье":["Азево", "Альметьевск", "Березники", "Ирбит", "Каменск-Уральский", "Пермь"],
    "Урал":["Остроленский", "Челябинск"],
    "Сибирь":["Айхал", "Багдарин", "Стрежевой", "Юрга"],
    "Дальний":["Пятиречье", "Провидения"]
}



MOSCOW_TZ = pytz.timezone('Europe/Moscow')

def moscow_time():
    now = datetime.now(MOSCOW_TZ)
    return now.strftime("%Y-%m-%d %H:%M:%S")

def see_what(call, query):
    bot.delete_message(call.message.chat.id, call.message.id)
    bot.send_message(call.message.chat.id, f"Вы хотите посмотреть исключительно камеры в тех местах, где нет облачности или во всех местах?", reply_markup=types.InlineKeyboardMarkup(
        [[types.InlineKeyboardButton("Все камеры", callback_data="see all"),
          types.InlineKeyboardButton("Камеры без облачности", callback_data="see dont")]]
    ))

def all_camera(call):
    global places
    bot.delete_message(call.message.chat.id, call.message.message_id)
    markup = types.InlineKeyboardMarkup(row_width=1)

    for i in range(len(places)):
        button = types.InlineKeyboardButton(text=places[i], callback_data=f"see_place {places[i]}")
        markup.add(button)
    bot.send_message(call.message.chat.id, "В каком примерном месте вы хотите посмотреть изображение с камеры?", reply_markup=markup)

def place_camera(call, query):
    bot.delete_message(call.message.chat.id, call.message.id)
    markup = types.InlineKeyboardMarkup(row_width=1)
    for i in range(len(place_dict[query[0]])):
        print(place_dict[query[0]][i])
        button = types.InlineKeyboardButton(text=place_dict[query[0]][i], callback_data=f"seen {place_dict[query[0]][i]}")
        markup.add(button)
    markup.add(types.InlineKeyboardButton(text="🔙Назад", callback_data="see all"))
    user.save_user_markup(call.message.chat.id, markup)
    bot.send_message(call.message.chat.id, "Какую камеру вы хотите посмотреть?", reply_markup=markup)        

def dont_camera(call):

    bot.delete_message(call.message.chat.id, call.message.message_id)
    markup = types.InlineKeyboardMarkup(row_width=1)
    has_cameras = False

    log.check("----------------", "WEATHER")
    time = moscow_time()
    log.check(f"Start check at {time}", "WEATHER")
    for location, coords in locations.items():
        lat, lon = coords["lat"], coords["lon"]
        result = check_cloudiness(lat, lon, location)
        if result:
            button = types.InlineKeyboardButton(text=location, callback_data=f"seen {location}")
            markup.add(button)
            has_cameras = True
    log.check("----------------", "WEATHER")
    if has_cameras:
        user.save_user_markup(call.message.chat.id, markup)
        bot.send_message(call.message.chat.id, f"Выберите камеру:", reply_markup=markup)
    else:
        bot.send_message(call.message.chat.id, "Нет доступных камер без облачности.")

def what_camera(call, query):
    if query[0] == "all":
        all_camera(call)
    elif query[0] == "dont":
        dont_camera(call)

def camera(call, query):
    last = call.message
    bot.delete_message(call.message.chat.id, call.message.id)
    image_bytes = get_camera_image(query[0])
    if image_bytes:
        send_image_to_telegram(image_bytes, call.message.chat.id)
        bot.send_message(call.message.chat.id, f"Изображение с камеры {query[0]}", reply_markup=types.InlineKeyboardMarkup(
            [[types.InlineKeyboardButton("Вернуться в меню", callback_data="menu"),
             types.InlineKeyboardButton("Вернуться к выбору камер", callback_data=f"return_camera")]]
        ))
    else:
        print("Не удалось получить изображение с сайта")

def return_menu(call, query):
    try:
        if query[0] == "no":
            menu(call.message)
            return
        elif query[0] == "yes":
            if query[1] == "callback":
                user.update_state(call.message.chat.id, "callback", False)
            bot.delete_message(call.message.chat.id, call.message.id)
            menu(call.message) 
            return   

    except:
        user.clear_user_markup(call.message.chat.id)
        bot.delete_message(call.message.chat.id, call.message.id)
        menu(call.message)


def return_camera(call, query):
    if not user.get_user_markup(call.message.chat.id):
        all_camera(call)
        return
    bot.delete_message(call.message.chat.id, call.message.id)
    markup = user.get_user_markup(call.message.chat.id)
    bot.send_message(call.message.chat.id, "Выберите камеру:", reply_markup=markup)