ADGM_CHECKLISTS = {
    "Company Incorporation": [
        "Articles of Association",
        "Memorandum of Association",
        "Incorporation Application Form",
        "UBO Declaration Form",
        "Register of Members and Directors"
    ],
    "Licensing": [
        "Licence Application",
        "Proof of Address",
        "Board Resolution (if applicable)"
    ]
}

def checklist_check(process, detected_docs):
    required = ADGM_CHECKLISTS.get(process, [])
    missing = [d for d in required if d not in detected_docs]
    return {"required_documents": len(required), "missing_documents": missing}
