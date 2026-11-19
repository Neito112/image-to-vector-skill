---
name: image-to-vector
description: Universal skill & toolchain to convert ANY input image (signs, logos, emblems, badges, diagrams, typography) into 100% faithful SVG vector graphics with pure vector paths, zero emojis, rendered preview image, and direct one-click links to open file and folder.
---

# 🚀 Universal Image-to-Vector Skill

This skill and its bundled toolchain are **100% universal and general-purpose**, designed to convert **ANY input image** (photographs of signs, logos, icons, badges, posters, or UI elements) into high-fidelity, scalable SVG vector graphics.

---

## 🎯 Core Principles & Non-Negotiable Rules

1. **Universal Applicability**:
   - The workflow and tools apply to **ANY input image**, regardless of subject matter (signs, vehicles, logos, diagrams, labels, product tags).
2. **100% Geometric & Visual Parity**:
   - The generated SVG must preserve the source image's aspect ratio, layout, hierarchical proportions, colors, and styling.
3. **Strict Separation of Graphics vs. Text**:
   - **Graphical Elements (drawings, silhouettes, icons, symbols, logos, borders, badges)**:
     - MUST ALWAYS be rendered as genuine vector shapes (`<path>`, `<circle>`, `<polygon>`, `<rect>`, `<g>`).
     - **ABSOLUTE PROHIBITION**: NEVER use emojis (e.g. 👠, 👞, ⛔), unicode characters, or symbol fonts as substitutes for illustrations.
   - **Text Elements**:
     - MUST be rendered as genuine SVG `<text>` elements with matched font family, weight, alignment, and fill color.
4. **Mandatory Automated Validation**:
   - Every generated SVG must pass `scripts/validator.py` before delivery.
5. **Mandatory Delivery Protocol (Preview + Direct Open Links)**:
   - In every response completing a vectorization task, the assistant MUST provide:
     1. **Inline Preview Image**: Display the rendered preview image directly in chat (`![Preview](file:///..._preview.png)`).
     2. **Clickable Direct File Link**: To open the `.svg` file directly in the user's default viewer (`[Mở trực tiếp file SVG](file:///.../output.svg)`).
     3. **Clickable Direct Folder Link**: To open the containing directory in File Explorer (`[Mở thư mục chứa file](file:///.../)`).

---

## 🛠️ Toolchain Reference

The repository provides three standardized, ready-to-use Python tools:

| Tool | Purpose | Usage |
| :--- | :--- | :--- |
| **`scripts/auto_vectorizer.py`** | Universal automated pipeline for **ANY input image**. Detects color palette, segments foreground layers, extracts multi-contour vector `<path>` elements, and generates both `<name>.svg` and `<name>_preview.png`. | `python scripts/auto_vectorizer.py <input_img> <output.svg>` |
| **`scripts/vector_tracer.py`** | High-precision contour tracer for extracting specific objects, masks, or cropped icons into smooth `<path d="...">` data. | `python scripts/vector_tracer.py <image_or_mask> [output.svg]` |
| **`scripts/validator.py`** | Automated compliance and quality-gate checker. Guarantees well-formed XML, presence of real paths, and 100% absence of emojis in graphics. | `python scripts/validator.py <target.svg>` |

---

## 📋 Universal Execution Workflow

Whenever a user provides ANY image and requests a vector version:

### 1. Ingestion & Analysis
- Inspect the input image's dimensions, aspect ratio, and color palette.
- Identify the core zones:
  - Background & borders.
  - Graphical illustrations, logos, or icons.
  - Textual headers, body labels, or captions.

### 2. Vectorization of Graphics
- For arbitrary designs, run `scripts/auto_vectorizer.py` to extract all contours into layered vector `<path>` elements and generate both the `.svg` and `_preview.png`.
- For hybrid designs (combining logos/drawings with clean typography):
  - Extract the graphical shapes using `scripts/vector_tracer.py`.
  - Reconstruct the textual elements with matched SVG `<text>` tags and exact font properties.
  - Generate the corresponding raster preview image.

### 3. Layer Assembly
- Structure the SVG with proper `<defs>` (gradients, masks, clips).
- Layer sequence:
  1. Background plate & canvas.
  2. Borders and frames.
  3. Graphical drawings (`<path>`, `<g>`).
  4. Text blocks (`<text>`).
  5. Accent details (dividers, underlines, strikethroughs).

### 4. Automated Quality Gate
- Execute `python scripts/validator.py <generated.svg>`.
- If any emoji or validation error is detected, fix the offending element immediately.

### 5. Delivery (Preview & Direct Open Links)
Provide the standard response with:
- Rendered visual preview image: `![Xem trước](file:///path/to/output_preview.png)`
- Direct file open link: `[Mở trực tiếp file SVG](file:///path/to/output.svg)`
- Direct folder open link: `[Mở thư mục chứa file](file:///path/to/folder/)`
