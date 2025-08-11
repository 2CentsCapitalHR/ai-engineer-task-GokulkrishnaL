
from docx import Document
from lxml import etree
from zipfile import ZipFile
import shutil
import zipfile
from pathlib import Path
import uuid

NSMAP = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
}

def insert_comments(input_path, issues, output_path):
    """
    Insert Word comments at paragraph level where issues are found.
    The comment text includes issue, suggestion, and citation.
    """
    # Save a working copy
    shutil.copyfile(input_path, output_path)
    temp_dir = Path(str(output_path) + "_unzip")
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    temp_dir.mkdir()
    # Unzip docx
    with ZipFile(output_path, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)

    # Load document.xml
    doc_xml_path = temp_dir / "word" / "document.xml"
    doc_tree = etree.parse(str(doc_xml_path))
    doc_root = doc_tree.getroot()

    # Create comments.xml if not exists
    comments_path = temp_dir / "word" / "comments.xml"
    if comments_path.exists():
        comments_tree = etree.parse(str(comments_path))
        comments_root = comments_tree.getroot()
    else:
        comments_root = etree.Element("{%s}comments" % NSMAP['w'], nsmap=NSMAP)
        comments_tree = etree.ElementTree(comments_root)

    # Determine starting cmt_id
    existing_ids = [int(c.get("{%s}id" % NSMAP['w'])) for c in comments_root.findall("w:comment", NSMAP) if c.get("{%s}id" % NSMAP['w']).isdigit()]
    cmt_id = max(existing_ids) + 1 if existing_ids else 0

    # For each issue, add comment and link to paragraph
    for issue in issues:
        # Build comment text
        comment_text = f"Issue: {issue.get('issue')}\nSuggestion: {issue.get('suggestion')}\nCitation: {issue.get('citation')}"
        # Create comment element
        cmt = etree.Element("{%s}comment" % NSMAP['w'], nsmap=NSMAP)
        cmt.set("{%s}id" % NSMAP['w'], str(cmt_id))
        cmt.set("{%s}author" % NSMAP['w'], "ADGM Corporate Agent")
        cmt.set("{%s}date" % NSMAP['w'], "2025-08-11T00:00:00Z")
        p = etree.Element("{%s}p" % NSMAP['w'])
        r = etree.SubElement(p, "{%s}r" % NSMAP['w'])
        t = etree.SubElement(r, "{%s}t" % NSMAP['w'])
        t.text = comment_text
        cmt.append(p)
        comments_root.append(cmt)

        # Attach to first matching paragraph containing section or doc name
        for para in doc_root.findall(".//w:p", NSMAP):
            para_text = "".join(para.xpath(".//w:t/text()", namespaces=NSMAP)).strip()
            if issue.get("section") and issue["section"].lower() in para_text.lower():
                start = etree.Element("{%s}commentRangeStart" % NSMAP['w'])
                start.set("{%s}id" % NSMAP['w'], str(cmt_id))
                end = etree.Element("{%s}commentRangeEnd" % NSMAP['w'])
                end.set("{%s}id" % NSMAP['w'], str(cmt_id))
                ref = etree.Element("{%s}r" % NSMAP['w'])
                cref = etree.SubElement(ref, "{%s}commentReference" % NSMAP['w'])
                cref.set("{%s}id" % NSMAP['w'], str(cmt_id))
                para.insert(0, start)
                para.append(end)
                para.append(ref)
                break
        cmt_id += 1

    # Save updated comments.xml
    comments_tree.write(str(comments_path), xml_declaration=True, encoding="UTF-8", standalone="yes")

    # Add relationship in document.xml.rels to comments.xml if missing
    rels_path = temp_dir / "word" / "_rels" / "document.xml.rels"
    rels_tree = etree.parse(str(rels_path))
    rels_root = rels_tree.getroot()
    has_comment_rel = any("comments.xml" in r.get("Target") for r in rels_root.findall("{%s}Relationship" % NSMAP['w'].replace('/wordprocessingml/2006/main','/package/2006/relationships')))
    if not has_comment_rel:
        # Relationship NS for .rels
        rels_ns = "http://schemas.openxmlformats.org/package/2006/relationships"
        rel = etree.Element("{%s}Relationship" % rels_ns)
        rel.set("Id", "rId" + str(uuid.uuid4())[:8])
        rel.set("Type", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/comments")
        rel.set("Target", "comments.xml")
        rels_root.append(rel)
        rels_tree.write(str(rels_path), xml_declaration=True, encoding="UTF-8", standalone="yes")

    # Save document.xml
    doc_tree.write(str(doc_xml_path), xml_declaration=True, encoding="UTF-8", standalone="yes")

    # Zip back into output_path
    with ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as docx_zip:
        for file in temp_dir.rglob("*"):
            docx_zip.write(file, file.relative_to(temp_dir))

    shutil.rmtree(temp_dir)
