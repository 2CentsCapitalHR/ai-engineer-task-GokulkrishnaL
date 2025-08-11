import os
import pickle
import numpy as np

# Note: This module expects an OPENAI_API_KEY env var for actual runs.
# For the demo skeleton, the detect_red_flags function will create a placeholder issue
# if it finds the word "jurisdiction" or "UAE Federal" in the text.

def detect_red_flags(texts):
    issues = []
    for doc_name, content in texts.items():
        if content is None:
            continue
        lower = content.lower()
        if "uae federal" in lower or "federal courts" in lower or "federal court" in lower:
            issues.append({
                "document": doc_name,
                "section": "Jurisdiction clause",
                "issue": "Jurisdiction references UAE Federal Courts instead of ADGM Courts",
                "severity": "High",
                "suggestion": "Update jurisdiction clause to refer explicitly to ADGM Courts.",
                "citation": "ADGM Companies Regulations 2020, Art. 16"
            })
        elif "sign" not in lower and "signature" not in lower:
            # flag missing signature blocks as medium severity (demo heuristic)
            issues.append({
                "document": doc_name,
                "section": "Signatory block",
                "issue": "Possible missing signatory or signature section",
                "severity": "Medium",
                "suggestion": "Ensure document contains signatory lines with names, positions, and dates.",
                "citation": "ADGM Companies Regulations 2020"
            })
    # Return issues list (could be empty)
    return issues
