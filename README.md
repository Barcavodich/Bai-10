# Bài thực hành 10: Smart Home Mini

Ứng dụng điều khiển nhà thông minh với đèn (`SmartLight`), quạt (`SmartFan`), cửa (`SmartDoor`), dùng ba pattern Factory, Singleton, Facade.

Chạy: `python main.py` (kiểm thử T1 đến T6, mỗi phép kiểm tra in `PASS`/`FAIL`).

## Cấu trúc

| File | Nội dung |
|---|---|
| `devices.py` | `IDevice`, `ILockable`, `SmartLight`, `SmartFan`, `SmartDoor` |
| `factory.py` | `DeviceFactory` |
| `configuration.py` | `HomeConfiguration` |
| `facade.py` | `SmartHomeFacade` |
| `main.py` | Kiểm thử T1 đến T6 |

## Vị trí sử dụng, lợi ích, hạn chế

| Pattern | Vị trí | Lợi ích | 
|---|---|---|
| Factory | `DeviceFactory.create(type, name)` | Client chỉ biết `IDevice` và chuỗi loại, không gọi constructor của lớp cụ thể |
| Singleton | `HomeConfiguration.instance` | Cả ứng dụng dùng chung một cấu hình (tên nhà, mức đèn ngủ) |
| Facade | `SmartHomeFacade.go_to_work()`, `go_to_sleep()` | Một lệnh thay cho nhiều lệnh thiết bị; client vẫn điều khiển riêng từng thiết bị khi cần |

**Hạn chế của thiết kế:** `DeviceFactory` dùng `if/elif` theo chuỗi, nên thêm loại thiết bị mới vẫn phải sửa factory (trái nguyên tắc đóng/mở). `SmartHomeFacade` mặc định đọc thẳng `HomeConfiguration.instance` nên bị gắn với trạng thái toàn cục; để khắc phục, facade nhận thêm tham số `config` tùy chọn (Dependency Injection) và `main.py` (T6) dùng cấu hình giả để kiểm thử.

## Phần C: Factory

- **Che giấu điều gì?** Che việc chọn và khởi tạo lớp cụ thể (`SmartLight`, `SmartFan`, `SmartDoor`) từ chuỗi loại; client chỉ nhận `IDevice`.
- **Thêm `SmartCamera` phải sửa gì?** Thêm lớp `SmartCamera` trong `devices.py` và một nhánh `"camera"` trong `DeviceFactory`. Client, `SmartHomeFacade` và các thiết bị cũ không phải sửa.

## Phần D: Singleton

- **Constructor:** C# để `private`. Python không có `private` thật, nên `HomeConfiguration()` gọi trực tiếp sẽ ném `TypeError`; chỉ thuộc tính `instance` mới tạo được thể hiện (qua khóa nội bộ).
- **Vì sao `sealed`?** Lớp con có thể tạo thêm thể hiện thứ hai, phá cam kết "chỉ một". Bản Python dùng `@final` và `__init_subclass__` ném lỗi khi bị kế thừa.
- **Khó khăn khi unit test:** trạng thái toàn cục dùng chung giữa các test (test này đổi `night_light_level` sẽ ảnh hưởng test sau) và khó thay bằng đối tượng giả.
- **Có .NET DI `AddSingleton` thì còn cần tự cài Singleton không?** Không nhất thiết. Container giữ đúng một thể hiện và tiêm vào nơi cần, lớp vẫn có constructor public bình thường, dễ thay bằng đối tượng giả khi test.

## Phần G: Câu hỏi

1. **Factory che giấu quyết định thiết kế nào?** Quyết định "loại chuỗi này ứng với lớp cụ thể nào và khởi tạo ra sao".
2. **Singleton bảo đảm gì, rủi ro gì?** Bảo đảm chỉ có một thể hiện và có điểm truy cập chung. Rủi ro: trạng thái toàn cục ẩn, phụ thuộc ngầm giữa các lớp, khó kiểm thử, dễ sai khi nhiều luồng nếu cài không an toàn.
3. **Facade khác Factory ở mục đích chính?** Factory giải quyết việc *tạo* đối tượng (ai tạo, tạo loại nào); Facade giải quyết việc *dùng* nhiều đối tượng (gom nhiều thao tác thành giao diện đơn giản).
4. **Nếu bỏ `SmartHomeFacade`, client phải biết thêm gì?** Phải biết có những thiết bị nào, thứ tự thao tác của từng chế độ (tắt đèn, tắt quạt, khóa cửa), thiết bị nào khóa được, và phải tự đọc `HomeConfiguration` để lấy mức sáng ban đêm. Mỗi nơi cần chế độ "Đi làm" lại phải lặp lại chuỗi lệnh đó.
