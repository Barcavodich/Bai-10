# /*********************
# Mã sinh viên: 202418900
# Họ tên: Nguyễn Đăng Hiếu
# *********************/

from devices import IDevice, SmartLight, SmartFan, SmartDoor


class DeviceFactory:
    """
    Factory: tạo thiết bị theo loại do người dùng chọn.
    Client chỉ biết IDevice và chuỗi loại, không gọi constructor của lớp cụ thể.
    """

    @staticmethod
    def create(device_type: str, name: str) -> IDevice:
        """
        Tạo thiết bị. Chuỗi loại không phân biệt hoa/thường và được cắt khoảng trắng.
        Loại không hỗ trợ thì ném ValueError (tương đương ArgumentException), không trả về None.
        """
        normalized_type = device_type.strip().lower()
        if normalized_type == "light":
            return SmartLight(name)
        elif normalized_type == "fan":
            return SmartFan(name)
        elif normalized_type == "door":
            return SmartDoor(name)
        else:
            raise ValueError(f"Unsupported device type: {device_type}")
