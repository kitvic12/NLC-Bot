from core.api import bot
from telebot import types
from core.database import user
from core.main import change


# from AI.types.check_nlc import handle_photo as handle_types
# from AI.nlc_or_cloud.check_on_camera import handle_photo as handle_have

#inline

def check_nlc_types(call, query):
        try:
            if query[1] == "return":
                change(call.message, "Отправьте ваше новое фото СО для анализа их типов или нажмите 'Отмена'", reply_markup=types.InlineKeyboardMarkup((
                [[types.InlineKeyboardButton("Отмена", callback_data="nlc cancel")]]
                )))
                user.update_state(call.message.chat.id, "types nlc", True)
                user.update_state(call.message.chat.id, "id", call.message.id)
                return          
        except:
            change(call.message, "Отправьте ваше фото СО для анализа их типов или нажмите 'Отмена'", reply_markup=types.InlineKeyboardMarkup((
            [[types.InlineKeyboardButton("Отмена", callback_data="menu yes nlc_types")]]
            )))
            user.update_state(call.message.chat.id, "types nlc", True)
            user.update_state(call.message.chat.id, "id", call.message.id)



#message

def handle_nlc_photo(message, _):
    state = user.get_state(message.chat.id, "types nlc")
    id = user.get_state(message.chat.id, "id")
    if state:
        bot.delete_message(message.chat.id, id)
        try:
            # type = handle_types(message.photo)
            # resp += type
            resp = "Технические работы, приносим свои извинения..."
            bot.reply_to(message, resp, reply_markup=types.InlineKeyboardMarkup(
            [[types.InlineKeyboardButton("Повторить", callback_data="nlc check return")],
            [types.InlineKeyboardButton("В меню", callback_data="menu no")]]))
        except Exception as e:
            print(f"⚠ Ошибка обработки фото: {str(e)}")
    return True