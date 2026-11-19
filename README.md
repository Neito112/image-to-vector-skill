# 🎯 Universal Image-to-Vector Skill & Toolchain

A standardized, production-grade skill and automated toolchain for converting **ANY input image** into **100% faithful, scalable SVG vector graphics**.

## 🌟 Highlights

- **Universal Capability**: Works for any input image: signs, logos, badges, emblems, diagrams, labels, and iconography.
- **Pure Vector Drawings**: Every visual shape is traced and rendered with SVG `<path>`, `<circle>`, `<polygon>`, or `<rect>`. **Strictly ZERO emoji or character approximations.**
- **Proper Typography**: Text is structured as clean SVG `<text>` elements with matched fonts, weights, and alignments.
- **Built-in Quality Verification**: Includes an automated validator (`scripts/validator.py`) to verify schema and banish character-based fake vectors.

---

## 📁 Repository Structure

```
├── SKILL.md                  # Universal SOP and execution instructions
├── scripts/
│   ├── auto_vectorizer.py    # Universal end-to-end vectorizer for any image
│   ├── vector_tracer.py      # High-precision contour-to-path extractor
│   └── validator.py          # Strict compliance validation tool
└── examples/
    └── no_shoes_sign.svg     # Reference sign implementation (100% vector-faithful)
```

---

## 🛠️ Toolchain Reference

### 1. Vectorize Any Image Automatically:
```bash
python scripts/auto_vectorizer.py <input_image> <output_svg>
```

### 2. Extract Specific Shapes/Contours to SVG:
```bash
python scripts/vector_tracer.py <input_or_crop> <output_svg>
```

### 3. Verify Compliance (Zero Emojis, Real Vectors):
```bash
python scripts/validator.py <target_svg>
```
