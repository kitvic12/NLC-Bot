from api import bot

from log import log
from config import config
from telebot import types

from database import activity_tracker


from inline.loader import handler_map

@bot.callback_query_handler()
def callback_inline(call):
    user = call.from_user
    activity_tracker.update_activity(user, 'inline')
    log(f"New query from {call.message.chat.username}: {call.data}", "Inline")
    try:
        if call.message:
            data = call.data.split(' ')
            if data[0] in handler_map:
                handler_map[data[0]](call, data[1:])
    except Exception as e:
        print(repr(e))