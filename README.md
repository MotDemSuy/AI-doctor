# 🏥 Hệ Thống Chẩn Đoán Y Khoa AI (Local Ollama)

Ứng dụng quản lý hồ sơ bệnh nhân và chẩn đoán sơ bộ sử dụng AI (Llama 3) chạy trực tiếp trên máy tính cá nhân (Offline/Local), không lo giới hạn số lần gọi.

## 📋 Yêu Cầu Hệ Thống
- **Hệ điều hành**: Windows 10/11, macOS, hoặc Linux.
- **Python**: Phiên bản 3.9 trở lên.
- **RAM**: Tối thiểu 8GB (Khuyến nghị 16GB để chạy AI mượt hơn).
- **Dung lượng**: Trống khoảng 10GB (để tải Model AI).

---

## 🚀 Hướng Dẫn Cài Đặt

### Bước 1: Cài đặt Ollama & Tải Model AI
Đây là bộ não của hệ thống.
1.  Truy cập [ollama.com](https://ollama.com/) và tải bản cài đặt cho Windows.
2.  Cài đặt xong, mở **Command Prompt (CMD)** hoặc **PowerShell** và chạy lệnh sau để tải model:
    ```bash
    ollama pull llama3
    ```
    *(Chờ vài phút để tải khoảng 4.7GB)*.

### Bước 2: Cài Đặt Môi Trường Python
1.  Đảm bảo máy đã cài Python. Kiểm tra bằng cách mở CMD gõ: `python --version`.
2.  Cài đặt các thư viện cần thiết cho dự án:
    ```bash
    pip install streamlit langchain-ollama python-dotenv
    ```

---

## ▶️ Cách Sử Dụng

### 1. Khởi Động Ứng Dụng
- Chạy file **`run_web_app.bat`** (nếu có).
- Hoặc mở CMD tại thư mục dự án và gõ:
  ```bash
  streamlit run app.py
  ```

### 2. Quy Trình Khám Bệnh
1.  **Đăng Nhập/Đăng Ký**:
    -   Nhập số **CCCD** bên trái -> Bấm **"🔍 Tra Cứu"**.
    -   Nếu hồ sơ đã có: Thông tin sẽ hiện bên phải.
    -   Nếu chưa có: Tự nhập thông tin mới.
    -   Kiểm tra kỹ **Ngày Sinh**, **Cân Nặng**... -> Bấm **"💾 Lưu & Đăng Nhập"**.

2.  **Khám Bệnh**:
    -   Nhập triệu chứng vào ô trống (Ví dụ: *"Đau bụng dưới, buồn nôn..."*).
    -   Bấm **"Bắt Đầu Chẩn Đoán"**.
    -   AI sẽ đóng vai các bác sĩ chuyên khoa để phân tích và đưa ra kết luận.

3.  **Phân Tích Thể Trạng (BMI)**:
    -   Nhìn cột bên trái, dưới chỉ số BMI.
    -   Bấm nút **"🔍 Phân Tích & Lời Khuyên"**.
    -   AI sẽ tư vấn chế độ ăn uống và tập luyện dựa trên chiều cao/cân nặng của bạn.

---

## 🛠️ Xử Lý Lỗi Thường Gặp

- **Lỗi `Connection refused` hoặc AI không trả lời**:
  - Kiểm tra xem Ollama đã bật chưa (nhìn dưới thanh taskbar có icon con lạc đà).
  - Thử mở CMD lanh `ollama serve`.

- **Lỗi nhập ngày sinh đỏ lòm**:
  - Hãy nhập đúng định dạng **Ngày/Tháng/Năm** (Ví dụ: `20/05/1995`) rồi bấm **Enter**.
  - Hoặc bấm vào ô để chọn từ lịch.
