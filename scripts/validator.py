import sys
import xml.etree.ElementTree as ET
import re

def validate_svg(svg_path):
    """
    Validates SVG according to strict skill rules:
    1. Must be valid XML.
    2. Must contain genuine vector paths/shapes for graphics.
    3. Strictly forbids using emojis or unicode symbols as graphics.
    4. Text elements must only contain legitimate words/labels.
    """
    print(f"[*] Validating SVG: {svg_path}")
    try:
        tree = ET.parse(svg_path)
        root = tree.getroot()
    except Exception as e:
        print(f"[FAIL] Invalid XML/SVG syntax: {e}")
        return False

    ns = {'svg': 'http://www.w3.org/2000/svg'}
    
    # Check paths and shapes
    paths = root.findall('.//svg:path', ns) + root.findall('.//path')
    circles = root.findall('.//svg:circle', ns) + root.findall('.//circle')
    rects = root.findall('.//svg:rect', ns) + root.findall('.//rect')
    lines = root.findall('.//svg:line', ns) + root.findall('.//line')
    polygons = root.findall('.//svg:polygon', ns) + root.findall('.//polygon')

    total_shapes = len(paths) + len(circles) + len(rects) + len(lines) + len(polygons)
    print(f"[+] Vector shapes found: {total_shapes} (paths: {len(paths)}, circles: {len(circles)}, lines: {len(lines)}, rects: {len(rects)})")
    
    if total_shapes == 0:
        print("[FAIL] No vector drawing shapes found!")
        return False

    # Check text elements
    texts = root.findall('.//svg:text', ns) + root.findall('.//text')
    print(f"[+] Text elements found: {len(texts)}")

    # Check for emojis or symbol glyphs in text
    emoji_pattern = re.compile(
        "[\U00010000-\U0010ffff"  # Supplemental symbols & pictographs, emojis
        "\u2600-\u27bf"          # Miscellaneous symbols & dingbats
        "\u2300-\u23ff"          # Miscellaneous technical
        "\u2b50-\u2b55"          # Star symbols
        "]+", flags=re.UNICODE
    )

    has_violation = False
    for idx, t in enumerate(texts):
        content = "".join(t.itertext()).strip()
        print(f"    - Text #{idx + 1}: \"{content}\"")
        if emoji_pattern.search(content):
            print(f"[FAIL] Rule violation in Text #{idx + 1}: Emoji/Icon character detected: '{content}'")
            print("       Graphical icons must be drawn with SVG <path>/<shape>, NOT emojis!")
            has_violation = True

    if has_violation:
        return False

    print("[PASS] SVG successfully verified! 100% compliant with strict vectorization standards.")
    return True

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else 'd:/ComfyUI/svg/no_shoes_sign.svg'
    success = validate_svg(target)
    sys.exit(0 if success else 1)
