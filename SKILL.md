---
name: image-to-vector
description: Converts reference images and signboards into 100% faithful, scalable SVG vector graphics with strict element separation (genuine vector paths for graphics, proper SVG text for typography, zero emoji substitutions).
---

# Image-to-Vector Skill

This skill automates the creation of 100% visually faithful, production-grade SVG vector graphics from reference photos and design mockups.

## ⚠️ NON-NEGOTIABLE CORE DIRECTIVES

1. **100% Visual and Geometric Parity**:
   - The generated SVG must match the reference image in layout, proportions, color palette, typography hierarchy, margins, and borders.
2. **Strict Element Separation**:
   - **Graphical / Iconic Elements**: MUST ALWAYS be drawn as genuine vector shapes (`<path>`, `<circle>`, `<rect>`, `<polygon>`, `<line>`, `<g>`).
   - **PROHIBITION ON EMOJIS & SPECIAL CHARACTERS**: It is strictly forbidden to use emojis (e.g., 👠, 👞, ⛔), Unicode pictographs, or dingbat symbols to represent illustrations or icons.
   - **Textual Elements**: MUST be rendered using genuine SVG `<text>` elements with precise font-family fallbacks, weights, text-anchor, and colors.
3. **Automated Quality Verification**:
   - Every generated SVG must pass `scripts/validator.py` to ensure valid XML and zero forbidden emoji substitutions.

---

## Standard Operating Procedure (SOP)

### Step 1: Image Deconstruction & Geometry Analysis
- Calculate canvas aspect ratio and set an appropriate `viewBox` (e.g., `0 0 1000 534`).
- Identify color palette: background, borders, primary accent, text colors.
- Map the spatial coordinates and bounding boxes of all components (icons, text blocks, dividers).

### Step 2: Vector Graphic Extraction / Construction
- For each graphical element (silhouettes, emblems, icons, badges):
  - Use `python scripts/vector_tracer.py <cropped_image_or_mask> <output_path>` to extract high-resolution, smoothed SVG contours (`<path d="...">`).
  - Or construct precise mathematical Bezier curves.
  - Combine multiple components (e.g., shoe body + sole + laces) as grouped vector paths.

### Step 3: Typography & Text Alignment
- Identify text case (ALL CAPS, Title Case), font weights (900 for extra-bold, 800 for bold), and line spacing.
- Center text blocks accurately using `text-anchor="middle"` with calculated anchor coordinates.
- Render special text treatments (e.g., strikethroughs, underlines, dividers) as dedicated `<line>` or `<path>` elements.

### Step 4: Layered SVG Assembly
Assemble elements in correct Z-index order:
1. `<defs>`: Gradients, clip paths, patterns.
2. Background plate & outer border.
3. Inset borders & frames.
4. Graphical drawings (`<path>`, `<circle>`, `<g>`).
5. Overlays (slashes, badges, clip masks).
6. Text elements (`<text>`).
7. Divider lines, accents, and strikethroughs.

### Step 5: Verification & Quality Gate
Run the automated validator:
```bash
python scripts/validator.py <generated_file.svg>
```
The validator checks:
- Well-formed XML/SVG.
- Existence of vector paths/shapes.
- Absence of emojis or unicode approximations.

---

## Tooling Reference

- `scripts/vector_tracer.py`: Extracts vector contours from images into smooth SVG `<path>` data.
- `scripts/validator.py`: Automated compliance verification tool.
- `examples/no_shoes_sign.svg`: Gold-standard reference implementation.
