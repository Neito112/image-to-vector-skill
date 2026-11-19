---
name: image-to-vector
description: Universal skill & toolchain to convert ANY input image into 100% faithful SVG vector graphics. Activates as a dedicated Vector Studio when the repository link is pasted into chat, with a session-scoped output folder picker icon strictly isolated to that chat alone.
---

# 🚀 Universal Image-to-Vector Skill

This skill and its bundled toolchain are **100% universal and general-purpose**, designed to convert **ANY input image** into high-fidelity, clean, professional SVG vector graphics using Antigravity's built-in quota.

---

## 🔒 SESSION-SCOPED ACTIVATION & ISOLATION RULE (QUY TẮC CÔ LẬP KHUNG CHAT)

1. **Kích hoạt qua Link Repo (Activation via Repo Link)**:
   - Khi người dùng gửi/nhập link repository:
     `https://github.com/Neito112/image-to-vector-skill`
     vào bất kỳ khung chat nào của Antigravity, **khung chat đó lập tức biến thành Xưởng Tạo Ảnh Vector chuyên dụng**.
   - Agent trong phiên đó tự động kích hoạt session (`imageToVector.activateSession`), tải cấu hình và sẵn sàng tiếp nhận ảnh.

2. **Tuyệt đối không chèn nút sang các khung chat khác (Strict Session Isolation)**:
   - Icon chọn thư mục ảnh đầu ra `$(folder-opened)` và icon kéo thả ảnh `$(file-media)` trên Topbar được kiểm soát bởi context key:
     `"when": "imageToVector.sessionActive"`
   - **NGHIÊM CẤM HIỂN THỊ TOÀN CỤC**: Ở tất cả các khung chat khác, cửa sổ soạn thảo khác, các nút này **hoàn toàn vô hình 100%**. Chúng chỉ xuất hiện duy nhất tại phiên làm việc nơi link repo được gửi vào.

3. **Tùy ý chọn thư mục ảnh đầu ra**:
   - Người dùng có thể nhấp vào icon `$(folder-opened)` trên Topbar của phiên đó để chọn thư mục lưu ảnh tùy ý thông qua hộp thoại Windows File Picker.
   - Hoặc chỉ cần nói trong chat: `"Đổi thư mục xuất ảnh sang <đường_dẫn>"`, Agent sẽ cập nhật file `output_config.json` ngay lập tức.

---

## 🎯 Core Principles & Non-Negotiable Directives

1. **Search-First Icon & Graphic Strategy (Hạn chế tự vẽ hình bằng code)**:
   - Tra cứu và kế thừa các đoạn mã vector chuẩn từ các thư viện vector uy tín (Wikimedia, SVGRepo, ISO icons), sau đó tinh chỉnh toán học các điểm kiểm soát Bezier (`C`), góc xoay và nét cắt để đạt độ ăn khớp 100% với ảnh gốc.
2. **Strict Typography Metric Calibration (Bám sát bố cục & size chữ gốc)**:
   - Trích xuất pixel đo đạc trực tiếp từ ảnh gốc. Áp dụng chuẩn thuộc tính SVG `textLength` và `lengthAdjust="spacingAndGlyphs"` để cỡ chữ, độ co dãn (condensed), thanh kẻ phân cách và thanh gạch ngang đỏ bao phủ chính xác 100% bề rộng văn bản gốc.
3. **Chuẩn phông chữ thông thường (Standard SVG Text)**:
   - Luôn sử dụng thẻ `<text>` tiêu chuẩn cho chữ viết, không làm vỡ nét chữ thành pixel thô.
4. **Tuyệt đối không dùng Emoji thay thế hình vẽ**.
5. **Headless Chrome Rendering & Mở ngoài Windows**:
   - Render preview bằng Chrome Engine để ảnh xem trước mịn mượt 100% như file SVG thật.
   - Luôn mở file và thư mục trực tiếp ra ngoài Windows (File Explorer và trình duyệt mặc định).

---

## 📋 Hướng Dẫn Thực Thi

1. **Khi nhận link repo trong chat:**
   - Kích hoạt session vector riêng biệt cho chat đó:
     ```bash
     python scripts/set_output_dir.py
     ```
   - Xác nhận thư mục đầu ra hiện tại và chào đón người dùng kéo thả ảnh.
2. **Khi nhận ảnh đầu vào:**
   - Vector hóa theo thư mục đã cấu hình trong `output_config.json`.
   - Render ảnh preview bằng Headless Chrome:
     ```bash
     chrome --headless=new --screenshot=<out_preview.png> --window-size=1000,534 <out.svg>
     ```
   - Hiển thị ảnh preview ngay trong chat.
   - Gọi lệnh mở ngoài Windows:
     ```powershell
     Start-Process explorer.exe -ArgumentList "<output_folder>"
     Start-Process "<output_svg_path>"
     ```
