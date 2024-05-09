"""This script extracts fields from the pdf and scanned pdf files.
It's compiled by Phala Mathobela"""

import re
import PyPDF2
import pdfplumber
import pytesseract
from PIL import Image


def extract_fields_from_pdf(pdf_file):
    try:
        # Attempt to extract text using PyPDF2
        with open(pdf_file, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            extracted_text = ''
            for page in pdf_reader.pages:
                extracted_text += page.extract_text()
        return extract_fields_from_text(extracted_text)
    except PyPDF2.PdfReadError:
        # If PyPDF2 fails (possibly scanned document), use Tesseract OCR
        return extract_fields_from_scanned_pdf(pdf_file)


def extract_fields_from_text(text):
    # Extract fields using regular expressions
    name_match = re.search(r'Name:\s*(.*)', text)
    surname_match = re.search(r'Surname:\s*(.*)', text)
    policy_number_match = re.search(r'Policy Number:\s*(.*)', text)
    address_match = re.search(r'Address:\s*(.*)', text)

    # Get values from matches
    name = name_match.group(1) if name_match else None
    surname = surname_match.group(1) if surname_match else None
    policy_number = policy_number_match.group(1) if policy_number_match else None
    address = address_match.group(1) if address_match else None

    return {
        'Name': name,
        'Surname': surname,
        'Policy Number': policy_number,
        'Address': address
    }


def extract_fields_from_scanned_pdf(pdf_file):
    text = ''
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            for image in page.images:
                img = Image.open(image["stream"])
                extracted_text = pytesseract.image_to_string(img)
                text += extracted_text
    return extract_fields_from_text(text)

pdf_text = extract_fields_from_pdf('C:/Users/Phala/Desktop/SAVIKA_Test.pdf')
print(pdf_text)