from .api import bot
from .log import log
from telebot import types
from .config import config
from .user_activity import activity_tracker




#command

from function.start import start_cmd
from function.help import help_cmd, admin_command
from function.get import get
from function.menu import menu_cmd
from function.about import about_cmd
from function.user_activity_cmd import show_all_users
from function.callback import callback_handler
from function.fake import fake
from function.admins import amdin_list_command
from function.clear import clear_cmd
from function.get_userdate import get_location




#message

from .resp import resp_all
from function.callback import resp_handler, owner_respons
from function.check_nlc_types import handle_nlc_photo
from function.do_you_see_nlc import place, place_photo
from function.admins import admins_handler

message_callbacks = [place, admins_handler, resp_handler, owner_respons, resp_all]
image_callbacks = [place_photo]
geo_callback = [get_location]



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



@bot.message_handler(content_types=["location"])
def callback_image(message):
    activity_tracker.update_activity(message.from_user, 'message')
    log(f"{message.from_user.username}: <location>", "Message")
    didreturn = False
    for callback in geo_callback:
        if callback(message, didreturn):
            if callback(message, didreturn):
                didreturn = True    




#inline

from function.see_video_query import see_what
from function.see_video_query import what_camera
from function.see_video_query import camera
from function.see_video_query import return_camera
from function.see_video_query import place_camera

from function.get_userdate import get_userdate

from function.do_you_see_nlc import see_nlc

from function.subscribe import need_resp

from function.about import main_handler


from function.check_nlc_types import check_nlc_types

from function.see_now import see_now, send_all

from function.admins import admins

from .main import return_menu

from function.get_userdate import geo_cancel, get_info

handler_map = {
    "see_video":see_what,
    "see":what_camera,
    "seen":camera,
    "menu":return_menu,
    "nlc":main_handler,
    "return_camera":return_camera,
    "will_see":see_nlc,
    "subscribe":need_resp,
    "nlc_types":check_nlc_types,
    "see_now": see_now,
    "admin":admins,
    "send":send_all,
    "see_place":place_camera,
    "give":get_userdate,                                 
    "geo_cancel":geo_cancel,
    "userdate":get_info
}



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