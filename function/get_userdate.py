from core.api import bot
from core.database import user
from telebot import types
from core.main import change
from function.menu import menu

from threading import Thread
import time

from telebot import types

from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

import csv


file_real = "../../../../var/www/Kitvic/backend/data.csv"  
file_test = "./files/data.csv"



#writer to csv-table

def writer(new_row):
    with open(file_real, mode='a', newline='', encoding='utf-8') as file: 
        writer = csv.writer(file)
        writer.writerow(new_row)



#get famous city

geolocator = Nominatim(user_agent="cloud_observation_bot")

def location_handler(lat: float, lon: float) -> str:
    try:
        location = geolocator.reverse((lat, lon), exactly_one=True, timeout=10)
        
        if location:
            address = location.raw.get('address', {})
            city = (
                address.get('city') or 
                address.get('town') or 
                address.get('village') or 
                address.get('municipality') or 
                address.get('county')
            )
            return city if city else "Неизвестное местоположение"
        return "Местоположение не найдено"
    
    except (GeocoderTimedOut, GeocoderServiceError, AttributeError):
        return "Ошибка определения местоположения"




#get time

from timezonefinder import TimezoneFinder
from datetime import datetime
import pytz

tf = TimezoneFinder()

def time_handler(lat: float, lon: float) -> str:
    timezone_str = tf.timezone_at(lat=lat, lng=lon)
    if timezone_str:
        tz = pytz.timezone(timezone_str)
        local_time = datetime.now(tz)
        return local_time.strftime("%d/%m/%Y"), local_time.strftime("%H:%M")
    return "Часовой пояс не определен"



#time-out for send

def waiting(chat_id):
    for _ in range(10):
        time.sleep(1)
        if not user.get_state(chat_id, "active"):
            return
    
    bot.send_message(chat_id, "Прошло 30 минут, ожидаем новую запись в дневник, если она не появиться в течении 1 часа", reply_markup=types.InlineKeyboardMarkup(
        [[types.InlineKeyboardButton("Новая запись", callback_data="userdate new continue")],
         [types.InlineKeyboardButton("Завершить наблюдение", callback_data="give cancel_write")]]
    ))




#upload to site

def upload(message: types.Message):
    name = ""
    data = user.get_state(message.chat.id, "userdate")


    if message.chat.first_name is not None:
        name += message.chat.first_name

    if message.chat.last_name is not None:
        name += message.chat.last_name
    
    elif message.chat.first_name is None and message.chat.last_name is None:
        name += message.chat.username


    for i in range(data["count"]):
        i += 1

        for_add = list()
        for_add.append(name)
        for_add.append(data["city"])
        for_add.append(data["date"])
        for_add.append(data[i]["time"])
        for_add.append(data[i]["brightness"])
        for_add.append(data[i]["weather"])
        for_add.append(data[i]["intensity"])

        writer(for_add)




#----------------------------


#user engagement



def get_userdate(call, query):
    if query[0] == "start":
        last = bot.send_message(call.message.chat.id, "Отправьте вашу геопозицию, нажав кнопку на вашей клавиатуре. Время будет  записано автоматически, в соответсвии с вашем мостоположением", reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(types.KeyboardButton("Отправить геолокацию", request_location=True)))
        bot.send_message(call.message.chat.id, "Для отмены и возврата в меню воспользуйтесь кнопкой 'Отмена'", reply_markup=types.InlineKeyboardMarkup(
            [[types.InlineKeyboardButton("Отмена", callback_data=f"geo_cancel {last.id}")]]
        ))

        data = dict()
        data[1] = dict()
        data["count"] = 0

        user.update_state(call.message.chat.id, "userdate", data)
    
    elif query[0] == "cancel_write":
        data = user.get_state(call.message.chat.id, "userdate")
        markup = types.InlineKeyboardMarkup()

        bot.delete_message(call.message.chat.id, call.message.id)
        user.update_state(call.message.chat.id, "active", False)

        if data["count"] >= 1:
            upload(call.message)
            text = 'Спасибо за информацию! Она будет записана в <a href="http://kitvic12.github.io/nlc-site/database.html">базу данных нашего сайта</a>. Воспользуйтесь кнопкой возврата в меню, если вам это надо.'
        else:
            user.update_state(call.message.chat.id, "userdate", dict())
            text = 'К сожалению количество ваших наблюдений не позволяет построить график, для этого нужно минимум 3 записи. Если вы хотите, вы можете продолжить запись или вернуться в меню, но после возврата в меню все данные вашей записи будут удалены.'
            
            markup.add(types.InlineKeyboardButton("Продолжить запись", callback_data="userdate new continue"))
        
        markup.add(types.InlineKeyboardButton("В меню", callback_data="give menu"))
        bot.send_message(call.message.chat.id, text, reply_markup=markup, parse_mode="HTML")

    elif query[0] == "menu":
        user.update_state(call.message.chat.id, "userdate", dict())
        menu(call.message, "yes")




def get_location(message: types.Message, _):
    lat = message.location.latitude
    lon = message.location.longitude

    city = location_handler(lat, lon)
    date, time = time_handler(lat, lon)

    date = date.replace("/", ".")

    bot.send_message(message.chat.id, f"Близлежащий к вам населенный пункт - {city}, он будет записан в итогоую таблицу, ваше текущее время: {time}, оно также будет записано в таблицу.", reply_markup=types.ReplyKeyboardRemove())

    data = user.get_state(message.chat.id, "userdate")
    data["count"] += 1
    data["city"] = city
    data["lat"] = lat
    data["lon"] = lon
    data["date"] = date
    data[data["count"]] = dict()
    data[data["count"]]["time"] = time


    user.update_state(message.chat.id, "userdate", data)

    get_info(message=message, query=["new", "from_geo"])
    




def geo_cancel(call, query):
    last = bot.send_message(call.message.chat.id, "Возврат в меню...", reply_markup=types.ReplyKeyboardRemove())

    bot.delete_message(call.message.chat.id, call.message.id)
    bot.delete_message(call.message.chat.id, query[0])
    bot.delete_message(call.message.chat.id, last.id)

    menu(call.message)




def get_info(call=None, query=None, message=None):
    if call is not None:
        message = call.message

    data = user.get_state(message.chat.id, "userdate")
    markup = types.InlineKeyboardMarkup()

    if query[0] == "new":
        if query[1] == "continue":
            data["count"] += 1
            data[data["count"]] = dict()
            date, time = time_handler(data["lat"], data["lon"])
            data[data["count"]]["time"] = time

        text = "Хорошо, теперь укажите яркость, пожалуйтса. Если вам надо ознакомиться со шкалой яркости это можно сделать с помощью команды /about -> 'Дневник наблюдателя' -> 'Шкала яркости'"

        markup.add(types.InlineKeyboardButton("1", callback_data="userdate brightness 1"))
        markup.add(types.InlineKeyboardButton("2", callback_data="userdate brightness 2"))
        markup.add(types.InlineKeyboardButton("3", callback_data="userdate brightness 3"))
        markup.add(types.InlineKeyboardButton("4", callback_data="userdate brightness 4"))
        markup.add(types.InlineKeyboardButton("5", callback_data="userdate brightness 5"))
    
    


    if query[0] == "brightness":
        data[data["count"]]["brightness"] = query[1]

        text = "Хорошо, а теперь укажите облачность, пожалуйста. Ознакомиться с ней можно с помощью команды /about -> 'Параметры видимости СО' -> 'Погода'. "

        markup.add(types.InlineKeyboardButton("А", callback_data="userdate weather А"))
        markup.add(types.InlineKeyboardButton("Б", callback_data="userdate weather Б"))
        markup.add(types.InlineKeyboardButton("В", callback_data="userdate weather В"))
        markup.add(types.InlineKeyboardButton("Г", callback_data="userdate weather Г"))
        markup.add(types.InlineKeyboardButton("Д", callback_data="userdate weather Д"))
    
    if query[0] == "weather":
        data[data["count"]]["weather"] = query[1]

        text = "Хорошо, а теперь укажите интенсивность, пожалуйста. Ознакомиться с ней можно с помощью команды /about -> 'Параметры видимости СО' -> 'Интенсивность'. "

        markup.add(types.InlineKeyboardButton("1", callback_data="userdate intensity 1"))
        markup.add(types.InlineKeyboardButton("2", callback_data="userdate intensity 2"))
        markup.add(types.InlineKeyboardButton("3", callback_data="userdate intensity 3"))
        markup.add(types.InlineKeyboardButton("4", callback_data="userdate intensity 4"))
        markup.add(types.InlineKeyboardButton("5", callback_data="userdate intensity 5"))
        markup.add(types.InlineKeyboardButton("6", callback_data="userdate intensity 6"))
        markup.add(types.InlineKeyboardButton("7", callback_data="userdate intensity 7"))
        markup.add(types.InlineKeyboardButton("8", callback_data="userdate intensity 8"))
        markup.add(types.InlineKeyboardButton("9", callback_data="userdate intensity 9"))
        markup.add(types.InlineKeyboardButton("10", callback_data="userdate intensity 10"))

    if query[0] == "intensity":
        data[data["count"]]["intensity"] = query[1]

        text = "Хорошо, вы заполнили еще один временной промежуток. Через 30 минут бот вам напомнит заполнить следующий, если вы хотите завершить наблюдение - нажмите кнопку 'Завершить наблюдение'"

        user.update_state(message.chat.id, "active", True)

        markup.add(types.InlineKeyboardButton("Завершить наблюдение", callback_data="give cancel_write"))
        
        th = Thread(target=waiting, args=(message.chat.id, ))
        th.start()

       
    user.update_state(message.chat.id, "userdate", data)


    if query[1] == "from_geo":
        bot.send_message(message.chat.id, text, reply_markup=markup)
    else:
        change(message, text=text, reply_markup=markup)
