from django.urls import path
from .views.correction import correct_submission
from .views.plagiarism import PlagiarismCheckView, check_plagiarism_form
from .views.auth import RegisterView
from .views.dashboard import DashboardView
from rest_framework.routers import DefaultRouter
from .views.submission import SubmissionViewSet

router = DefaultRouter()
router.register(r'submissions', SubmissionViewSet)

urlpatterns = [
    path('correct_submission/<int:submission_id>/', correct_submission, name='correct_submission'),
    path('plagiarism-check/', PlagiarismCheckView.as_view(), name='plagiarism_check'),
    path('register/', RegisterView.as_view(), name='register'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('check_plagiarism_form/', check_plagiarism_form, name='check_plagiarism_form'),
] + router.urls
