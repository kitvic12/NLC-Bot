from api import bot
from telebot import types

def load_image(file_path):
    with open(file_path, 'rb') as f:
        return f.read()

photo = load_image(r"photo/NLC.jpg")

from user_activity import activity_tracker

@bot.message_handler(commands=["about"])
def about_cmd(message):
    activity_tracker.update_activity(message.from_user, 'command')
    bot.send_photo(
    message.chat.id, 
    photo, 
    "Серебристые облака - это сравнительно редкое атмосферное явление, крайне разрежённые облака, состоящие из мелких льдинок, которые подсвечивает солнце. Возникают эти облака в мезосфере под мезопаузой (на высоте 76—85 км над поверхностью Земли) и видимые в глубоких сумерках, непосредственно после заката или перед восходом Солнца.",
    reply_markup=types.InlineKeyboardMarkup(
        [[types.InlineKeyboardButton("Типы СО", callback_data="type_choise")],
         [types.InlineKeyboardButton("Яркость СО", callback_data="light")]]
    )
    )