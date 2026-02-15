from core.api import bot
from telebot import types

from core.main import change

import pytz
from datetime import datetime

import core.log as log

from core.database import user

from .weather import locations, check_cloudiness
from .get_image import get_camera_image, send_image_to_telegram

from .menu import menu

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

    change(call.message, f"Вы хотите посмотреть исключительно камеры в тех местах, где нет облачности или во всех местах?", reply_markup=types.InlineKeyboardMarkup(
        [[types.InlineKeyboardButton("Все камеры", callback_data="see all"),
          types.InlineKeyboardButton("Камеры без облачности", callback_data="see dont")]]
    ))

def all_camera(call):
    global places
    markup = types.InlineKeyboardMarkup(row_width=1)

    for i in range(len(places)):
        button = types.InlineKeyboardButton(text=places[i], callback_data=f"see_place {places[i]}")
        markup.add(button)
    markup.add(types.InlineKeyboardButton("🔙Назад", callback_data="see_video"))
    change(call.message, "В каком примерном месте вы хотите посмотреть изображение с камеры?", reply_markup=markup)

def place_camera(call, query):
    markup = types.InlineKeyboardMarkup(row_width=1)
    for i in range(len(place_dict[query[0]])):
        print(place_dict[query[0]][i])
        button = types.InlineKeyboardButton(text=place_dict[query[0]][i], callback_data=f"seen {place_dict[query[0]][i]}")
        markup.add(button)
    markup.add(types.InlineKeyboardButton(text="🔙Назад", callback_data="see all"))
    user.save_user_markup(call.message.chat.id, markup)
    change(call.message, "Какую камеру вы хотите посмотреть?", reply_markup=markup)        

def dont_camera(call):

    change(call.message, "Проверка облачности, ожидайте...")
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
    markup.add(types.InlineKeyboardButton("🔙Назад", callback_data="see_video"))
    if has_cameras:
        user.save_user_markup(call.message.chat.id, markup)
        change(call.message, f"Выберите камеру:", reply_markup=markup)
    else:
        change(call.message, "Нет доступных камер без облачности.", reply_markup=markup)

def what_camera(call, query):
    if query[0] == "all":
        all_camera(call)
    elif query[0] == "dont":
        dont_camera(call)

def camera(call, query):
    change(call.message, "Загрузка данных, ожидайте...")
    image_bytes = get_camera_image(query[0])
    if image_bytes:
        bot.delete_message(call.message.chat.id, call.message.id)
        send_image_to_telegram(image_bytes, call.message.chat.id)
        bot.send_message(call.message.chat.id, f"Изображение с камеры {query[0]}", reply_markup=types.InlineKeyboardMarkup(
            [[types.InlineKeyboardButton("Вернуться в меню", callback_data="menu"),
             types.InlineKeyboardButton("Вернуться к выбору камер", callback_data=f"return_camera")]]
        ))
    else:
        print("Не удалось получить изображение с сайта")



def return_camera(call, query):
    if not user.get_user_markup(call.message.chat.id):
        all_camera(call)
        return
    markup = user.get_user_markup(call.message.chat.id)
    change(call.message, "Выбрерите камеру:", markup)