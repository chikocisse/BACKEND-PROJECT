# myapp/utils/pdf_utils.py

from PyPDF2 import PdfReader

def extract_text_from_pdf(file_path):
    """
    Extrait le texte brut d'un fichier PDF.
    :param file_path: chemin vers le fichier PDF
    :return: texte extrait (str)
    """
    text = ""
    try:
        reader = PdfReader(file_path)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    except Exception as e:
        print(f"Erreur lors de l'extraction du texte du PDF : {e}")
    return text.strip()
