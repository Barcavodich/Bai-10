# /*********************
# Mã sinh viên: 202418900
# Họ tên: Nguyễn Đăng Hiếu
# *********************/

from factory import DeviceFactory
from configuration import HomeConfiguration
from facade import SmartHomeFacade

def run_tests():
    print("=== BAT DAU KIEM THU LAB 10: DESIGN PATTERNS ===")

    # T1: Tao light, fan, door qua Factory
    print("\n[T1] Test Factory Creation:")
    light = DeviceFactory.create("light", "Living room light")
    fan = DeviceFactory.create("fan", "Living room fan")
    door = DeviceFactory.create("door", "Main door")
    print(f"Created: {type(light).__name__}, {type(fan).__name__}, {type(door).__name__}")

    # T2: Tao loai khong ho tro (phai sinh ArgumentException/ValueError)
    print("\n[T2] Test Unsupported Device Type:")
    try:
        DeviceFactory.create("camera", "Security camera")
    except ValueError as e:
        print(f"Caught expected exception: {e}")

    # T3: Kiem tra Singleton HomeConfiguration
    print("\n[T3] Test Singleton Configuration:")
    c1 = HomeConfiguration.instance
    c2 = HomeConfiguration.instance
    is_same = (c1 is c2)
    print(f"ReferenceEquals(c1, c2): {is_same}")
    if not is_same:
        raise Exception("Singleton implementation is incorrect.")

    # T4 & T5: Kiem tra Facade (GoToWork & GoToSleep)
    facade = SmartHomeFacade(light, fan, door)

    print("\n[T4] Test Facade GoToWork():")
    facade.go_to_work()

    print("\n[T5] Test Facade GoToSleep():")
    facade.go_to_sleep()

    print("\n=== HOAN TAT KIEM THU LAB 10 ===")

if __name__ == "__main__":
    run_tests()