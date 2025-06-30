from api import bot
from telebot import types
from database import user
from main import change
from git import Repo
import os
import log
import pandas as pd

from inline.pat_token import pat_token as GITHUB_TOKEN 

GITHUB_REPO_URL = "https://github.com/kitvic12/NLC-Database.git"
LOCAL_REPO_DIR = "temp_repo"       
FILE_NAME = "data.csv"             
TABLE_COLUMNS = ["name", "place", "date", "time", "brightness", "weather", "intensity"]

def add_to_github_table(new_row):
    try:
        if not os.path.exists(LOCAL_REPO_DIR):
            repo_url = GITHUB_REPO_URL.replace(
                "https://", 
                f"https://{GITHUB_TOKEN}@"
            )
            Repo.clone_from(repo_url, LOCAL_REPO_DIR)
        
        repo = Repo(LOCAL_REPO_DIR)
        repo.remotes.origin.pull()
        file_path = os.path.join(LOCAL_REPO_DIR, FILE_NAME)
        if not os.path.exists(file_path):
            pd.DataFrame(columns=TABLE_COLUMNS).to_csv(file_path, index=False)


        if FILE_NAME.endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path, engine='openpyxl')


        if len(new_row) != len(TABLE_COLUMNS):
            raise ValueError(
                f"Ошибка: Нужно {len(TABLE_COLUMNS)} значений. Получено: {new_row}"
            )
        
        df.loc[len(df)] = new_row

        if FILE_NAME.endswith('.csv'):
            df.to_csv(file_path, index=False)
        else:
            df.to_excel(file_path, index=False, engine='openpyxl')


        repo.git.add(FILE_NAME) 
        repo.index.commit(f"Upd Data")
        repo.remotes.origin.push()

        log.log(f"Upload to GH completed!")

    except Exception as e:
        log.error(f"Error: {e}")




def give(call, query):
    if query[0] == "start":
        change(call.message, "Укажите место и дату вашего наблдения разделив их запятой. Дату укажите в формате ДД.ММ.ГГГГ", reply_markup=types.InlineKeyboardMarkup(
            [[types.InlineKeyboardButton("Отмена", callback_data="menu yes")]]
        ))
        user.update_state(call.message.chat.id, "wait for place and date", True)

    elif query[0] == "cancel":
        change(call.message, "Спасибо вам большое за то, что поделились вашими наблюдениями! Ваши записи как и другие вы уже можете посмотреть на сайте.", reply_markup=types.InlineKeyboardMarkup([
            [types.InlineKeyboardButton("В меню", callback_data="menu back")]
        ]))
        for elem in user.get_state(call.message.chat.id, "data"):
            mes_to_upd = []
            mes_to_upd.extend(user.get_state(call.message.chat.id, "date and place").split(", "))
            mes_to_upd.extend(user.get_state(call.message.chat.id, "data")[elem].split(","))
            print(mes_to_upd)
            add_to_github_table(mes_to_upd)