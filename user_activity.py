import pickle
from datetime import datetime
import os
import pytz
import log

USER_DB_FILE = "users_activity.pkl"
MOSCOW_TZ = pytz.timezone('Europe/Moscow')

class UserActivityTracker:
    def __init__(self):
        self.user_data = self._load_data()
        self.ACTION_TYPES = {
            'message': 'messages',
            'command': 'commands',
            'inline': 'inline'
        }
    
    def _load_data(self):
        if os.path.exists(USER_DB_FILE):
            try:
                with open(USER_DB_FILE, 'rb') as f:
                    data = pickle.load(f)
                    for user_id in data:
                        if 'actions' not in data[user_id]:
                            data[user_id]['actions'] = {v: 0 for v in self.ACTION_TYPES.values()}
                    return data
            except Exception as e:
                log.error(f"Data load error: {str(e)}", "DB_ERROR")
                return {}
        return {}

    def _save_data(self):
        try:
            with open(USER_DB_FILE, 'wb') as f:
                pickle.dump(self.user_data, f)
        except Exception as e:
            log.error(f"Data save error: {str(e)}", "DB_ERROR")

    def _get_moscow_time(self):
        return datetime.now(MOSCOW_TZ)

    def update_activity(self, user, action_type):
        if getattr(user, 'is_bot', False):
            print(f"⚠️ Bot detected! ID={user.id}, Username=@{user.username}")
            return

        normalized_type = self.ACTION_TYPES.get(action_type)
        if not normalized_type:
            log.error(f"Unknown action type: {action_type}", "ACTION_ERROR")
            return

        user_id = user.id
        now = self._get_moscow_time() 
        
        if user_id not in self.user_data:
            print(f"➕ New user: ID={user_id}, Username=@{user.username}")
            self.user_data[user_id] = {
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'first_seen': now,
                'last_seen': now,
                'actions': {v: 0 for v in self.ACTION_TYPES.values()}
            }
        
        self.user_data[user_id]['last_seen'] = now
        self.user_data[user_id]['actions'][normalized_type] += 1
        self._save_data()

        user_id = user.id
        now = self._get_moscow_time() 
        
        if user_id not in self.user_data:
            self.user_data[user_id] = {
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'first_seen': now,
                'last_seen': now,
                'actions': {v: 0 for v in self.ACTION_TYPES.values()}
            }
            log.log(f"New user registered: {user_id} (@{user.username}) at {now.strftime('%Y-%m-%d %H:%M:%S %Z')}")
        
        self.user_data[user_id]['last_seen'] = now
        self.user_data[user_id]['actions'][normalized_type] += 1
        self._save_data()

    def get_user_stats(self, user_id):
        return self.user_data.get(user_id, None)
    
    def get_all_users(self):
        return self.user_data

activity_tracker = UserActivityTracker()