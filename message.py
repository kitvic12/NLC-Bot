from api import bot
from commands import loader
from log import log
from telebot import types

from config import config

from messages.loader import message_callbacks,image_callbacks

from user_activity import activity_tracker


@bot.message_handler(content_types=["text"])
def callback_message(message):
    activity_tracker.update_activity(message.from_user, 'message')
    log(f"{message.from_user.username}: {message.text}", "Message")
    didreturn = False
    for callback in message_callbacks:
        if callback(message, didreturn):
            didreturn = True
            
@bot.message_handler(content_types=["photo"])
def callback_image(message):
    activity_tracker.update_activity(message.from_user, 'message')
    log(f"{message.from_user.username}: <picture>", "Message")
    didreturn = False
    for callback in image_callbacks:
        if callback(message, didreturn):
            if callback(message, didreturn):
                didreturn = True