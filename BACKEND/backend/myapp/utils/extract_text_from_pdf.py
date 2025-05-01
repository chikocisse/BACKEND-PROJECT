# myapp/utils/extract_text_from_pdf.py

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
            text += page.extract_text() or ""
    except Exception as e:
        print(f"Erreur lors de l'extraction du texte du PDF : {e}")
    return text.strip()
