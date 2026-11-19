# 🎯 Universal Image-to-Vector Skill & Toolchain

A standardized, production-grade skill and automated toolchain for converting **ANY input image** into **100% faithful, scalable SVG vector graphics**.

Designed for **Antigravity**: transforms any chat into a dedicated Vector Studio when the repository link is pasted, with a session-scoped output folder picker icon strictly isolated to that chat alone.

---

## 🔒 Session-Scoped Activation (Cô lập theo từng khung chat)

- **Kích hoạt qua Link Repo:** Chỉ cần nhập link repo vào khung chat, khung chat đó lập tức biến thành Xưởng Tạo Ảnh Vector.
- **Cách ly tuyệt đối:** Icon chọn thư mục đầu ra `$(folder-opened)` và icon kéo thả ảnh **chỉ xuất hiện duy nhất ở khung chat đã nhận link repo**. Tuyệt đối không xuất hiện ở các khung chat khác!
- **Tùy chọn thư mục đầu ra:** Tùy ý chọn thư mục lưu ảnh vector qua icon hoặc ra lệnh trực tiếp trong chat.
- **Sử dụng Quota Antigravity có sẵn:** Tận dụng 100% quota Gemini trong Antigravity, hoàn toàn miễn phí không cần API key ngoài.

---

## 🚀 Quick Setup (Cho Người & Agent)

👉 Xem chi tiết tại [SETUP.md](./SETUP.md)

1. Dán link repo vào khung chat Antigravity:
   ```text
   https://github.com/Neito112/image-to-vector-skill
   ```
2. Icon chọn thư mục đầu ra xuất hiện trên Topbar của khung chat đó.
3. Kéo thả ảnh vào và nhận file vector SVG cực mịn nét kèm ảnh preview tức thì!

---

## 📁 Repository Structure

```
├── SETUP.md                  # Hướng dẫn chi tiết cho cả Người và Agent
├── SKILL.md                  # Quy chuẩn SOP và hướng dẫn thực thi chuẩn
├── install.bat               # Script cài đặt tự động 1-click cho Windows
├── output_config.json        # File lưu cấu hình thư mục đầu ra
├── extension/                # VS Code / Antigravity Topbar Extension (Session-scoped)
│   ├── package.json          # Khóa nút bấm bằng context imageToVector.sessionActive
│   └── extension.js          # Logic chọn thư mục và Webview kéo thả ảnh
├── scripts/
│   ├── auto_vectorizer.py    # Pipeline vector tự động đa lớp & Chrome preview
│   ├── set_output_dir.py     # Script đổi thư mục đầu ra linh hoạt
│   ├── vector_tracer.py      # Trích xuất contour thành thẻ <path> mượt mà
│   └── validator.py          # Kiểm định chất lượng (loại bỏ 100% emoji)
└── examples/
    └── no_shoes_sign.svg     # File vector mẫu đạt chuẩn 100%
```
