from api import bot
from inline.see_video_query import place
from camera.weather import check_cloudiness, locations
from camera.get_image import get_camera_image
from AI.nlc_or_cloud.check_on_camera import handle_photo
from inline.subscribe import load_data
from log import check
from commands.menu import menu
from always_check import moscow_time
from telebot import types

def see_now(call, query):
    have = []
    have_nlc = False

    bot.delete_message(call.message.chat.id, call.message.id)

    last = bot.send_message(call.message.chat.id, "Началась проверка на наличие серебристых облаков на камерах, ожидайте...")
    check("----------------", "CHECK")
    check(f"Start check at {moscow_time()}", "CHECK")

    for i in range(len(place)):
        lat = locations[place[i]]["lat"]
        lon = locations[place[i]]["lon"]
        cloud = check_cloudiness(lat, lon, place[i])

        if cloud:
            photo = get_camera_image(place[i])
            check_nlc = handle_photo(photo)

            if check_nlc: 
                have_nlc = True
                check(f"{place[i]} maybe see nlc", "CHECK")
                bot.send_photo(call.message.chat.id, photo, f"Подозрение на наличие серебристых облаков на камере  {place[i]}. Вы согласны с ниличем СО на фото?", reply_markup=types.InlineKeyboardMarkup((
                    [[types.InlineKeyboardButton("Да, там есть СО", callback_data=f"send yes {place[i]}")]],
                    [[types.InlineKeyboardButton("Нет, там нет СО", callback_data=f"send no")]]
                )))

    check("----------------", "CHECK")
    bot.delete_message(call.message.chat.id, last.id)

    if not have_nlc:
        bot.send_message(call.message.chat.id, "Серебристые облака не были обнаружены, ожидайте возврата в меню.")
    menu(call.message)


def send_all(call, query):
    if query[0] == "no":
        bot.send_message(call.message.chat.id, "Хорошо, буду знать, что это ошибочное сообщение.")
        menu(call.message)
        return
    elif query[0] == "yes":
        mes = bot.send_message(call.message.chat.id, "Хорошо, запускаю рассылку оповещений, ожидайте...")
        photo = get_camera_image(query[1])
        for chat in load_data():
            if chat == call.message.chat.id:
                continue
            else:
                bot.send_photo(call.message.chat.id, photo, f"Были обнаружены серебристые облака на камере {query[1]}! Удачных наблюдений!")
        bot.edit_message_text("Все оповещения успешно отправлены! Ожидайте возврата в меню", call.message.chat.id, mes.id)        
        menu(call.message)