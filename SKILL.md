---
name: image-to-vector
description: Universal skill & toolchain to convert ANY input image into 100% faithful, professional SVG vector graphics using a search-first icon strategy (retrieving standard SVG snippets from the web and fine-tuning), strict typography metric calibration, instant Headless Chrome preview rendering, and direct native Windows launch.
---

# 🚀 Universal Image-to-Vector Skill

This skill and its bundled toolchain are **100% universal and general-purpose**, designed to convert **ANY input image** into high-fidelity, clean, professional SVG vector graphics.

---

## 🎯 Core Principles & Non-Negotiable Directives

1. **Search-First Icon & Graphic Strategy (Hạn chế tự vẽ hình bằng code)**:
   - **DO NOT** hand-code complex graphical shapes from scratch blindly, and **DO NOT** perform raw noisy pixel thresholding.
   - **USE WEB SEARCH / REPOSITORIES**: Query online vector repositories (Wikimedia, SVGRepo, open icon sets) via web search to locate clean, standard SVG/HTML code for the matching objects, symbols, or silhouettes.
   - **FINE-TUNE & CALIBRATE**: Incorporate the clean vector paths into the design, calibrate their scale, rotation, stroke, and Bezier control points to match the target reference image with 100% fidelity.

2. **Strict Typography Metric Calibration (Bám sát bố cục & size chữ gốc)**:
   - Text elements **MUST NOT** have arbitrary sizes or estimated line widths.
   - Measure the exact bounding box, aspect ratio, and baseline coordinates from the source image.
   - Use SVG attributes `textLength` and `lengthAdjust="spacingAndGlyphs"` alongside proper font stacks (`'Arial', 'Helvetica Neue', 'Segoe UI', Roboto, sans-serif`) to ensure words, dividers, and strikethroughs match the exact pixel spans of the reference.

3. **Standard SVG Typography**:
   - Textual labels MUST ALWAYS be rendered using genuine SVG `<text>` elements. Never substitute text with jagged pixel paths.

4. **Zero Emojis**:
   - Strictly forbidden to use emojis (e.g. 👠, 👞, ⛔) or Unicode characters as graphics.

5. **Headless Chrome Rendering & Native Windows Launch**:
   - Preview images MUST be rendered directly from the `.svg` using the **Headless Chrome Engine** for 100% subpixel antialiasing and color fidelity.
   - Every delivery must provide inline preview and launch the files externally in Windows Explorer and the default viewer.

---

## 📋 Universal Execution Workflow

### Step 1: Metric Extraction & Layout Calibration
- Extract canvas dimensions, aspect ratio, and color palette.
- Measure the exact bounds of text blocks:
  - Width and height of each line.
  - Span of dividers and strikethrough lines.
  - Left/right margins and vertical rhythm.

### Step 2: Search & Retrieval of Graphic Paths
- Identify the graphical symbols in the design (e.g. prohibition signs, shoes, vehicles, logos).
- Search the web for clean SVG vector representations.
- Copy the SVG `<path d="...">` markup, clean it, and adjust coordinate transforms (`translate`, `scale`, `rotate`).

### Step 3: Layer Assembly
- Background plate with metallic or solid gradient.
- Inner border frames.
- Graphical elements (`<path>`, `<circle>`, `<g>`).
- Calibrated typography (`<text ... textLength="..." lengthAdjust="spacingAndGlyphs">`).
- Accent lines (dividers, underlines, strikethroughs).

### Step 4: Verification & Chrome Rendering
- Validate with `python scripts/validator.py <file.svg>`.
- Render pixel-perfect preview via Chrome:
  ```bash
  chrome --headless=new --screenshot=<file_preview.png> --window-size=W,H <file.svg>
  ```

### Step 5: Native Launch & Delivery
- Open externally on Windows:
  ```powershell
  Start-Process explorer.exe -ArgumentList "<folder_path>"
  Start-Process "<file_path.svg>"
  ```
- Output inline preview in chat.
