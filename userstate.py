import pickle
from log import log

filename = 'userstate.pkl'

dont_log = ["last markup"]

def save_userstate(users):
    global filename
    with open(filename, "wb") as file:
        pickle.dump(users, file)

def load_userstate():
    global filename
    try:
        with open(filename, "rb") as file:
            users = pickle.load(file)
        return users
    except FileNotFoundError:
        return {}
    

def update_state(user, key, state):
    global dont_log
    users = load_userstate()
    if user not in users:
        users[user]={}
    users[user][key] = state
    if key not in dont_log:
        log(f"State {key} for {user} updated to {state}", "State")
    save_userstate(users)
    return state

def get_state(user, key, default = None):
    users = load_userstate()
    if user not in users:
        return False
    elif key not in users[user]:
        if default:
            return default
        else:
            return False
    return users[user][key]