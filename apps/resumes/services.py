import pdfplumber
from docx import Document
import re


def extract_text_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text


def extract_text_from_docx(file_path):
    doc = Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])


def extract_basic_details(text):
    """
    Very basic parsing (we will improve later)
    """

    # Email
    email = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    email = email[0] if email else None

    # Skills (simple keyword match)
    skills_list = ["python", "django", "sql", "java", "aws"]
    found_skills = [skill for skill in skills_list if skill.lower() in text.lower()]

    return {
        "email": email,
        "skills": found_skills,
    }


def parse_resume(file_path, file_type):
    if "pdf" in file_type:
        text = extract_text_from_pdf(file_path)
    else:
        text = extract_text_from_docx(file_path)

    data = extract_basic_details(text)

    return data