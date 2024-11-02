# Hướng Dẫn Sử Dụng Chương Trình Tìm Đường Đi Cho Nhân Vật

## Giới thiệu
Chương trình bao gồm hai file chính:
1. `main.py`: Xử lý logic tìm đường đi và tạo ra các file output cho từng file input.
2. `gui.py`: Giao diện trực quan giúp hiển thị đường đi của nhân vật dựa trên các output đã được tạo.

## Hướng dẫn sử dụng

### Bước 1: Chạy `main.py`
1. Để bắt đầu, **chạy file `main.py` trước** để xử lý các file input và tạo ra các file output tương ứng.
2. Đảm bảo cho `main.py` chạy xong hoàn toàn. Mỗi file input sẽ sinh ra một file output chứa đường đi nếu tìm được.

### Bước 2: Chạy `gui.py`
Sau khi chạy `main.py`, sử dụng `gui.py` để trực quan hóa đường đi:
1. Mở và chạy file `gui.py`.
2. Trong giao diện đồ họa:
   - **Chọn thuật toán** và **file input** cần sử dụng.
   - Nhấn **Start** để bắt đầu hiển thị đường đi.
   - Bạn có thể **dừng (Pause)** và **khởi động lại (Restart)** nếu muốn.

### Thêm file input mới
- Nếu bạn muốn chạy một file input mới không có sẵn, hãy thêm nó vào thư mục `input` hoặc thay thế nội dung của file input bất kỳ.
- Sau đó, **chạy lại `main.py`** để chương trình xử lý và tìm đường đi cho file input mới của bạn.
- Tiếp tục sử dụng `gui.py` như hướng dẫn ở trên để xem đường đi.

### Lưu ý
- Các input không có kết quả sẽ không tạo ra file output tương ứng.
- Trong GUI, nếu không tìm thấy output, chương trình sẽ thông báo.
