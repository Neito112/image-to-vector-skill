# 🎯 Universal Image-to-Vector Skill & Toolchain

A standardized, production-grade skill and automated toolchain for converting **ANY input image** into **100% faithful, scalable SVG vector graphics**.

Includes a **Topbar Button for Antigravity (Drag & Drop)** utilizing your built-in Antigravity AI quota!

---

## 🌟 Highlights

- **Topbar Button & Drag-and-Drop**: 1-click button located right on the Antigravity topbar. Simply drag and drop any image into the panel.
- **Built-in Antigravity Quota**: Runs directly using the logged-in Gemini models in Antigravity. Zero external API keys needed.
- **Pure Vector Drawings**: Graphical elements are traced or retrieved from standard open SVG libraries, then fine-tuned with smooth Bezier curves. **Strictly zero emojis or character approximations.**
- **Accurate Typography**: Standard SVG `<text>` elements with precise `textLength` and `lengthAdjust` metrics bám sát reference photos.
- **Pixel-Perfect Preview**: Rendered with the Chrome Headless engine for true subpixel antialiasing.
- **Native External Launch**: 1-click buttons to open the SVG in your default external browser and folder in Windows Explorer.

---

## 🚀 Quick Setup (Cho Người & Agent)

👉 Xem chi tiết tại [SETUP.md](./SETUP.md)

### Dành cho Người dùng (1 click):
Chạy file **`install.bat`** rồi khởi động lại Antigravity. Nút **`Vectorize Image`** sẽ xuất hiện trên thanh Topbar (khu vực Editor Title Bar bên phải).

### Dành cho AI Agent:
Tự động copy `extension/` vào `~/.vscode/extensions/image-to-vector-button/` và `SKILL.md` vào `~/.gemini/skills/image-to-vector/`.

---

## 📁 Repository Structure

```
├── SETUP.md                  # Hướng dẫn chi tiết cho cả Người và Agent
├── SKILL.md                  # Quy chuẩn SOP và hướng dẫn thực thi chuẩn
├── install.bat               # Script cài đặt tự động 1-click cho Windows
├── extension/                # VS Code / Antigravity Topbar Extension
│   ├── package.json          # Đăng ký nút Topbar (editor/title navigation)
│   └── extension.js          # Webview Panel kéo thả ảnh và xử lý
├── scripts/
│   ├── auto_vectorizer.py    # Pipeline vector tự động đa lớp & Chrome preview
│   ├── vector_tracer.py      # Trích xuất contour thành thẻ <path> mượt mà
│   └── validator.py          # Kiểm định chất lượng (loại bỏ 100% emoji)
└── examples/
    └── no_shoes_sign.svg     # File vector mẫu đạt chuẩn 100%
```
