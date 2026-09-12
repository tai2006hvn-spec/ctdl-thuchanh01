# Chạy bộ kiểm thử

Tại thư mục gói học liệu:

```text
python tests/verify.py
```

Trên Linux/macOS có thể dùng `python3` thay `python`. Script chỉ dùng thư viện chuẩn Python, tìm `g++` hoặc `clang++` và `julia` trong PATH. Có thể cung cấp vị trí đã cài đặt:

```text
python tests/verify.py --cpp C:/msys64/ucrt64/bin/g++.exe --julia C:/duong-dan/julia.exe
```

Đường dẫn trên là ví dụ; thay bằng đường dẫn thật trên máy. Script không tự tải hoặc cài phần mềm. Ngôn ngữ không có runtime được ghi **skipped**, không được tính là đã chạy đạt.

Mỗi bài có 30 ca ngẫu nhiên với seed cố định, cộng các ca mẫu và ca biên. Các đáp án được tính độc lập bằng công thức, `sorted` và `bisect`, không gọi hàm trong mã lời giải. Bài 02 kiểm tra cả số so sánh và số dịch; bài 03 kiểm tra số bước dò và xử lý mảng chưa sắp xếp; bài 04 kiểm tra thứ tự ID khi cùng khoảng cách, hòa phiếu và dữ liệu không hợp lệ.

Hai báo cáo được cập nhật sau mỗi lần chạy:

- `verification.md`: bảng kết quả dễ đọc.
- `verification.json`: chi tiết từng ca; nếu lỗi có dữ liệu vào, đầu ra mong đợi, đầu ra thật và mã thoát.

Chương trình trả mã thoát 1 nếu có lỗi kiểm thử hoặc biên dịch; mã 0 khi các ngôn ngữ đã chạy đều đạt. Luôn đọc mục ngôn ngữ bị bỏ qua trong báo cáo để biết phần nào chưa thực thi.

Nếu có Julia, các ca hợp lệ của mỗi bài chạy chung một tiến trình qua `julia_batch.jl`: tải nguồn gốc một lần rồi gọi lại `main()`, giữ nguyên tệp lời giải. Các ca sai dữ liệu chạy trong tiến trình riêng để kiểm tra `exit(1)`. Bộ trợ giúp Julia này chưa được thực thi khi máy không có Julia; báo cáo ghi rõ trạng thái tương ứng.

Thư mục `build/` là đầu ra tạm do bộ kiểm thử tạo, gồm chương trình C++ đã biên dịch và tệp cho kiểm thử Julia. Không cần phát kèm thư mục này cho sinh viên. Kết quả thời gian là thời gian chạy kiểm thử, không phải đo hiệu năng thuật toán.
