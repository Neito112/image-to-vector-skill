---
name: image-to-vector
description: Universal skill & toolchain to convert ANY input image into 100% visually faithful, smooth SVG vector graphics using intelligent contour inference, clean Bezier reconstruction (avoiding noisy pixel fragmentation), standard SVG typography, instant preview rendering, and direct one-click links.
---

# 🚀 Universal Image-to-Vector Skill

This skill and its bundled toolchain are **100% universal and general-purpose**, designed to convert **ANY input image** into high-fidelity, clean, professional SVG vector graphics.

---

## 🎯 Core Principles & Non-Negotiable Directives

1. **Intelligent Contour Inference (No Fragmented or Distorted Pixels)**:
   - **DO NOT** perform blind, dogmatic pixel-thresholding on raw bitmaps or noisy photographs. Direct thresholding of camera noise, compression artifacts, and lighting gradients causes vectors to look **jagged, distorted, and fragmented** ("méo mó, phân mảnh").
   - **INFER AND RECONSTRUCT**: Analyze the intended design, infer the true silhouette and contours, and reconstruct them using **smooth mathematical Bezier curves (`C`, `S`, `Q`)**, clean geometric primitives (`<circle>`, `<rect>`, `<line>`), and continuous closed paths (`Z`).
   - Graphic elements (shoes, vehicles, animals, logos, icons, human figures) must look polished, cohesive, smooth, and professionally illustrated.

2. **Strict Typography Standard (Standard SVG Text)**:
   - Textual labels, titles, headers, and body words **MUST ALWAYS** be rendered using genuine, standard SVG `<text>` elements with appropriate font stacks (`Arial, 'Helvetica Neue', 'Segoe UI', Roboto, sans-serif`), weights, sizes, and colors.
   - Never turn text into noisy, distorted path fragments.

3. **No Emojis or Character Substitutions**:
   - Strictly forbidden to substitute drawn graphics with emojis (e.g. 👠, 👞, ⛔) or Unicode characters.

4. **Instant Visual Preview + Direct Open Links**:
   - In every completion response, the assistant must provide:
     1. **Inline Rendered Preview**: `![Preview](file:///..._preview.png)`
     2. **Clickable Direct File Link**: `[Mở trực tiếp file SVG](file:///.../output.svg)`
     3. **Clickable Direct Folder Link**: `[Mở thư mục chứa file](file:///.../)`

---

## 🛠️ Toolchain Reference

| Tool | Purpose | Usage |
| :--- | :--- | :--- |
| **`scripts/auto_vectorizer.py`** | Automated pipeline with adaptive denoising, contour smoothing, and dual output (`.svg` + `_preview.png`). | `python scripts/auto_vectorizer.py <input_img> <output.svg>` |
| **`scripts/vector_tracer.py`** | Precision contour tracer with customizable curve smoothing (`epsilon_ratio`). | `python scripts/vector_tracer.py <image_or_mask> [output.svg]` |
| **`scripts/validator.py`** | Quality gate: verifies XML schema, checks presence of vector paths, and rejects emoji glyphs. | `python scripts/validator.py <target.svg>` |

---

## 📋 Universal Execution Workflow

1. **Analyze Design & Hierarchy**:
   - Detect canvas dimensions, background, frames, and color palette.
   - Separate textual zones from illustration/icon zones.
2. **Intelligently Reconstruct Graphic Elements**:
   - Deduce the intended smooth contours of the drawing.
   - Formulate clean Bezier curves (`M... C... C... Z`) and geometric shapes.
3. **Typeset Text Elements**:
   - Create crisp SVG `<text>` elements with matched font properties, alignments, and accent lines.
4. **Validate**:
   - Run `python scripts/validator.py <generated.svg>`.
5. **Render Preview & Deliver**:
   - Render the antialiased preview image (`_preview.png`).
   - Deliver with inline image preview and one-click file/folder links.
