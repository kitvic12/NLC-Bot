from AI.types.check_nlc import handle_photo
import userstate
from api import bot

def handle_nlc_photo(message, _):
    state = userstate.get_state(message.chat.id, "types nlc")
    id = userstate.get_state(message.chat.id, "id")
    if state:
        bot.delete_message(message.chat.id, id)
        handle_photo(message)