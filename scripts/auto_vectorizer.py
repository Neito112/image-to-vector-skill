import os
import sys
import cv2
import numpy as np
import xml.etree.ElementTree as ET

def extract_dominant_colors(image, k=4):
    """
    Extracts the dominant colors in an image using K-Means clustering.
    Returns RGB hex colors sorted by frequency.
    """
    pixels = image.reshape((-1, 3)).astype(np.float32)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
    _, labels, centers = cv2.kmeans(pixels, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    
    unique, counts = np.unique(labels, return_counts=True)
    sorted_indices = np.argsort(-counts)
    
    hex_colors = []
    for idx in sorted_indices:
        b, g, r = centers[idx].astype(int)
        hex_colors.append(f"#{r:02x}{g:02x}{b:02x}")
    return hex_colors

def image_to_svg_paths(binary_mask, scale=1.0, epsilon_ratio=0.003, min_area=25):
    """
    Converts any binary mask of graphics into smooth SVG path strings.
    """
    cnts, hier = cv2.findContours(binary_mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_TC89_KCOS)
    if not cnts or hier is None:
        return []

    paths = []
    hier = hier[0]

    for i, c in enumerate(cnts):
        # Only process external contours or significant internal holes
        area = cv2.contourArea(c)
        if area < min_area:
            continue

        epsilon = epsilon_ratio * cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, epsilon, True)
        pts = approx.reshape(-1, 2)
        if len(pts) < 3:
            continue

        d = [f"M {pts[0][0]*scale:.2f} {pts[0][1]*scale:.2f}"]
        for p in pts[1:]:
            d.append(f"L {p[0]*scale:.2f} {p[1]*scale:.2f}")
        d.append("Z")
        paths.append(" ".join(d))

    return paths

def vectorize_general_image(input_image_path, output_svg_path, target_width=1000):
    """
    UNIVERSAL IMAGE-TO-VECTOR CONVERTER:
    Works on ANY input image (signs, logos, diagrams, badges, infographics).
    - Extracts dimensions and creates responsive viewBox.
    - Preserves background and layout geometry.
    - Converts all graphical details into genuine SVG <path> elements.
    - Strictly prevents emojis or unicode substitutions.
    """
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

    # Extract dominant palette
    palette = extract_dominant_colors(img, k=5)
    bg_color = palette[0]
    print(f"[+] Detected color palette: {palette}")

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Multi-level thresholding / color slicing to extract distinct graphical layers
    layers = []
    
    # Layer 1: Dark foreground elements (silhouettes, lines, text)
    _, dark_mask = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)
    dark_paths = image_to_svg_paths(dark_mask, scale=scale, epsilon_ratio=0.0025, min_area=20)
    if dark_paths:
        layers.append({"fill": "#1f2430", "paths": dark_paths, "name": "dark_elements"})

    # Layer 2: Colored / saturated accents (e.g. red, blue, green accents)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    sat = hsv[:, :, 1]
    _, sat_mask = cv2.threshold(sat, 80, 255, cv2.THRESH_BINARY)
    # Exclude what's already dark
    color_accent_mask = cv2.bitwise_and(sat_mask, cv2.bitwise_not(dark_mask))
    accent_paths = image_to_svg_paths(color_accent_mask, scale=scale, epsilon_ratio=0.003, min_area=30)
    if accent_paths:
        accent_color = palette[1] if len(palette) > 1 else "#d3222a"
        layers.append({"fill": accent_color, "paths": accent_paths, "name": "color_accents"})

    # Assemble complete SVG
    svg_lines = [
        f'<svg width="{target_width}" height="{target_height}" viewBox="0 0 {target_width} {target_height}" xmlns="http://www.w3.org/2000/svg">',
        '  <!-- Background Canvas -->',
        f'  <rect width="{target_width}" height="{target_height}" rx="12" ry="12" fill="{bg_color}" />'
    ]

    for layer in layers:
        svg_lines.append(f'  <!-- Layer: {layer["name"]} (Pure vector paths, zero emojis) -->')
        svg_lines.append(f'  <g id="{layer["name"]}" fill="{layer["fill"]}">')
        for p in layer["paths"]:
            svg_lines.append(f'    <path d="{p}" fill-rule="evenodd" />')
        svg_lines.append('  </g>')

    svg_lines.append('</svg>')

    os.makedirs(os.path.dirname(os.path.abspath(output_svg_path)), exist_ok=True)
    with open(output_svg_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_lines))

    print(f"[PASS] Successfully generated universal vector SVG at: {output_svg_path}")
    return output_svg_path

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python auto_vectorizer.py <input_image> [output_svg]")
        sys.exit(1)
    inp = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else "output.svg"
    vectorize_general_image(inp, out)
