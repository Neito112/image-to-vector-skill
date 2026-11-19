# 🛠️ Hướng Dẫn Cài Đặt (Setup Guide)

Tài liệu này được biên soạn chuẩn hóa để **Người dùng (Humans)** và **Trí tuệ nhân tạo (AI Agents)** đều có thể đọc, hiểu và tự động thiết lập 100%.

---

## 👤 PHẦN 1: HƯỚNG DẪN DÀNH CHO NGƯỜI DÙNG (HUMAN GUIDE)

### 1. Cài đặt siêu tốc (1 cú nhấp chuột)
1. Mở thư mục repository `image-to-vector-skill`.
2. Double-click chạy file **`install.bat`**.
3. Khởi động lại ứng dụng **Antigravity**.

### 2. Vị trí nút trên Topbar và Cách sử dụng
- **Vị trí nút:** Nhìn lên góc trên bên phải của thanh công cụ Topbar (khu vực Editor Title Bar), bạn sẽ thấy một nút biểu tượng ảnh: `$(file-media)` mang tên **"Vectorize Image (Drag & Drop)"**.
- **Cách dùng:**
  1. Nhấp vào nút **Vectorize Image** trên Topbar.
  2. Một bảng điều khiển hiện đại sẽ mở ra với vùng kéo thả: **"Kéo & thả ảnh vào đây"**.
  3. Kéo bất kỳ file ảnh nào (`.jpg`, `.png`, `.webp`, `.bmp`) từ máy tính thả vào khung.
  4. Hệ thống sẽ tự động thực hiện vẽ lại vector, hiển thị bản preview trực tiếp kèm 2 nút bấm:
     - 📄 **Mở file SVG ngoài Windows**
     - 📂 **Mở thư mục ngoài Windows**

### 3. Về Quota sử dụng trong Antigravity
- **Sử dụng 100% Quota Antigravity có sẵn:** Toàn bộ quá trình phân tích hình học, xử lý nét vẽ và tối ưu hóa đều chạy trực tiếp thông qua môi trường và model Gemini (3.8 Flash / Pro) đã đăng nhập trong Antigravity của bạn.
- **Không tốn thêm chi phí:** Không yêu cầu nhập thêm thẻ tín dụng hay API key trả phí của bên thứ ba.

---

## 🤖 PHẦN 2: HƯỚNG DẪN DÀNH CHO AI AGENT (AGENT SPECIFICATION)

When an AI Agent is tasked with setting up or executing this capability, follow this exact automated protocol:

### 1. Discovery & Extension Deployment
- **Extension Target Directory:**
  - Windows: `%USERPROFILE%\.vscode\extensions\image-to-vector-button\`
  - Linux/macOS: `~/.vscode/extensions/image-to-vector-button/`
- **Action:** Copy the contents of `./extension/` directly into the extension target directory.

### 2. Skill Registration
- **Global Skill Directory:**
  - Windows: `%USERPROFILE%\.gemini\skills\image-to-vector\`
  - Linux/macOS: `~/.gemini/skills/image-to-vector/`
- **Action:** Copy `SKILL.md` and `./scripts/` to the skill directory so the Antigravity language server registers the `/image-to-vector` slash command and autonomous capability.

### 3. Execution Protocol via CLI / Script
When an image is provided:
```bash
python scripts/auto_vectorizer.py <input_image_path> <output_svg_path>
```
To validate compliance:
```bash
python scripts/validator.py <output_svg_path>
```

### 4. Headless Preview & External Launch
To render the subpixel preview without raster distortion:
```bash
chrome --headless=new --disable-gpu --screenshot=<preview.png> --window-size=1000,534 <file.svg>
```
To launch externally in Windows:
```powershell
Start-Process explorer.exe -ArgumentList "<output_folder>"
Start-Process "<output_file.svg>"
```
