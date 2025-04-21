from api import bot
from telebot import types

photo = open(r"photo/NLC.jpg", "rb")

from database import activity_tracker

@bot.message_handler(commands=["about"])
def about_cmd(message):
    activity_tracker.update_activity(message.from_user, 'command')
    bot.send_photo(
    message.chat.id, 
    photo, 
    "Серебристые облака - это сравнительно редкое атмосферное явление, крайне разрежённые облака, состоящие из мелких льдинок, которые подсвечивает солнце. Возникают эти облака в мезосфере под мезопаузой (на высоте 76—85 км над поверхностью Земли) и видимые в глубоких сумерках, непосредственно после заката или перед восходом Солнца.",
    reply_markup=types.InlineKeyboardMarkup(
        [[types.InlineKeyboardButton("Типы СО", callback_data="type")],
         [types.InlineKeyboardButton("Яркость СО", callback_data="light")]]
    )
    )