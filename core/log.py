from datetime import datetime
import pytz
from .api import bot
from .config import config
import traceback
import os

MOSCOW_TZ = pytz.timezone('Europe/Moscow')


log_files = {
    "log": "./files/botlog.log",
    "errorlog": "./files/errorlog.log",
    "checklog": "./files/checklog.log"
}

def moscow_time():
    now = datetime.now(MOSCOW_TZ)
    return now.strftime("%Y-%m-%d %H:%M:%S")

def get_log_file(log_type):
    return open(log_files[log_type], "a", encoding="utf-8")

def log_print(text):
    print(text)
    with get_log_file("log") as f:
        print(text, file=f, flush=True)

def log_init():
    log_print("----------------------------")

def log(text, level="Info"):
    log_print(f"[{level}] {text}")

def error_print(text):
    print(text)
    with get_log_file("errorlog") as f:
        print(text, file=f, flush=True)

def error_init():
    error_print("----------------------------")

def error(text, level="Info"):
    error_print(f"[{level}] {text}")

def check_print(text):
    print(text)
    with get_log_file("checklog") as f:
        print(text, file=f, flush=True)

def check_init():
    check_print("----------------------------")

def check(text, level="Info"):
    check_print(f"[{level}] {text}")

log_dict = {
    "log": ("botlog.log", log_init, log),
    "errorlog": ("errorlog.log", error_init, error),
    "checklog": ("checklog.log", check_init, check)
}

def clear_log(log_type, id):
    time = moscow_time()
    try:
        if log_type not in log_dict:
            raise KeyError(f"Лог {log_type} не найден в log_dict")     
        log_file_path, init_func, log_func = log_dict[log_type]
        for f in [log_file, error_log_file, check_log_file]:
            try:
                if not f.closed:
                    f.close()
            except:
                pass
        with open(log_file_path, "wb") as f:
            f.write(b'')

        if os.path.getsize(log_file_path) != 0:
            raise IOError("Файл не был очищен")
        
        if init_func:
            init_func()
        if log_func:
            log_func(f"Start after cleaning at {time}", "Info")
        
        return True
        
    except Exception as e:
        error_message = f"Ошибка: {str(e)}\n\nТрассировка:\n{traceback.format_exc()}"
        bot.send_message(id, f"⚠️ Ошибка:\n```\n{error_message}\n```", parse_mode="MarkdownV2")
        return False


log_file = open("./botlog.log", "a", encoding="utf-8")
error_log_file = open("./errorlog.log", "a", encoding="utf-8")
check_log_file = open("./checklog.log", "a", encoding="utf-8")