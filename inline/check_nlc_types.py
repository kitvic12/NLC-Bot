from api import bot
from telebot import types
from database import user
from main import change

def check_nlc_types(call, query):
        try:
            if query[1] == "return":
                change(call.message, "Отправьте ваше новое фото неба для поного анализа на предмет наличия Со и их типов или нажмите 'Отмена'", reply_markup=types.InlineKeyboardMarkup((
                [[types.InlineKeyboardButton("Отмена", callback_data="nlc cancel")]]
                )))
                user.update_state(call.message.chat.id, "types nlc", True)
                user.update_state(call.message.chat.id, "id", call.message.id)
                return          
        except:
            change(call.message, "Отправьте ваше фото наба для полного анализа на предмет наличия СО и их типов или нажмите 'Отмена'", reply_markup=types.InlineKeyboardMarkup((
            [[types.InlineKeyboardButton("Отмена", callback_data="menu yes nlc_types")]]
            )))
            user.update_state(call.message.chat.id, "types nlc", True)
            user.update_state(call.message.chat.id, "id", call.message.id)



