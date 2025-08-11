import os
import json
from utils.docx_parser import extract_text_from_docx
from checklist import checklist_check
from rag_engine import detect_red_flags
from annotate_docx import insert_comments

def analyze_documents(file_objs):
    detected_docs = {}
    texts = {}

    # file_objs is a list of uploaded file paths or file-like objects
    for f in file_objs:
        # Gradio provides a tempfile with .name or a path string
        path = f.name if hasattr(f, "name") else f
        text = extract_text_from_docx(path)
        # Very simple doc type detection based on filename or content
        if "articles" in path.lower() or "articles" in text.lower():
            doc_type = "Articles of Association"
        elif "memorandum" in path.lower() or "memorandum" in text.lower():
            doc_type = "Memorandum of Association"
        elif "register" in path.lower() or "register" in text.lower():
            doc_type = "Register of Members and Directors"
        else:
            doc_type = os.path.basename(path)
        detected_docs[doc_type] = path
        texts[doc_type] = text

    # Process detection: basic heuristic
    process = "Company Incorporation" if any(k.startswith("Articles") or k.startswith("Memorandum") for k in detected_docs.keys()) else "Licensing"

    checklist_result = checklist_check(process, list(detected_docs.keys()))
    issues = detect_red_flags(texts)

    # Create reviewed doc by annotating the first uploaded doc as a demo
    first_path = list(detected_docs.values())[0]
    reviewed_path = os.path.join("data", "example_output", "example_after_reviewed.docx")
    os.makedirs(os.path.dirname(reviewed_path), exist_ok=True)
    insert_comments(first_path, issues, reviewed_path)

    summary = {
        "process": process,
        "documents_uploaded": len(detected_docs),
        "required_documents": checklist_result["required_documents"],
        "missing_documents": checklist_result["missing_documents"],
        "issues_found": issues
    }

    # write JSON report
    json_path = os.path.join("data", "example_output", "report.json")
    with open(json_path, "w", encoding="utf-8") as jf:
        json.dump(summary, jf, indent=2)

    return reviewed_path, summary
