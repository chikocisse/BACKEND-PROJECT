from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pdfplumber

def extract_text_from_pdf(pdf_file):
    """
    Extrait le texte d'un fichier PDF en utilisant pdfplumber.
    """
    with pdfplumber.open(pdf_file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

def compute_plagiarism_scores(text1, text2):
    # Créer un vecteur TF-IDF pour les deux textes
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([text1, text2])

    # Calculer la similarité cosinus
    similarity_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])

    # Retourner le score de similarité
    return similarity_matrix[0][0]
