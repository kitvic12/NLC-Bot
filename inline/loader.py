from inline.see_video_query import see_what
from inline.see_video_query import what_camera
from inline.see_video_query import camera
from inline.see_video_query import return_menu
from inline.see_video_query import return_camera


from inline.do_you_see_nlc import see_nlc

from inline.subscribe import need_resp

from inline.about_nlc import type_choise
from inline.about_nlc import light_check
from inline.about_nlc import types_send_nlc
from inline.about_nlc import back

from inline.check_nlc_types import check_nlc_types

from inline.see_now import see_now, send_all

from inline.admins_inline import admins

handler_map = {
    "see_video":see_what,
    "see":what_camera,
    "seen":camera,
    "menu":return_menu,
    "light":light_check,
    "type":type_choise,
    "types":types_send_nlc,
    "back":back,
    "return_camera":return_camera,
    "will_see":see_nlc,
    "subscribe":need_resp,
    "nlc":check_nlc_types,
    "see_now": see_now,
    "admin":admins,
    "send":send_all
}