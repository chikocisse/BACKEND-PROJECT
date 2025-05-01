import os
import tempfile
import fitz  # PyMuPDF
import PyPDF2

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.contrib.auth import authenticate, get_user_model

from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, AllowAny, BasePermission
from rest_framework_simplejwt.tokens import RefreshToken

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .models import Submission, PlagiarismCheck
from .serializers import SubmissionSerializer
from .forms import PlagiarismForm
from .utils.extract_text_from_pdf import extract_text_from_pdf
from .ai.corrector import correct_with_ai
from plagiarism_checker.analyze_similarity import analyze_similarity

User = get_user_model()

# -------------------------
# AUTHENTIFICATION
# -------------------------

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        if not username or not password or not email:
            return Response({"error": "Username, email, and password are required."}, status=400)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists."}, status=400)

        if User.objects.filter(email=email).exists():
            return Response({"error": "Email already registered."}, status=400)

        user = User.objects.create_user(username=username, email=email, password=password)
        refresh = RefreshToken.for_user(user)

        return Response({
            "message": "User registered successfully.",
            "user": {"username": user.username, "email": user.email},
            "token": {"refresh": str(refresh), "access": str(refresh.access_token)},
        }, status=201)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'token': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                },
                'user': {
                    'username': user.username,
                    'email': user.email,
                }
            })
        return Response({'error': 'Invalid credentials'}, status=401)

# -------------------------
# PERMISSIONS
# -------------------------

class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'role') and request.user.role == 'teacher'

# -------------------------
# SOUMISSIONS
# -------------------------

class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [IsAuthenticated]

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def correct_submission(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id)
    try:
        grade, feedback = correct_with_ai(submission.submitted_file.path)
        submission.grade = grade
        submission.feedback = feedback
        submission.save()
        return Response({"grade": grade, "feedback": feedback})
    except Exception as e:
        return Response({"error": f"Error during correction: {str(e)}"}, status=500)

# -------------------------
# PLAGIAT
# -------------------------

class PlagiarismCheckView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({"error": "No file provided"}, status=400)

        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp:
                for chunk in file.chunks():
                    temp.write(chunk)
                temp_path = temp.name

            uploaded_text = ""
            with open(temp_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    text = page.extract_text()
                    if text:
                        uploaded_text += text + " "

            if not uploaded_text.strip():
                os.remove(temp_path)
                return Response({'error': 'No text extracted from the PDF.'}, status=400)

            # Analyse avancée via analyze_similarity
            results = analyze_similarity(uploaded_text)
            return Response({'results': results}, status=200)

        except Exception as e:
            return Response({'error': f"Error: {str(e)}"}, status=500)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

# -------------------------
# DEVOIRS / UPLOAD
# -------------------------

@api_view(["POST"])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def submit_homework(request):
    file = request.FILES.get('file')
    if not file:
        return Response({"error": "No file submitted"}, status=400)

    file_name = default_storage.save(file.name, ContentFile(file.read()))
    file_path = os.path.join(default_storage.location, file_name)

    submission = Submission.objects.create(
        submitted_file=file_path,
        user=request.user
    )

    return Response({'message': 'Homework submitted successfully.', 'submission_id': submission.id})

# -------------------------
# UI FORM VIEWS
# -------------------------

def home(request):
    return HttpResponse("Welcome to the home page!")

def check_plagiarism_form(request):
    if request.method == "POST" and request.FILES.get('file'):
        file = request.FILES['file']
        text = extract_text_from_pdf(file)

        plagiarism_check = PlagiarismCheck(file=file, plagiarism_score=0.0)
        plagiarism_check.save()

        return render(request, 'results.html', {'plagiarism_score': 0.0, 'corrected': True})
    else:
        form = PlagiarismForm()
    return render(request, 'check_plagiarism_form.html', {'form': form})

# -------------------------
# DASHBOARD
# -------------------------

class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "Welcome to the dashboard!"})

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "username": user.username,
            "email": user.email,
            "is_staff": user.is_staff,
            "is_superuser": user.is_superuser,
        })
