# 🎯 Image-to-Vector Skill

A production-grade, automated skill and toolkit for converting reference photos, signs, and graphic designs into **100% faithful, scalable SVG vector graphics**.

## 🌟 Key Highlights

- **Pure Vector Drawing**: Graphical elements (shoes, icons, symbols) are drawn exclusively with SVG `<path>`, `<circle>`, and `<rect>` elements. **Zero emojis or unicode shortcuts.**
- **Accurate Typography**: Genuine SVG `<text>` elements with precise font weights, kerning, and alignments.
- **Automated Validation**: Built-in verification script (`scripts/validator.py`) guarantees structural and rule compliance.
- **Vector Tracer Tool**: Bundled contour tracing script (`scripts/vector_tracer.py`) for automated mask-to-path generation.

---

## 📁 Repository Structure

```
├── SKILL.md                  # Standard Operating Procedure (SOP) & Rules
├── scripts/
│   ├── vector_tracer.py      # Image contour to SVG path extractor
│   └── validator.py          # Strict compliance validation tool
└── examples/
    └── no_shoes_sign.svg     # Reference example (100% vector-faithful sign)
```

---

## 🛠️ Usage

### 1. Tracing an image element into SVG paths:
```bash
python scripts/vector_tracer.py path/to/image.png output.svg
```

### 2. Validating compliance:
```bash
python scripts/validator.py output.svg
```

---

## 📜 Example Output

The reference sign in `examples/no_shoes_sign.svg` features:
- Metallic brushed gradient background with rounded borders.
- Proportional prohibition ring and diagonal slash.
- High heel stiletto and leather dress shoe drawn with **pure SVG vector paths**.
- Centered Vietnamese and English typography with authentic divider and strikethrough styling.
