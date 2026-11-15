# /*********************
# Mã sinh viên: 202418900
# Họ tên: Nguyễn Đăng Hiếu
# *********************/

from abc import ABC, abstractmethod


class IDevice(ABC):
    """Abstraction chung của mọi thiết bị: bật và tắt."""

    @abstractmethod
    def turn_on(self) -> None:
        pass

    @abstractmethod
    def turn_off(self) -> None:
        pass


class ILockable(ABC):
    """Khả năng khóa/mở khóa. Tách riêng khỏi IDevice vì đèn và quạt không khóa được."""

    @abstractmethod
    def lock(self) -> None:
        pass

    @abstractmethod
    def unlock(self) -> None:
        pass


# Ba lớp bên dưới cố ý không dùng lớp cơ sở chung chỉ để tái sử dụng vài dòng print
# (theo yêu cầu của đề), mỗi lớp tự cài đặt hành vi và trạng thái của mình.

class SmartLight(IDevice):
    """Đèn thông minh."""

    def __init__(self, name: str):
        self.name = name
        self._is_on = False

    @property
    def is_on(self) -> bool:
        """Trạng thái hiện tại, dùng để kiểm thử."""
        return self._is_on

    def turn_on(self) -> None:
        self._is_on = True
        print(f"{self.name}: ON")

    def turn_off(self) -> None:
        self._is_on = False
        print(f"{self.name}: OFF")


class SmartFan(IDevice):
    """Quạt thông minh."""

    def __init__(self, name: str):
        self.name = name
        self._is_on = False

    @property
    def is_on(self) -> bool:
        return self._is_on

    def turn_on(self) -> None:
        self._is_on = True
        print(f"{self.name}: ON")

    def turn_off(self) -> None:
        self._is_on = False
        print(f"{self.name}: OFF")


class SmartDoor(IDevice, ILockable):
    """Cửa thông minh: vừa bật/tắt được, vừa khóa/mở khóa được."""

    def __init__(self, name: str):
        self.name = name
        self._is_on = False
        self._is_locked = False

    @property
    def is_on(self) -> bool:
        return self._is_on

    @property
    def is_locked(self) -> bool:
        return self._is_locked

    def turn_on(self) -> None:
        self._is_on = True
        print(f"{self.name}: ON")

    def turn_off(self) -> None:
        self._is_on = False
        print(f"{self.name}: OFF")

    def lock(self) -> None:
        self._is_locked = True
        print(f"{self.name}: LOCKED")

    def unlock(self) -> None:
        self._is_locked = False
        print(f"{self.name}: UNLOCKED")
