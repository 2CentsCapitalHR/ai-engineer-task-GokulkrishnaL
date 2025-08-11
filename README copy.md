# ADGM-Compliant Corporate Agent (Demo Repo)

This repository is a demo-ready skeleton for the Candidate Task: **ADGM-Compliant Corporate Agent with Document Intelligence**.

## What is included
- Gradio UI (`app.py`) to upload `.docx` files
- Analysis pipeline that extracts text, runs simple heuristic RAG checks, produces a JSON report, and annotates a `.docx`
- FAISS/RAG hooks (demo placeholder) in `rag_engine.py`
- Minimal DOCX parsing that works for simple `.docx` files created by the demo
- Example input and output `.docx` files in `data/example_input` and `data/example_output`
- `requirements.txt` listing suggested dependencies

## Setup
1. Clone the repo or unzip the provided ZIP.
2. Create a virtualenv and install dependencies:
   ```
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Add your OpenAI key:
   ```
   export OPENAI_API_KEY="sk-..."
   ```

## Run
```bash
python app.py
```
Open the Gradio interface and upload example `.docx` files from `data/example_input/`.

## Notes
- The RAG pipeline is implemented in a demo-friendly way; to fully enable it, populate `data/adgm_sources` with ADGM PDFs and configure OpenAI usage in `rag_engine.py`.
- The annotate function appends simple comment paragraphs into the `.docx`. For production, a proper Word comments implementation is recommended.



## Official data sources links
See `data/data_sources_links.txt` for official ADGM links extracted from the uploaded Data Sources.pdf. The PDF is included in the submission and can be cited as: fileciteturn0file0
