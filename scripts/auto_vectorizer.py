import os
import sys
import subprocess
import cv2
import numpy as np

def extract_dominant_colors(image, k=4):
    pixels = image.reshape((-1, 3)).astype(np.float32)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
    _, labels, centers = cv2.kmeans(pixels, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    
    unique, counts = np.unique(labels, return_counts=True)
    sorted_indices = np.argsort(-counts)
    
    hex_colors = []
    bgr_colors = []
    for idx in sorted_indices:
        b, g, r = centers[idx].astype(int)
        hex_colors.append(f"#{r:02x}{g:02x}{b:02x}")
        bgr_colors.append((int(b), int(g), int(r)))
    return hex_colors, bgr_colors

def image_to_svg_paths(binary_mask, scale=1.0, epsilon_ratio=0.003, min_area=25):
    cnts, hier = cv2.findContours(binary_mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_TC89_KCOS)
    if not cnts or hier is None:
        return []

    paths = []
    for c in cnts:
        area = cv2.contourArea(c)
        if area < min_area:
            continue

        epsilon = epsilon_ratio * cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, epsilon, True)
        pts = approx.reshape(-1, 2)
        if len(pts) < 3:
            continue

        scaled_pts = pts * scale
        d = [f"M {scaled_pts[0][0]:.2f} {scaled_pts[0][1]:.2f}"]
        for p in scaled_pts[1:]:
            d.append(f"L {p[0]:.2f} {p[1]:.2f}")
        d.append("Z")
        paths.append(" ".join(d))

    return paths

def render_svg_to_png(svg_path, output_png_path, width=1000, height=534):
    """
    Renders SVG to PNG using Headless Chrome engine for 100% faithful, subpixel antialiased preview.
    """
    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe")
    ]
    chrome_bin = None
    for p in chrome_paths:
        if os.path.exists(p):
            chrome_bin = p
            break

    if chrome_bin:
        abs_svg = os.path.abspath(svg_path).replace("\\", "/")
        cmd = [
            chrome_bin,
            "--headless=new",
            "--disable-gpu",
            "--no-sandbox",
            f"--screenshot={os.path.abspath(output_png_path)}",
            f"--window-size={width},{height}",
            f"file:///{abs_svg}"
        ]
        res = subprocess.run(cmd, capture_output=True)
        if res.returncode == 0 and os.path.exists(output_png_path):
            print(f"[+] Rendered subpixel-perfect preview via Chrome engine: {output_png_path}")
            return True

    print("[-] Headless Chrome not available for rendering preview.")
    return False

def vectorize_general_image(input_image_path, output_svg_path, target_width=1000):
    if not os.path.exists(input_image_path):
        raise FileNotFoundError(f"Input image not found: {input_image_path}")

    img = cv2.imread(input_image_path)
    if img is None:
        raise ValueError(f"Could not load image: {input_image_path}")

    h, w, _ = img.shape
    aspect = w / h
    target_height = int(target_width / aspect)
    scale = target_width / w

    print(f"[*] Processing {input_image_path}: Original size {w}x{h} -> Scaled {target_width}x{target_height}")

    hex_palette, _ = extract_dominant_colors(img, k=5)
    bg_hex = hex_palette[0]

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    layers = []
    
    # Layer 1: Dark foreground elements
    _, dark_mask = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)
    dark_paths = image_to_svg_paths(dark_mask, scale=scale, epsilon_ratio=0.0025, min_area=20)
    if dark_paths:
        layers.append({"fill": "#1a202c", "paths": dark_paths, "name": "dark_elements"})

    # Layer 2: Colored / saturated accents
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    sat = hsv[:, :, 1]
    _, sat_mask = cv2.threshold(sat, 80, 255, cv2.THRESH_BINARY)
    color_accent_mask = cv2.bitwise_and(sat_mask, cv2.bitwise_not(dark_mask))
    accent_paths = image_to_svg_paths(color_accent_mask, scale=scale, epsilon_ratio=0.003, min_area=30)
    if accent_paths:
        accent_hex = hex_palette[1] if len(hex_palette) > 1 else "#d32027"
        layers.append({"fill": accent_hex, "paths": accent_paths, "name": "color_accents"})

    svg_lines = [
        f'<svg width="{target_width}" height="{target_height}" viewBox="0 0 {target_width} {target_height}" xmlns="http://www.w3.org/2000/svg">',
        '  <!-- Background Canvas -->',
        f'  <rect width="{target_width}" height="{target_height}" rx="14" ry="14" fill="{bg_hex}" />'
    ]

    for layer in layers:
        svg_lines.append(f'  <!-- Layer: {layer["name"]} -->')
        svg_lines.append(f'  <g id="{layer["name"]}" fill="{layer["fill"]}">')
        for p in layer["paths"]:
            svg_lines.append(f'    <path d="{p}" fill-rule="evenodd" />')
        svg_lines.append('  </g>')

    svg_lines.append('</svg>')

    os.makedirs(os.path.dirname(os.path.abspath(output_svg_path)), exist_ok=True)
    with open(output_svg_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_lines))
    print(f"[+] Exported Vector SVG: {output_svg_path}")

    # Generate preview PNG using Chrome rendering
    base_name, _ = os.path.splitext(output_svg_path)
    preview_png_path = f"{base_name}_preview.png"
    render_svg_to_png(output_svg_path, preview_png_path, target_width, target_height)

    return output_svg_path, preview_png_path

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python auto_vectorizer.py <input_image> [output_svg]")
        sys.exit(1)
    inp = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else "output.svg"
    vectorize_general_image(inp, out)
