from AI.types.check_nlc import handle_photo as handle_types
from AI.nlc_or_cloud.check_on_camera import handle_photo as handle_have
from database import user
from telebot import types
from api import bot

def handle_nlc_photo(message, _):
    state = user.get_state(message.chat.id, "types nlc")
    id = user.get_state(message.chat.id, "id")
    if state:
        bot.delete_message(message.chat.id, id)
        try:
            file_info = bot.get_file(message.photo[-1].file_id)
            file_bytes = bot.download_file(file_info.file_path)
            have = handle_have(file_bytes)
            if have:
                resp = "Поздравляем, на вашем фото есть СО!"
                type = handle_types(message.photo)
                resp += type
                bot.reply_to(message, resp, reply_markup=types.InlineKeyboardMarkup(
                [[types.InlineKeyboardButton("Повторить", callback_data="nlc check return")],
                [types.InlineKeyboardButton("В меню", callback_data="menu no")]]))
            else:  
                bot.reply_to(message, "Сожалеем, на вашем фото нету СО :(", reply_markup=types.InlineKeyboardMarkup(
                [[types.InlineKeyboardButton("Повторить", callback_data="nlc check return")],
                 [types.InlineKeyboardButton("В меню", callback_data="menu no")]]))
        except Exception as e:
            print(f"⚠ Ошибка обработки фото: {str(e)}")
    return True