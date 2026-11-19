import os
import sys
import json
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox

CONFIG_PATH = r'd:\ComfyUI\svg\output_config.json'

def get_current_dir():
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if data.get('outputDir') and os.path.exists(data['outputDir']):
                    return data['outputDir']
        except Exception:
            pass
    return r'd:\ComfyUI\svg'

def set_current_dir(new_dir):
    os.makedirs(new_dir, exist_ok=True)
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump({'outputDir': new_dir}, f, indent=2)

def main():
    root = tk.Tk()
    root.title("Image to Vector - Quick Toolbar")
    root.geometry("520x65+400+100")
    root.attributes("-topmost", True)
    root.configure(bg="#1a202c")
    root.resizable(False, False)

    # Styling
    font_main = ("Segoe UI", 9)
    font_bold = ("Segoe UI", 9, "bold")

    frame = tk.Frame(root, bg="#1a202c", padx=10, pady=8)
    frame.pack(fill=tk.BOTH, expand=True)

    # Row 1: Current Dir Label
    lbl_dir = tk.Label(frame, text=f"📂 Output: {get_current_dir()}", bg="#1a202c", fg="#e2e8f0", font=font_main, anchor="w")
    lbl_dir.pack(fill=tk.X, side=tk.TOP, pady=(0, 5))

    # Row 2: Buttons
    btn_frame = tk.Frame(frame, bg="#1a202c")
    btn_frame.pack(fill=tk.X, side=tk.TOP)

    def on_choose_dir():
        initial = get_current_dir()
        selected = filedialog.askdirectory(initialdir=initial, title="Chọn thư mục xuất ảnh Vector")
        if selected:
            selected_norm = os.path.normpath(selected)
            set_current_dir(selected_norm)
            lbl_dir.config(text=f"📂 Output: {selected_norm}")
            messagebox.showinfo("Thành công", f"Đã đổi thư mục xuất ảnh vector sang:\n{selected_norm}")

    def on_choose_image():
        selected_img = filedialog.askopenfilename(
            title="Chọn ảnh cần vector hóa",
            filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.webp;*.bmp")]
        )
        if selected_img:
            out_dir = get_current_dir()
            out_svg = os.path.join(out_dir, "output_vector.svg")
            script = r"d:\ComfyUI\svg\image-to-vector-skill-repo\scripts\auto_vectorizer.py"
            cmd = f'python "{script}" "{selected_img}" "{out_svg}"'
            subprocess.Popen(cmd, shell=True)
            messagebox.showinfo("Đang xử lý", f"Đang vector hóa ảnh!\nKết quả sẽ được lưu vào:\n{out_dir}")

    def on_open_folder():
        cur = get_current_dir()
        subprocess.Popen(f'explorer.exe "{cur}"', shell=True)

    btn_dir = tk.Button(btn_frame, text="📂 Chọn Thư Mục Ra", command=on_choose_dir, bg="#2563eb", fg="white", font=font_bold, relief=tk.FLAT, padx=8, pady=2, cursor="hand2")
    btn_dir.pack(side=tk.LEFT, padx=(0, 6))

    btn_img = tk.Button(btn_frame, text="🖼️ Chọn Ảnh Cần Vẽ", command=on_choose_image, bg="#059669", fg="white", font=font_bold, relief=tk.FLAT, padx=8, pady=2, cursor="hand2")
    btn_img.pack(side=tk.LEFT, padx=(0, 6))

    btn_open = tk.Button(btn_frame, text="↗ Mở Folder", command=on_open_folder, bg="#475569", fg="white", font=font_main, relief=tk.FLAT, padx=8, pady=2, cursor="hand2")
    btn_open.pack(side=tk.LEFT)

    root.mainloop()

if __name__ == "__main__":
    main()
