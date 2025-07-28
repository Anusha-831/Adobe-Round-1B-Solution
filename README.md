# 🧠 PDF Outline Extractor – Round 1A Solution
Adobe India Hackathon 2025 – Round 1A  
Team: Innoventors  
Contributors: Koyyada Anusha, Muddassir Shakhan

## 🚀 Challenge: Persona-Driven Document Intelligence

> “Connect What Matters — For the User Who Matters”

This project builds an intelligent document analysis system that extracts and ranks the most relevant sections from a collection of PDFs based on a user-defined persona and their job-to-be-done.

---

## 🧑‍💼 Input Format

- Documents: 3 to 10 related PDFs
- Persona: Describes the role and expertise (e.g., “PhD Researcher in Computational Biology”)
- Job-to-be-Done: Specific task (e.g., “Summarize methodologies in GNNs for drug discovery”)

---

## 🧠 Output Format

Each document outputs a JSON with:
1. Metadata
   - Input file name
   - Persona
   - Job
   - Timestamp
2. Extracted Sections
   - Document name
   - Page number
   - Text content
   - Relevance score
   - Importance rank
3. Sub-section Analysis
   - Document
   - Page
   - Refined summary text

Sample output: See output/Document - X/Document - X.json

---

## 🛠️ How to Run

### 🧪 Requirements
- Python 3.10+
- CPU-only (no GPU)
- Model sizes ≤ 1GB
- No internet access

### ✅ Setup

1. Install dependencies:
   `bash
   pip install -r requirements.txt
   
3. Place PDF files inside input/ folder.

4. Run the script:

   python main.py --persona "PhD Researcher in Computational Biology" --job "Prepare a literature review on GNNs in drug discovery" --top_k 15

4. Check outputs in: output/DocumentName/DocumentName.json

---

### 🐳 Run via Docker (Offline Mode)

1. Build image:

docker build -t adobe-r1b .

2. Run container:

docker run --rm -v "$(pwd)/input":/app/input -v "$(pwd)/output":/app/output adobe-r1b

---

## 📌 Constraints Satisfied

✅ Offline execution (no internet)

✅ CPU only

✅ Model size < 1GB (all-MiniLM-L6-v2, t5-small)

✅ Output matches official JSON format

✅ Fast processing (≤60s for 3–5 PDFs)
