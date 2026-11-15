# /*********************
# Mã sinh viên: 202418900
# Họ tên: Nguyễn Đăng Hiếu
# *********************/

from devices import IDevice, SmartLight, SmartFan, SmartDoor

class DeviceFactory:
    @staticmethod
    def create(device_type: str, name: str) -> IDevice:
        normalized_type = device_type.strip().lower()
        if normalized_type == "light":
            return SmartLight(name)
        elif normalized_type == "fan":
            return SmartFan(name)
        elif normalized_type == "door":
            return SmartDoor(name)
        else:
            raise ValueError(f"Unsupported device type: {device_type}")