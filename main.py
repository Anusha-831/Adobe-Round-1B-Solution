import os 
import time 
import uuid 
import json 
import argparse 
from datetime import datetime 
from utils.pdf_parser import extract_pdf_sections 
from utils.relevance_ranker import rank_sections_by_persona 
from utils.summarizer import summarize_sections

INPUT_DIR = "./input" 
OUTPUT_DIR = "./output" 
TOP_K = 15

os.makedirs(OUTPUT_DIR, exist_ok=True)

def process_document(file_name, persona, job_description): 
    file_path = os.path.join(INPUT_DIR, file_name) 
    print(f"\n📄 [{file_name}] Processing document...")

    # Step 1: Extract Sections
    sections, num_pages = extract_pdf_sections(file_path)
    print(f"📄 {num_pages} pages, {len(sections)} sections extracted")

    if not sections:
        print("⚠️  No sections found. Skipping.")
        return None

    # Step 2: Rank Sections
    top_sections = rank_sections_by_persona(sections, persona, job_description, top_k=TOP_K)

    # Step 3: Summarize
    refined_summaries = summarize_sections(top_sections, INPUT_DIR)

    # Step 4: Format Output JSON
    metadata = {
        "input_documents": [file_name],
        "persona": persona,
        "job": job_description,
        "timestamp": str(datetime.utcnow())
    }

    extracted = [
        {
            "id": str(uuid.uuid4()),
            "document": sec["document"],
            "page": sec["page"],
            "text": sec["text"],
            "relevance_score": round(sec["relevance_score"], 4),
            "importance_rank": sec["importance_rank"]
        }
        for sec in top_sections
    ]

    sub_analysis = [
        {
            "document": r["document"],
            "page": r["page"],
            "heading_title": r.get("heading_title", ""),
            "refined_text": r["refined_text"]
        }
        for r in refined_summaries
    ]

    final_output = {
        "metadata": metadata,
        "extracted_sections": extracted,
        "sub_section_analysis": sub_analysis
    }

    # Save output
    out_file = os.path.join(OUTPUT_DIR, f"{os.path.splitext(file_name)[0]}.json")
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(final_output, f, indent=2)

    print(f"✅ Output saved to: {out_file}")
    return extracted

def main(): 
    parser = argparse.ArgumentParser(description="Persona-Driven Document Intelligence") 
    parser.add_argument('--persona', type=str, default="Test Researcher", help='Persona description') 
    parser.add_argument('--job', type=str, default="Summarise key sections", help='Job to be done') 
    parser.add_argument('--top_k', type=int, default=TOP_K, help='Top-K relevant sections') 
    args = parser.parse_args()

    persona = args.persona
    job_description = args.job
    top_k = args.top_k

    print("📁 Scanning input directory...")
    pdf_files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith('.pdf')]
    print(f"\nFound {len(pdf_files)} PDF files to process for persona-driven analysis\n")
    print(f"Persona: '{persona}' |\n\nJob: '{job_description}' |\n\nTop-K: {top_k}\n")

    all_sections = []
    start_time = time.time()

    for idx, file_name in enumerate(pdf_files):
        print(f"[{idx + 1}/{len(pdf_files)}] {file_name}")
        try:
            sections = process_document(file_name, persona, job_description)
            if sections:
                all_sections.extend(sections)
        except Exception as e:
            print(f"❌ Error processing {file_name}: {e}")

    end_time = time.time()
    print("\n✨ Persona-driven analysis completed!")
    print(f"\nDocuments processed: {len(pdf_files)}")
    print(f"Total sections analyzed: {len(all_sections)}")
    print(f"Total processing time: {round(end_time - start_time, 3)} seconds")

if __name__ == "__main__": 
    main()