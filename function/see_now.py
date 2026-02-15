from core.api import bot
from .see_video_query import place
from .weather import check_cloudiness, locations
from .get_image import get_camera_image
# from AI.nlc_or_cloud.check_on_camera import handle_photo
from core.database import user
from core.log import check
from .menu import menu_send
# from services import moscow_time
from telebot import types
from core.main import change

def see_now(call, query):
    have = []
    have_nlc = False

#     change(call.message, "Началась проверка на наличие серебристых облаков на камерах, ожидайте...")
#     check("----------------", "CHECK")
#     check(f"Start check at {moscow_time()}", "CHECK")

#     for i in range(len(place)):
#         lat = locations[place[i]]["lat"]
#         lon = locations[place[i]]["lon"]
#         cloud = check_cloudiness(lat, lon, place[i])

#         if cloud:
#             photo = get_camera_image(place[i])
#             check_nlc = handle_photo(photo)

#             # if check_nlc: 
#             #     have_nlc = True
#             #     bot.delete_message(call.message.chat.id, call.message.id)
#             #     check(f"{place[i]} maybe see nlc", "CHECK")
#             #     bot.send_photo(call.message.chat.id, photo, f"Подозрение на наличие серебристых облаков на камере  {place[i]}. Вы согласны с ниличем СО на фото?", reply_markup=types.InlineKeyboardMarkup((
#             #         [[types.InlineKeyboardButton("Да, там есть СО", callback_data=f"send yes {place[i]}")]],
#             #         [[types.InlineKeyboardButton("Нет, там нет СО", callback_data=f"send no")]]
#             #     )))

#     check("----------------", "CHECK")


#     if not have_nlc:
#         change(call.message, "Серебристые облака не были обнаружены, ожидайте возврата в меню.")
#         menu_send(call.message)


def send_all(call, query):
    if query[0] == "no":
        bot.send_message(call.message.chat.id, "Хорошо, буду знать, что это ошибочное сообщение.")
        menu_send(call.message)
        return
    elif query[0] == "yes":
        mes = bot.send_message(call.message.chat.id, "Хорошо, запускаю рассылку оповещений, ожидайте...")
        photo = get_camera_image(query[1])
        for users in user.get_all_users():
            if users['user_id'] == call.message.chat.id:
                continue
            elif users['notification'] == 'on':
                bot.send_photo(users['user_id'], f"Были обнаружены серебристые облака на камере {query[1]}! Удачных наблюдений!")
        bot.edit_message_text("Все оповещения успешно отправлены! Ожидайте возврата в меню", call.message.chat.id, mes.id)        
        menu_send(call.message)