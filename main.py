import fitz 
import os
import json

def classify_headings(text_blocks):
    sizes = sorted(set([b['size'] for b in text_blocks]), reverse=True)
    size_map = {}
    if len(sizes) > 0:
        size_map[sizes[0]] = "Title"
    if len(sizes) > 1:
        size_map[sizes[1]] = "H1"
    if len(sizes) > 2:
        size_map[sizes[2]] = "H2"
    if len(sizes) > 3:
        size_map[sizes[3]] = "H3"
    return size_map

def extract_outline(pdf_path):
    doc = fitz.open(pdf_path)
    blocks = []

    for page_num, page in enumerate(doc):
        blocks_data = page.get_text("dict")["blocks"]
        for block in blocks_data:
            for line in block.get("lines", []):
                line_text = ""
                font_sizes = []
                for span in line.get("spans", []):
                    line_text += span["text"].strip() + " "
                    font_sizes.append(span["size"])
                if line_text.strip():
                    avg_size = sum(font_sizes)/len(font_sizes)
                    blocks.append({
                        "text": line_text.strip(),
                        "size": avg_size,
                        "page": page_num + 1
                    })

    size_map = classify_headings(blocks)
    title = ""
    outline = []

    for block in blocks:
        level = size_map.get(block["size"])
        if level == "Title" and not title:
            title = block["text"]
        elif level in ["H1", "H2", "H3"]:
            outline.append({
                "level": level,
                "text": block["text"],
                "page": block["page"]
            })

    return {
        "title": title,
        "outline": outline
    }

def main():
    input_dir = "/app/input"
    output_dir = "/app/output"

    for filename in os.listdir(input_dir):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(input_dir, filename)
            data = extract_outline(pdf_path)
            out_filename = filename.replace(".pdf", ".json")
            with open(os.path.join(output_dir, out_filename), "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)

if __name__ == "__main__":
    main()
