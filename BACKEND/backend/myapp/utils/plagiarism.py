from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import itertools

def compute_plagiarism_scores(submissions: dict):
    """
    Args:
        submissions (dict): {student_name: texte_extrait_pdf}
    Returns:
        List of tuples: (studentA, studentB, score)
    """
    results = []
    names = list(submissions.keys())
    contents = list(submissions.values())

    vectorizer = TfidfVectorizer().fit_transform(contents)
    similarities = cosine_similarity(vectorizer)

    for i, j in itertools.combinations(range(len(names)), 2):
        score = similarities[i][j]
        results.append((names[i], names[j], round(score, 4)))

    return results
# myapp/utils/plagiarism.py

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def detect_plagiarism(uploaded_text, reference_texts, threshold=0.7):
    documents = reference_texts + [uploaded_text]
    vectorizer = TfidfVectorizer().fit_transform(documents)
    similarity_matrix = cosine_similarity(vectorizer)
    similarities = similarity_matrix[-1][:-1]
    max_similarity = max(similarities)
    is_plagiarism_suspected = max_similarity >= threshold
    return is_plagiarism_suspected, max_similarity
