import time
from threading import Lock

class ChatSessionManager:
    def __init__(self, timeout_seconds=1800):
        self.sessions = {}
        self.timeout = timeout_seconds
        self.lock = Lock()

    def get_session(self, uid, lecture_id):
        key = f"{lecture_id}:{uid}"
        with self.lock:
            session = self.sessions.get(key)
            if session and time.time() - session['last_active'] < self.timeout:
                session['last_active'] = time.time()
                return session['chat_session'], session['history']
            return None, None

    def set_session(self, uid, lecture_id, chat_session, history):
        key = f"{lecture_id}:{uid}"
        with self.lock:
            self.sessions[key] = {
                'chat_session': chat_session,
                'history': history,
                'last_active': time.time()
            }

    def clear_expired_sessions(self):
        now = time.time()
        with self.lock:
            expired = [k for k, v in self.sessions.items() if now - v['last_active'] > self.timeout]
            for k in expired:
                del self.sessions[k]
