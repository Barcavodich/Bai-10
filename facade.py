# /*********************
# Mã sinh viên: 202418900
# Họ tên: Nguyễn Đăng Hiếu
# *********************/

from devices import IDevice, ILockable
from configuration import HomeConfiguration


class SmartHomeFacade:
    """
    Facade: cung cấp các chế độ mức cao (Đi làm, Đi ngủ) cho nhiều thiết bị.
    Facade chỉ giữ abstraction (IDevice, ILockable), không thay thế các lớp thiết bị:
    client vẫn điều khiển riêng từng thiết bị khi cần.
    """

    def __init__(self, light: IDevice, fan: IDevice, door: ILockable, config=None):
        self._light = light
        self._fan = fan
        self._door = door
        # Cho phép truyền cấu hình từ ngoài (Dependency Injection) để dễ kiểm thử,
        # mặc định dùng Singleton của ứng dụng
        self._config = config if config is not None else HomeConfiguration.instance

    def go_to_work(self) -> None:
        """Chế độ đi làm: tắt đèn, tắt quạt, khóa cửa."""
        self._light.turn_off()
        self._fan.turn_off()
        self._door.lock()

    def go_to_sleep(self) -> None:
        """Chế độ đi ngủ: tắt quạt, khóa cửa, bật đèn ngủ ở mức sáng đọc từ cấu hình."""
        self._fan.turn_off()
        self._door.lock()
        self._light.turn_on()
        level = self._config.night_light_level
        print(f"Night light level: {level}%")
