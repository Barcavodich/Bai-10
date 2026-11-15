# /*********************
# Mã sinh viên: 202418900
# Họ tên: Nguyễn Đăng Hiếu
# *********************/

from devices import IDevice, ILockable
from configuration import HomeConfiguration

class SmartHomeFacade:
    def __init__(self, light: IDevice, fan: IDevice, door: ILockable):
        self._light = light
        self._fan = fan
        self._door = door

    def go_to_work(self) -> None:
        self._light.turn_off()
        self._fan.turn_off()
        self._door.lock()

    def go_to_sleep(self) -> None:
        self._fan.turn_off()
        self._door.lock()
        self._light.turn_on()
        level = HomeConfiguration.instance.night_light_level
        print(f"Night light level: {level}%")