import fitz
import os
from typing import List, Dict

def extract_pdf_sections(pdf_path: str) -> List[Dict]:
    doc = fitz.open(pdf_path)
    doc_name = os.path.basename(pdf_path)
    sections = []

    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" not in block:
                continue
            for line in block["lines"]:
                line_text = ""
                max_font_size = 0
                for span in line["spans"]:
                    line_text += span["text"].strip() + " "
                    max_font_size = max(max_font_size, span["size"])

                text = line_text.strip()
                if not text or len(text) < 3:
                    continue

                heading_level = None
                if max_font_size >= 16:
                    heading_level = "H1"
                elif 13 <= max_font_size < 16:
                    heading_level = "H2"
                elif 11 <= max_font_size < 13:
                    heading_level = "H3"

                if heading_level:
                    sections.append({
                        "document": doc_name,
                        "page": page_num,
                        "section_title": text,
                        "heading_level": heading_level
                    })

    return sections, len(doc)