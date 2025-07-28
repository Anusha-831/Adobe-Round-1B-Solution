import os
import fitz 
from transformers import pipeline

def extract_text_by_heading(pdf_path, page_num, heading_title):
    doc = fitz.open(pdf_path)
    text = ""

    # Try extracting text from current and next 2 pages
    pages_to_check = [page_num - 1]
    if page_num < len(doc):
        pages_to_check.append(page_num)
    if page_num + 1 < len(doc):
        pages_to_check.append(page_num + 1)

    heading_found = False

    for p in pages_to_check:
        try:
            page_text = doc[p].get_text()
            if heading_title.lower() in page_text.lower():
                start_idx = page_text.lower().find(heading_title.lower())
                extracted_text = page_text[start_idx:]
                text += extracted_text + "\n"
                heading_found = True
        except:
            continue

    # Fallback: if heading not found, use full page text
    if not heading_found:
        try:
            text = doc[page_num - 1].get_text()
        except:
            text = ""

    return text.strip()


def summarize_sections(ranked_sections, input_dir):
    summarizer = pipeline(
        "summarization",
        model="D:/huggingface/hub/models--t5-small",
        tokenizer="D:/huggingface/hub/models--t5-small"
    )

    refined_sections = []

    for section in ranked_sections:
        doc_name = section["document"]
        page_num = section["page"]
        heading_title = section["text"]
        pdf_path = os.path.join(input_dir, doc_name)

        section_text = extract_text_by_heading(pdf_path, page_num, heading_title)

        word_count = len(section_text.split())
        if word_count < 20:
            summary = "Summary generation failed due to insufficient content."
        else:
            try:
                input_text = "summarize: " + section_text[:1000]
                output = summarizer(input_text, max_length=100, min_length=30, do_sample=False)
                summary = output[0]['summary_text']
            except Exception as e:
                summary = f"Summary generation failed. ({str(e)})"

        refined_sections.append({
            "document": doc_name,
            "page": page_num,
            "heading_title": heading_title,
            "refined_text": summary
        })

    return refined_sections