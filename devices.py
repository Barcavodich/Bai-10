# /*********************
# Mã sinh viên: 202418900
# Họ tên: Nguyễn Đăng Hiếu
# *********************/

from abc import ABC, abstractmethod

class IDevice(ABC):
    @abstractmethod
    def turn_on(self) -> None:
        pass

    @abstractmethod
    def turn_off(self) -> None:
        pass

class ILockable(ABC):
    @abstractmethod
    def lock(self) -> None:
        pass

    @abstractmethod
    def unlock(self) -> None:
        pass

class SmartLight(IDevice):
    def __init__(self, name: str):
        self.name = name

    def turn_on(self) -> None:
        print(f"{self.name}: ON")

    def turn_off(self) -> None:
        print(f"{self.name}: OFF")

class SmartFan(IDevice):
    def __init__(self, name: str):
        self.name = name

    def turn_on(self) -> None:
        print(f"{self.name}: ON")

    def turn_off(self) -> None:
        print(f"{self.name}: OFF")

class SmartDoor(IDevice, ILockable):
    def __init__(self, name: str):
        self.name = name
        self._is_locked = False

    def turn_on(self) -> None:
        print(f"{self.name}: ON")

    def turn_off(self) -> None:
        print(f"{self.name}: OFF")

    def lock(self) -> None:
        self._is_locked = True
        print(f"{self.name}: LOCKED")

    def unlock(self) -> None:
        self._is_locked = False
        print(f"{self.name}: UNLOCKED")