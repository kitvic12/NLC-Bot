import json
from typing import Dict, Any, Optional
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

class UserDatabase:
    def __init__(self, filename: str = 'database.json'):
        self.filename = filename
        self.data = self._load_data()
    
    def _load_data(self) -> Dict[int, Dict[str, Any]]:
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return {
                    int(user_id): {
                        'username': user_data.get('username', None),  
                        'userstate': {str(k): v for k, v in user_data.get('userstate', {}).items()},
                        'notification': user_data.get('notification', 'off')
                    }
                    for user_id, user_data in data.items()
                }
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def _save_data(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(
                {str(user_id): user_data for user_id, user_data in self.data.items()},
                f,
                indent=4,
                ensure_ascii=False
            )
    
    def add_user(self, user_id: int, username: Optional[str] = None):  
        if user_id not in self.data:
            self.data[user_id] = {
                'username': username, 
                'userstate': {},
                'notification': 'on'
            }
            self._save_data()
        elif username is not None and self.data[user_id].get('username') is None: 
            self.data[user_id]['username'] = username
            self._save_data()
    
    def update_state(self, user_id: int, key: Any, value: Any):
        if user_id in self.data:
            str_key = str(key) 
            if 'userstate' not in self.data[user_id]:
                self.data[user_id]['userstate'] = {}
            self.data[user_id]['userstate'][str_key] = value
            self._save_data()
    
    def get_state(self, user_id: int, key: Any, default: Any = None) -> Any:
        user = self.get_user(user_id)
        if user and 'userstate' in user:
            str_key = str(key)
            return user['userstate'].get(str_key, default)
        return default
    
    def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        return self.data.get(user_id)
    
    def set_notification(self, user_id: int, status: str):
        if user_id in self.data and status in ('on', 'off'):
            self.data[user_id]['notification'] = status
            self._save_data()

    def check(self, user_id: int):
        user = self.get_user(user_id)
        if user:
            return self.data[user_id]['notification'] == "on"

    def get_all_users(self):
        for user_id, user_data in self.data.items():
            yield {'user_id': user_id, **user_data}

    def save_user_markup(self, user_id: int, markup: InlineKeyboardMarkup):
        if user_id not in self.data:
            self.add_user(user_id)  

        self.data[user_id]['userstate']['keyboard'] = [
            [{'text': btn.text, **{k: v for k, v in btn.__dict__.items() if v}} 
             for btn in row] 
            for row in markup.keyboard
        ]
        self._save_data()

    def get_user_markup(self, user_id: int) -> InlineKeyboardMarkup:
        user = self.data.get(user_id)
        if not user or 'keyboard' not in user.get('userstate', {}):
            return False
            
        markup = InlineKeyboardMarkup()
        for row in user['userstate']['keyboard']:
            markup.add(*[InlineKeyboardButton(**btn) for btn in row])
        return markup
    
    def clear_user_markup(self, user_id: int) -> bool:
        if user_id in self.data and 'userstate' in self.data[user_id]:
            if 'keyboard' in self.data[user_id]['userstate']:
                del self.data[user_id]['userstate']['keyboard']
                self._save_data()
                return True
        return False
    
    def clear_all_userstates(self) -> int:
        count = 0
        for user_id in self.data:
            if 'userstate' in self.data[user_id] and self.data[user_id]['userstate']:
                self.data[user_id]['userstate'] = {}
                count += 1
        if count > 0:
            self._save_data()
        return count


def db_for_send(filename: str = 'database.json') -> list:
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            json_str = json.dumps(data, indent=4, ensure_ascii=False)
            MAX_LENGTH = 4096
            if len(json_str) <= MAX_LENGTH:
                return [json_str]
            parts = []
            current_part = []
            current_length = 0
            opening_brace = "{\n"
            current_part.append(opening_brace)
            current_length += len(opening_brace)
            for i, (user_id, user_data) in enumerate(data.items()):
                user_entry = f'    "{user_id}": {json.dumps(user_data, indent=4, ensure_ascii=False)}'
                if i < len(data) - 1:
                    user_entry += ",\n"
                else:
                    user_entry += "\n"
                if current_length + len(user_entry) > MAX_LENGTH - 2: 
                    current_part.append("}")
                    parts.append("".join(current_part))
                    current_part = [opening_brace, user_entry]
                    current_length = len(opening_brace) + len(user_entry)
                else:
                    current_part.append(user_entry)
                    current_length += len(user_entry)
            current_part.append("}")
            parts.append("".join(current_part))
            return parts
            
    except FileNotFoundError:
        return ["⚠ Файл базы данных не найден"]
    except json.JSONDecodeError:
        return ["⚠ Ошибка чтения базы данных (некорректный JSON)"]
    except Exception as e:
        return [f"⚠ Неизвестная ошибка: {str(e)}"]


user = UserDatabase()