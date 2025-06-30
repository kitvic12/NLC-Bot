from api import bot
from telebot import types


from user_activity import activity_tracker

@bot.message_handler(commands=["about"])
def about_cmd(message):
    activity_tracker.update_activity(message.from_user, 'command')
    bot.send_message(
    message.chat.id,  
    "В данной команде вы можете узнать как и о самих серебристых облаках(СО), так и о параметрах которые рекомендуется записывать во время набюдений для сбора статистики (также их можно отправлять в наш бот /menu -> 'Поделиться наблюдением').",
    reply_markup=types.InlineKeyboardMarkup(
        [[types.InlineKeyboardButton("Параметры видимости СО", callback_data=f"nlc choise_par {True}")],
         [types.InlineKeyboardButton("Базовые понятия о СО", callback_data=f"nlc about {True}")]]
    ))