# /*********************
# Mã sinh viên: 202418900
# Họ tên: Nguyễn Đăng Hiếu
# *********************/

import threading
from typing import final

# Khóa nội bộ: chỉ thuộc tính instance mới có khóa này nên bên ngoài không tạo trực tiếp được
_CREATE_KEY = object()


class _SingletonMeta(type):
    """
    Metaclass cung cấp thuộc tính cấp lớp `HomeConfiguration.instance`.
    Cách chồng @classmethod lên @property đã bị gỡ từ Python 3.13 nên dùng metaclass để chạy ổn định.
    """

    @property
    def instance(cls):
        # Double-checked locking: chỉ khóa khi chưa có thể hiện, an toàn khi nhiều luồng cùng gọi
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls(_create_key=_CREATE_KEY)
        return cls._instance


@final
class HomeConfiguration(metaclass=_SingletonMeta):
    """
    Singleton: cấu hình chung của ngôi nhà, toàn ứng dụng chỉ có một thể hiện.
    Truy cập qua HomeConfiguration.instance.
    """

    _instance = None
    _lock = threading.Lock()

    def __init__(self, _create_key=None):
        # Python không có constructor private, nên chặn gọi trực tiếp HomeConfiguration()
        if _create_key is not _CREATE_KEY:
            raise TypeError("HomeConfiguration la Singleton, hay dung HomeConfiguration.instance")
        self.home_name = "My Home"
        self.night_light_level = 30

    def __init_subclass__(cls, **kwargs):
        # Tương đương "sealed" trong C#: không cho kế thừa để không tạo thêm thể hiện thứ hai
        raise TypeError("HomeConfiguration khong duoc ke thua (sealed)")
