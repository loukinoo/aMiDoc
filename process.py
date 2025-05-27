# process.py - versione migliorata con pre-elaborazione OCR

from deep_translator import GoogleTranslator
import pytesseract
from PIL import Image
from transformers import pipeline
from pdf2image import convert_from_path
import numpy as np
import cv2
import os

# Configura il path di Tesseract solo se necessario (es. su macOS locale)
pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'


def preprocess_image_cv(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 3)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh


def extract_text_from_image(image_path):
    if image_path.lower().endswith(('.jpeg')):
        text = pytesseract.image_to_string(Image.open(image_path), lang='ita', config='--psm 6')
        return text
    else:
        preprocessed = preprocess_image_cv(image_path)
        temp_path = "temp_preprocessed.png"
        cv2.imwrite(temp_path, preprocessed)
        text = pytesseract.image_to_string(Image.open(temp_path), lang='ita', config='--psm 6')
        os.remove(temp_path)
        return text



def extract_text_from_pdf(pdf_path):
    images = convert_from_path(pdf_path)
    all_text = []
    for i, image in enumerate(images):
        image_path = f"page_{i}.png"
        image.save(image_path)
        text = extract_text_from_image(image_path)
        os.remove(image_path)
        all_text.append(text)
    return "\n".join(all_text)


def process_document(file_path, target_language='it'):
    text = ""
    if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp')):
        text = extract_text_from_image(file_path)
    elif file_path.lower().endswith('.pdf'):
        text = extract_text_from_pdf(file_path)
    else:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()

    print(text)

    if not text.strip():
        return "Nessun testo estratto dal documento."
    
    trans = GoogleTranslator(source='auto', target='en')
    text = trans.translate(text)
    # 2. Analisi NLP per estrazione e riassunto

    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    summary_result = summarizer(text, max_length=150, min_length=30, do_sample=False)
    extracted_summary = summary_result[0]['summary_text']

    final_summary = ["Riassunto Generale:", extracted_summary]


    translator = GoogleTranslator(source='auto', target=target_language)
    translated_summary_parts = []
    for part in final_summary:
        if "Riassunto Generale:" in part:
            translated_summary_parts.append(part)
        else:
            translated_summary_parts.append(translator.translate(part))
    final_summary = translated_summary_parts

    return "\n".join(final_summary)

# Esempio
# print(process_document("documento.pdf", target_language='it'))
