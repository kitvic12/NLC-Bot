from messages.resp import resp_all
from messages.callback_m import resp_handler, owner_respons
from messages.check_photo import handle_nlc_photo
from messages.system_for_add_to_site import get_place
from messages.place_when_see import place, place_photo
from messages.admins_mes import admins_handler

message_callbacks = [place, admins_handler, get_place, resp_handler, owner_respons, resp_all]
image_callbacks = [place_photo]