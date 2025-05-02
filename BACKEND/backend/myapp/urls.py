from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Vues pour l'API et les fonctionnalités
from .api_plagiarism import get_all_plagiarism_results
from .ai.views_plagiarism import check_plagiarism
from myapp.views import register_user
from .views import (
    analyze_and_store_plagiarism,
    PlagiarismCheckView,
    check_plagiarism_form,
    DashboardView,
    RegisterView,
    submit_homework,
    upload_file,
    home,
    correct_submission,
    SubmissionViewSet,
    UserProfileView,
)

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# API router pour gérer les soumissions
router = DefaultRouter()
router.register(r'submissions', SubmissionViewSet, basename='submission')

urlpatterns = [
    # 🌐 UI Views (pages classiques)
    path('', home, name='home'),
    path('submit/', submit_homework, name='submit_homework'),
    path('upload/', upload_file, name='upload_file'),
    path('plagiarism/form/', check_plagiarism_form, name='plagiarism_form'),

    # 🧠 API: Plagiat
    path('plagiarism/check/', check_plagiarism, name='check_plagiarism'),
    path('plagiarism/analyze/', analyze_and_store_plagiarism, name='analyze_plagiarism'),
    path('plagiarism/results/', get_all_plagiarism_results, name='plagiarism_results'),
    path('api/plagiarism/', PlagiarismCheckView.as_view(), name='plagiarism_check_api'),

    # 🧑‍💻 Authentification et JWT
    path('auth/', include('django.contrib.auth.urls')),  # Routes Django pour login/logout
    path('api/register/', RegisterView.as_view(), name='register'),  # Enregistrement utilisateur via API
    path('api/register/', register_user, name='register'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # JWT: Obtenir le token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # JWT: Rafraîchir le token

    # 📦 API: Submissions + Dashboard
    path('api/', include(router.urls)),  # Routes automatiques pour SubmissionViewSet
    path('api/correct/<int:submission_id>/', correct_submission, name='correct_submission'),
    path('api/dashboard/', DashboardView.as_view(), name='dashboard'),

    # 📊 Profil utilisateur (API)
    path('api/user/profile/', UserProfileView.as_view(), name='user_profile'),  # Profil utilisateur authentifié
]






