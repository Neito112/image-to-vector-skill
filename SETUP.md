# 🛠️ Hướng Dẫn Cài Đặt & Vận Hành (Setup Guide)

Tài liệu này được biên soạn chuẩn hóa để **Người dùng (Humans)** và **Trí tuệ nhân tạo (AI Agents)** đều có thể đọc, hiểu và tự động thiết lập 100%.

---

## 🔒 NGUYÊN TẮC QUAN TRỌNG: KÍCH HOẠT THEO KHUNG CHAT (SESSION-SCOPED)

> [!IMPORTANT]
> **Tuyệt đối cô lập:** Nút chọn thư mục đầu ra và nút công cụ vector **CHỈ TỒN TẠI DUY NHẤT** ở khung chat nào được nhập link repo. **Tuyệt đối KHÔNG xuất hiện hay ảnh hưởng đến bất kỳ khung chat hoặc cửa sổ soạn thảo nào khác!**

---

## 👤 PHẦN 1: DÀNH CHO NGƯỜI DÙNG (HUMAN GUIDE)

### 1. Cách kích hoạt Xưởng Tạo Ảnh Vector trong 3 giây
1. Mở bất kỳ khung chat nào trong Antigravity.
2. Gửi link repository này vào khung chat:
   ```text
   https://github.com/Neito112/image-to-vector-skill
   ```
3. Khung chat đó sẽ **ngay lập tức biến thành Xưởng Tạo Ảnh Vector chuyên dụng** cho phiên làm việc của bạn.

### 2. Tùy ý chọn thư mục ảnh đầu ra
- Ngay khi phiên làm việc được kích hoạt, một icon thư mục `$(folder-opened)` (**Chọn thư mục ảnh đầu ra**) sẽ xuất hiện trên Topbar/thanh công cụ riêng của khung chat đó.
- Nhấp vào icon này để mở hộp thoại Windows và chọn bất kỳ thư mục nào trên máy tính bạn muốn lưu ảnh vector.
- Bạn cũng có thể ra lệnh trực tiếp trong chat: *"Đổi thư mục lưu sang C:\MyVectors"*.

### 3. Kéo thả ảnh & Sử dụng Quota Antigravity
- Kéo thả bất kỳ ảnh nào vào khung chat hoặc nhấp icon `$(file-media)` trên Topbar để thả ảnh.
- Toàn bộ quá trình xử lý sử dụng **100% Quota có sẵn của Antigravity (Gemini 3.8 Flash/Pro)**, không tốn thêm bất kỳ chi phí hay API key nào.

---

## 🤖 PHẦN 2: DÀNH CHO AI AGENT (AGENT SPECIFICATION)

When an AI Agent is tasked with configuring or operating this skill, enforce these exact system rules:

### 1. Detection & Session Activation
Whenever the user inputs the repository URL in the current conversation:
- Identify the session context as an active **Vector Studio Session**.
- Run `scripts/set_output_dir.py` to inspect or initialize the target output directory.
- Execute context activation in the extension host:
  ```json
  "imageToVector.sessionActive": true
  ```
- **Ensure Scope Isolation**: Do NOT declare or inject the navigation buttons globally without the `"when": "imageToVector.sessionActive"` filter guard.

### 2. Directory Routing
- Read the active output directory from `output_config.json`.
- When generating SVG vectors:
  ```bash
  python scripts/auto_vectorizer.py <input_image> <target_output_dir/output.svg>
  ```
- Render preview via Chrome:
  ```bash
  chrome --headless=new --screenshot=<output_preview.png> --window-size=1000,534 <output.svg>
  ```

### 3. Delivery
- Render the preview image inline in chat: `![Preview](file:///...)`
- Open externally on Windows:
  ```powershell
  Start-Process explorer.exe -ArgumentList "<target_output_dir>"
  Start-Process "<output_svg_path>"
  ```
