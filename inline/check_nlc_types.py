from api import bot
from telebot import types
from database import user
from commands.menu import menu_cmd
from inline.about_nlc import edit

def check_nlc_types(call, query):
    if query[0] == "check":
        try:
            if query[1] == "return":
                edit(call.message)
                mes = bot.send_message(call.message.chat.id, "Отправьте ваше новое фото серебристых облаков для распознание типов или нажмите 'Отмена'", reply_markup=types.InlineKeyboardMarkup((
                [[types.InlineKeyboardButton("Отмена", callback_data="nlc cancel")]]
                )))
                user.update_state(call.message.chat.id, "types nlc", True)
                user.update_state(call.message.chat.id, "id", mes.id)
                return          
        except:
            bot.delete_message(call.message.chat.id, call.message.id)
            mes = bot.send_message(call.message.chat.id, "Отправьте ваше фото серебристых облоков для распознание типов или нажмите 'Отмена'", reply_markup=types.InlineKeyboardMarkup((
            [[types.InlineKeyboardButton("Отмена", callback_data="nlc cancel")]]
            )))
            user.update_state(call.message.chat.id, "types nlc", True)
            user.update_state(call.message.chat.id, "id", mes.id)

    elif query[0] == "cancel":
        state = user.update_state(call.message.chat.id, "types nlc", False)
        user.update_state(call.message.chat.id, "id", None)
        bot.delete_message(call.message.chat.id, call.message.id)
        menu_cmd(call.message)