from rest_framework import viewsets
from .models import Submission
from .serializers import SubmissionSerializer

class SubmissionViewSet(viewsets.ModelViewSet):
    """
    API CRUD pour les soumissions d'étudiants.
    """
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
