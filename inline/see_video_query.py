from api import bot
from telebot import types

import pytz
from datetime import datetime

import log

import userstate

from camera.weather import locations, check_cloudiness
from camera.get_image import get_camera_image, send_image_to_telegram

from commands.menu import menu

place = ["Азеево", "Айхал", "Альметьевск", "Багдарин", "Березники", "Васкелово", "Вологда", "Гулькевичи", "Ирбит", "Калининград", "Калуга", "Каменск-Уральский", "Краснодар", "Москва", "Остроленский", "Пермь", "Попово", "Провидения", "Пятиречье", "Русское", "Рязань", "Стрежевой", "Тула", "Уткино", "Челябинск", "Юрга", "Ярославль", "Тырнауз"]

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
    global place
    bot.delete_message(call.message.chat.id, call.message.message_id)
    markup = types.InlineKeyboardMarkup(row_width=1)

    if not place:
        bot.send_message(call.message.chat.id, "Нет доступных камер.")
        return

    for i in range(len(place)):
        button = types.InlineKeyboardButton(text=place[i], callback_data=f"seen {place[i]}")
        markup.add(button)
    userstate.update_state(call.message.chat.id, "last markup", markup)
    bot.send_message(call.message.chat.id, "Какую камеру вы хотите посмотреть?", reply_markup=markup)

def dont_camera(call):
    global place
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
        userstate.update_state(call.message.chat.id, "last markup", markup)
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
                userstate.update_state(call.message.chat.id, "callback", False)
            bot.delete_message(call.message.chat.id, call.message.id)
            menu(call.message) 
            return   

    except:
        bot.delete_message(call.message.chat.id, call.message.id)
        menu(call.message)


def return_camera(call, query):
    bot.delete_message(call.message.chat.id, call.message.id)
    markup = userstate.get_state(call.message.chat.id, "last markup")
    bot.send_message(call.message.chat.id, "Выберите камеру:", reply_markup=markup)