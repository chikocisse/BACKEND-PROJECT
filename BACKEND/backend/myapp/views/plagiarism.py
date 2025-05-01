import os
import tempfile
import PyPDF2
from django.http import JsonResponse
from .utils import extract_text_from_pdf
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import PlagiarismCheck

class PlagiarismCheckView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        if not file:
            return Response({"error": "No file provided"}, status=400)

        # Sauvegarde temporaire du fichier
        with open(f"temp_{file.name}", "wb") as temp_file:
            for chunk in file.chunks():
                temp_file.write(chunk)

        # Simuler la détection de plagiat
        result = {"score": 85, "details": ["Matched Text: Example 1", "Matched Text: Example 2"]}

        # Supprimer le fichier temporaire après traitement
        os.remove(f"temp_{file.name}")
        return Response(result, status=200)

def check_plagiarism_form(request):
    if request.method == "POST" and request.FILES['file']:
        file = request.FILES['file']
        text = extract_text_from_pdf(file)
        plagiarism_check = PlagiarismCheck(file=file, plagiarism_score=0.0)
        plagiarism_check.save()
        return render(request, 'results.html', {'plagiarism_score': 0.0, 'corrected': True})
    else:
        form = PlagiarismForm()
    return render(request, 'check_plagiarism_form.html', {'form': form})
