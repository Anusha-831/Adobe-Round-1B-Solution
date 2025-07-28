from sentence_transformers import SentenceTransformer, util
import torch
import uuid

def rank_sections_by_persona(sections, persona, job_description, top_k=15):
    model_path = "D:/huggingface/hub/models--sentence-transformers--all-MiniLM-L6-v2"
    model = SentenceTransformer(model_path)

    query = f"{persona}. {job_description}"
    query_embedding = model.encode(query, convert_to_tensor=True)

    ranked_sections = []
    for section in sections:
        section_title = section.get("section_title", "")
        combined_text = section_title.strip()
        section_embedding = model.encode(combined_text, convert_to_tensor=True)

        score = util.cos_sim(query_embedding, section_embedding).item()

        ranked_sections.append({
            "id": str(uuid.uuid4()),
            "document": section.get("document", ""),
            "page": section.get("page", -1),
            "text": section_title,
            "relevance_score": round(score, 4)
        })

    top_sections = sorted(ranked_sections, key=lambda x: x["relevance_score"], reverse=True)[:top_k]

    for rank, sec in enumerate(top_sections, 1):
        sec["importance_rank"] = rank

    return top_sections