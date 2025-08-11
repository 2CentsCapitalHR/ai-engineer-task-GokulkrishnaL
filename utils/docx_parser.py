from zipfile import ZipFile
from pathlib import Path
import xml.etree.ElementTree as ET

def extract_text_from_docx(path):
    """
    Lightweight text extraction from a .docx by reading word/document.xml.
    Works for simple docx files produced by this demo.
    """
    try:
        with ZipFile(path) as z:
            with z.open("word/document.xml") as docxml:
                tree = ET.parse(docxml)
                root = tree.getroot()
                ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
                paragraphs = []
                for p in root.findall(".//w:p", ns):
                    texts = [t.text for t in p.findall(".//w:t", ns) if t.text]
                    if texts:
                        paragraphs.append("".join(texts))
                return "\\n".join(paragraphs)
    except Exception:
        # fallback: return filename as minimal content
        return Path(path).stem
