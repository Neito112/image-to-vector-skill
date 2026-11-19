import os
import sys
import cv2
import numpy as np

def extract_dominant_colors(image, k=4):
    """
    Extracts dominant colors in an image using K-Means clustering.
    Returns RGB hex colors and BGR tuples.
    """
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
    """
    Converts any binary mask of graphics into smooth SVG path strings and polygon points.
    """
    cnts, hier = cv2.findContours(binary_mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_TC89_KCOS)
    if not cnts or hier is None:
        return [], []

    paths = []
    poly_points = []
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
        poly_points.append(scaled_pts.astype(np.int32))

        d = [f"M {scaled_pts[0][0]:.2f} {scaled_pts[0][1]:.2f}"]
        for p in scaled_pts[1:]:
            d.append(f"L {p[0]:.2f} {p[1]:.2f}")
        d.append("Z")
        paths.append(" ".join(d))

    return paths, poly_points

def vectorize_general_image(input_image_path, output_svg_path, target_width=1000):
    """
    UNIVERSAL IMAGE-TO-VECTOR CONVERTER WITH DUAL OUTPUT:
    1. Generates 100% scalable vector SVG (<name>.svg).
    2. Generates instant raster preview image (<name>_preview.png).
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
    hex_palette, bgr_palette = extract_dominant_colors(img, k=5)
    bg_hex = hex_palette[0]
    bg_bgr = bgr_palette[0]

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Multi-level thresholding / color slicing to extract distinct graphical layers
    layers = []
    
    # Layer 1: Dark foreground elements (silhouettes, lines, text)
    _, dark_mask = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)
    dark_paths, dark_polys = image_to_svg_paths(dark_mask, scale=scale, epsilon_ratio=0.0025, min_area=20)
    if dark_paths:
        layers.append({
            "fill": "#1f2430", 
            "bgr": (48, 36, 31), 
            "paths": dark_paths, 
            "polys": dark_polys, 
            "name": "dark_elements"
        })

    # Layer 2: Colored / saturated accents
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    sat = hsv[:, :, 1]
    _, sat_mask = cv2.threshold(sat, 80, 255, cv2.THRESH_BINARY)
    color_accent_mask = cv2.bitwise_and(sat_mask, cv2.bitwise_not(dark_mask))
    accent_paths, accent_polys = image_to_svg_paths(color_accent_mask, scale=scale, epsilon_ratio=0.003, min_area=30)
    if accent_paths:
        accent_hex = hex_palette[1] if len(hex_palette) > 1 else "#d3222a"
        accent_bgr = bgr_palette[1] if len(bgr_palette) > 1 else (42, 34, 211)
        layers.append({
            "fill": accent_hex, 
            "bgr": accent_bgr, 
            "paths": accent_paths, 
            "polys": accent_polys, 
            "name": "color_accents"
        })

    # Assemble complete SVG
    svg_lines = [
        f'<svg width="{target_width}" height="{target_height}" viewBox="0 0 {target_width} {target_height}" xmlns="http://www.w3.org/2000/svg">',
        '  <!-- Background Canvas -->',
        f'  <rect width="{target_width}" height="{target_height}" rx="12" ry="12" fill="{bg_hex}" />'
    ]

    # Create raster canvas for instant preview
    preview_canvas = np.full((target_height, target_width, 3), bg_bgr, dtype=np.uint8)

    for layer in layers:
        svg_lines.append(f'  <!-- Layer: {layer["name"]} (Pure vector paths, zero emojis) -->')
        svg_lines.append(f'  <g id="{layer["name"]}" fill="{layer["fill"]}">')
        for p in layer["paths"]:
            svg_lines.append(f'    <path d="{p}" fill-rule="evenodd" />')
        svg_lines.append('  </g>')

        # Render preview polygons with Anti-Aliasing
        for poly in layer["polys"]:
            cv2.fillPoly(preview_canvas, [poly], layer["bgr"], lineType=cv2.LINE_AA)

    svg_lines.append('</svg>')

    os.makedirs(os.path.dirname(os.path.abspath(output_svg_path)), exist_ok=True)
    with open(output_svg_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_lines))
    print(f"[+] Exported Vector SVG: {output_svg_path}")

    # Export preview PNG alongside the SVG
    base_name, _ = os.path.splitext(output_svg_path)
    preview_png_path = f"{base_name}_preview.png"
    cv2.imwrite(preview_png_path, preview_canvas)
    print(f"[+] Exported Preview PNG: {preview_png_path}")

    return output_svg_path, preview_png_path

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python auto_vectorizer.py <input_image> [output_svg]")
        sys.exit(1)
    inp = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else "output.svg"
    vectorize_general_image(inp, out)
