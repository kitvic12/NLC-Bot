from inline.see_video_query import see_what
from inline.see_video_query import what_camera
from inline.see_video_query import camera
from inline.see_video_query import return_camera
from inline.see_video_query import place_camera

from inline.give_info import give

from inline.do_you_see_nlc import see_nlc

from inline.subscribe import need_resp

from inline.about_nlc import main_handler

from inline.add_data import get_intensity
from inline.add_data import get_brightness
from inline.add_data import get_weather

from inline.check_nlc_types import check_nlc_types

from inline.see_now import see_now, send_all

from inline.admins_inline import admins

from main import return_menu

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
    "give":give,
    "intensity":get_intensity,
    "weather":get_weather,
    "brightness":get_brightness
}