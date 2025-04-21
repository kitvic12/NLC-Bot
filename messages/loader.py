from messages.resp import resp_all
from messages.callback_m import resp_handler, owner_respons
from messages.check_types import handle_nlc_photo
from messages.place_when_see import place
from messages.admins_mes import admins_handler

message_callbacks = [place, admins_handler, resp_handler, owner_respons, resp_all]
image_callbacks = [handle_nlc_photo]