from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from myapp.ai.corrector import correct_with_ai  # Tu dois créer ce module
from .models import Submission

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def correct_submission(request, submission_id):
    """
    Corrige une soumission d'un étudiant via l'IA, en attribuant une note et des commentaires.
    """
    submission = get_object_or_404(Submission, id=submission_id)
    grade, feedback = correct_with_ai(submission.submitted_file.path)
    submission.grade = grade
    submission.feedback = feedback
    submission.save()
    return Response({"grade": grade, "feedback": feedback})
