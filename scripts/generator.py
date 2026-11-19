import sys

def generate_svg_from_prompt(prompt, output_file):
    """
    Simple generator that creates a basic SVG structure based on a prompt.
    In a real scenario, this would use a computer vision or LLM-based parsing.
    """
    svg_content = f"""<svg width="600" height="250" xmlns="http://www.w3.org/2000/svg">
  <rect width="600" height="250" rx="15" ry="15" fill="#d1d1d1" stroke="#333" stroke-width="4"/>
  <text x="50" y="125" font-family="Arial" font-size="20" fill="#333">Generated from: {prompt}</text>
</svg>"""
    
    with open(output_file, "w") as f:
        f.write(svg_content)
    print(f"SVG generated at {output_file}")

if __name__ == "__main__":
    generate_svg_from_prompt(" ".join(sys.argv[1:]), "output.svg")
