import re
from PyPDF2 import PdfReader
from bs4 import BeautifulSoup
from docx import Document

def clean_text(text: str) -> str:
    text = re.sub(r'\n\s*\n+', '\n\n', text)
    return '\n'.join(line.strip() for line in text.strip().splitlines())

def strip_html(html_content: str) -> str:
    return BeautifulSoup(html_content, "html.parser").get_text()

def load_resume(file_path: str) -> str:
    if file_path.endswith(".pdf"):
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
        return clean_text(text)
    elif file_path.endswith(".docx"):
        doc = Document(file_path)
        return clean_text("\n".join([para.text for para in doc.paragraphs]))
    else:
        raise ValueError("Unsupported file type: must be .pdf or .docx")
