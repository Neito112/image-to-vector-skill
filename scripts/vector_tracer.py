import os
import sys
import cv2
import numpy as np

def trace_contours_to_svg(image_path, output_svg_path=None, scale=1.0, offset_x=0, offset_y=0, threshold=95, min_area=30, epsilon_ratio=0.003):
    """
    Extracts high-fidelity vector contours from an image or mask and converts them to SVG <path> elements.
    Never substitutes vector graphics with emojis or unicode symbols.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Input image not found: {image_path}")

    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError(f"Unable to read image: {image_path}")

    # Threshold if not already binary
    if len(np.unique(img)) > 2:
        _, binary = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY_INV)
    else:
        binary = img

    cnts, hier = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_KCOS)
    paths = []

    for c in cnts:
        area = cv2.contourArea(c)
        if area >= min_area:
            epsilon = epsilon_ratio * cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, epsilon, True)
            pts = approx.reshape(-1, 2)
            if len(pts) < 3:
                continue
            
            d_parts = [f"M {(pts[0][0] + offset_x) * scale:.2f} {(pts[0][1] + offset_y) * scale:.2f}"]
            for p in pts[1:]:
                d_parts.append(f"L {(p[0] + offset_x) * scale:.2f} {(p[1] + offset_y) * scale:.2f}")
            d_parts.append("Z")
            paths.append(" ".join(d_parts))

    if output_svg_path:
        h, w = img.shape
        svg_w = w * scale
        svg_h = h * scale
        with open(output_svg_path, "w", encoding="utf-8") as f:
            f.write(f'<svg width="{svg_w}" height="{svg_h}" xmlns="http://www.w3.org/2000/svg">\n')
            for p in paths:
                f.write(f'  <path d="{p}" fill="#222834" />\n')
            f.write('</svg>\n')
        print(f"[+] Exported SVG with {len(paths)} paths to: {output_svg_path}")

    return paths

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python vector_tracer.py <input_image> [output_svg]")
        sys.exit(1)
    inp = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else "traced_output.svg"
    trace_contours_to_svg(inp, out)
