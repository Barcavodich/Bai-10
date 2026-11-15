# /*********************
# Mã sinh viên: 202418900
# Họ tên: Nguyễn Đăng Hiếu
# *********************/

import threading

class HomeConfiguration:
    _instance = None
    _lock = threading.Lock()

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self.home_name = "My Home"
        self.night_light_level = 30
        self._initialized = True

    @classmethod
    @property
    def instance(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance