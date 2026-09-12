# Kết quả kiểm thử thực tế

Thời điểm: 2026-09-12T06:47:23.957481+00:00. Seed cố định: 13060102.

Oracle dùng Python stdlib: `sorted`, `bisect`, công thức đếm cặp; số dịch chèn bằng số nghịch thế. Không lấy đáp án từ mã lời giải.

| Ngôn ngữ | Bài | Đạt | Lỗi | Trạng thái |
|---|---|---:|---:|---|
| Python | bai01 | 39 | 0 | passed |
| Python | bai02 | 39 | 0 | passed |
| Python | bai03 | 44 | 0 | passed |
| Python | bai04 | 47 | 0 | passed |
| C++17 | bai01 | 0 | 39 | failed |
| C++17 | bai02 | 0 | 39 | failed |
| C++17 | bai03 | 0 | 44 | failed |
| C++17 | bai04 | 0 | 47 | failed |
| Julia | bai01 | 0 | 39 | failed |
| Julia | bai02 | 0 | 39 | failed |
| Julia | bai03 | 0 | 44 | failed |
| Julia | bai04 | 0 | 47 | failed |

Tổng: **169 ca đạt; 338 ca lỗi**. Số ngôn ngữ bỏ qua: 0.

Các ca gồm mẫu, rỗng, một phần tử, trùng, âm, tăng/giảm, biên tìm kiếm, dữ liệu chưa sắp xếp, k=1/k=n/k=2, hòa phiếu, hòa khoảng cách khác thứ tự ID và đầu vào kNN không hợp lệ. Có thêm 30 ca ngẫu nhiên cố định cho mỗi bài và mỗi ngôn ngữ được chạy.

Thời gian trong JSON là thời gian kiểm thử, không phải benchmark thuật toán. Khi chạy Julia theo lô, thời gian từng ca hợp lệ ghi 0 và thời gian cả lô được lưu riêng. Ngôn ngữ bỏ qua chưa được kiểm chứng lúc chạy.

Runtime Python: `C:\Users\tai20\AppData\Local\Python\pythoncore-3.14-64\python.exe`.
Phiên bản: `Python 3.14.7`.

Runtime C++17: `C:\msys64\ucrt64\bin\g++.EXE`.
Phiên bản: `g++.EXE (Rev5, Built by MSYS2 project) 16.1.0`.

Lỗi biên dịch C++17/bai01:
```text
Source missing: C:\ctdl\thuc_hanh_buoi_1\code\cpp\bai01.cpp
```

Lỗi biên dịch C++17/bai02:
```text
Source missing: C:\ctdl\thuc_hanh_buoi_1\code\cpp\bai02.cpp
```

Lỗi biên dịch C++17/bai03:
```text
Source missing: C:\ctdl\thuc_hanh_buoi_1\code\cpp\bai03.cpp
```

Lỗi biên dịch C++17/bai04:
```text
Source missing: C:\ctdl\thuc_hanh_buoi_1\code\cpp\bai04.cpp
```

Runtime Julia: `C:\Users\tai20\AppData\Local\Microsoft\WindowsApps\julia.EXE`.
Phiên bản: `julia version 1.12.6`.

Lỗi biên dịch Julia/bai01:
```text
Source missing: C:\ctdl\thuc_hanh_buoi_1\code\julia\bai01.jl
```

Lỗi biên dịch Julia/bai02:
```text
Source missing: C:\ctdl\thuc_hanh_buoi_1\code\julia\bai02.jl
```

Lỗi biên dịch Julia/bai03:
```text
Source missing: C:\ctdl\thuc_hanh_buoi_1\code\julia\bai03.jl
```

Lỗi biên dịch Julia/bai04:
```text
Source missing: C:\ctdl\thuc_hanh_buoi_1\code\julia\bai04.jl
```
