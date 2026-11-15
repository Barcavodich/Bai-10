# /*********************
# Mã sinh viên: 202418900
# Họ tên: Nguyễn Đăng Hiếu
# *********************/

import io
import threading
from contextlib import redirect_stdout

from devices import IDevice, ILockable
from factory import DeviceFactory
from configuration import HomeConfiguration
from facade import SmartHomeFacade

failed = 0  # đếm số phép kiểm tra thất bại


def check(description: str, condition: bool) -> None:
    """In kết quả một phép kiểm tra dưới dạng PASS/FAIL."""
    global failed
    if not condition:
        failed += 1
    print(f"  [{'PASS' if condition else 'FAIL'}] {description}")


def raises(exception_type, func) -> bool:
    """Trả về True nếu func() ném đúng loại ngoại lệ."""
    try:
        func()
    except exception_type:
        return True
    except Exception:
        return False
    return False


def run_and_show(func) -> str:
    """Chạy func, in lại phần output ra màn hình và trả về để kiểm tra nội dung."""
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        func()
    text = buffer.getvalue()
    print(text, end="")
    return text


def run_tests():
    print("=== BAT DAU KIEM THU LAB 10: DESIGN PATTERNS ===")

    # T1: tạo light, fan, door qua Factory
    print("\n[T1] Factory tao dung kieu doi tuong:")
    light = DeviceFactory.create("light", "Living room light")
    fan = DeviceFactory.create("fan", "Living room fan")
    door = DeviceFactory.create("door", "Main door")
    print(f"  Created: {type(light).__name__}, {type(fan).__name__}, {type(door).__name__}")
    check("light la SmartLight", type(light).__name__ == "SmartLight")
    check("fan la SmartFan", type(fan).__name__ == "SmartFan")
    check("door la SmartDoor", type(door).__name__ == "SmartDoor")
    check("Ca ba deu la IDevice", all(isinstance(d, IDevice) for d in (light, fan, door)))
    check("Chi cua moi khoa duoc (ILockable)",
          isinstance(door, ILockable) and not isinstance(light, ILockable) and not isinstance(fan, ILockable))
    check("Chuoi loai khong phan biet hoa thuong va khoang trang",
          type(DeviceFactory.create("  LiGhT ", "Test")).__name__ == "SmartLight")

    # T2: tạo loại chưa hỗ trợ
    print("\n[T2] Loai khong ho tro:")
    check("Tao 'camera' phai nem ValueError (khong tra ve None)",
          raises(ValueError, lambda: DeviceFactory.create("camera", "Security camera")))
    try:
        DeviceFactory.create("camera", "Security camera")
    except ValueError as e:
        print(f"  Caught expected exception: {e}")

    # T3: Singleton. Đây là lần đầu truy cập instance nên thử luôn nhiều luồng cùng lúc
    print("\n[T3] Singleton HomeConfiguration:")
    results = []
    threads = [threading.Thread(target=lambda: results.append(HomeConfiguration.instance)) for _ in range(20)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    check("20 luong cung lay instance deu ra cung mot doi tuong", all(r is results[0] for r in results))

    c1 = HomeConfiguration.instance
    c2 = HomeConfiguration.instance
    print(f"  ReferenceEquals(c1, c2): {c1 is c2}")
    check("c1 va c2 cung tham chieu mot doi tuong", c1 is c2)
    if c1 is not c2:
        raise Exception("Singleton implementation is incorrect.")
    check("Khong tao truc tiep HomeConfiguration() duoc", raises(TypeError, lambda: HomeConfiguration()))

    def make_subclass():
        class Sub(HomeConfiguration):
            pass
    check("Khong ke thua HomeConfiguration duoc (sealed)", raises(TypeError, make_subclass))

    # T4: Facade - chế độ đi làm. Đặt trạng thái ban đầu ngược lại để thấy rõ sự thay đổi
    facade = SmartHomeFacade(light, fan, door)
    print("\n[T4] Facade GoToWork():")
    light.turn_on()
    fan.turn_on()
    door.unlock()
    print("  -> goi go_to_work():")
    run_and_show(facade.go_to_work)
    check("Den tat", not light.is_on)
    check("Quat tat", not fan.is_on)
    check("Cua khoa", door.is_locked)

    # T5: Facade - chế độ đi ngủ
    print("\n[T5] Facade GoToSleep():")
    door.unlock()
    fan.turn_on()
    print("  -> goi go_to_sleep():")
    output = run_and_show(facade.go_to_sleep)
    check("Quat tat", not fan.is_on)
    check("Cua khoa", door.is_locked)
    check("Den bat", light.is_on)
    check("Thong bao muc sang dem 30% tu HomeConfiguration", "Night light level: 30%" in output)

    # T6: tiêu chí bổ sung - tiêm cấu hình giả (DI) và vẫn điều khiển riêng từng thiết bị
    print("\n[T6] Dependency Injection va dieu khien rieng le:")

    class FakeConfig:
        night_light_level = 55

    test_facade = SmartHomeFacade(light, fan, door, config=FakeConfig())
    output = run_and_show(test_facade.go_to_sleep)
    check("Facade dung cau hinh duoc tiem vao (55%) thay vi Singleton",
          "Night light level: 55%" in output and HomeConfiguration.instance.night_light_level == 30)
    light.turn_off()
    check("Client van dieu khien rieng tung thiet bi duoc", not light.is_on)

    print("\n=== HOAN TAT KIEM THU LAB 10 ===")
    print(f"Ket qua: {'TAT CA PASS' if failed == 0 else str(failed) + ' phep kiem tra FAIL'}")


if __name__ == "__main__":
    run_tests()
