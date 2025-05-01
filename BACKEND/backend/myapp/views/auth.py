from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model
from .serializers import CustomUserSerializer

User = get_user_model()

class RegisterView(CreateAPIView):
    """
    Permet à un utilisateur de s'enregistrer.
    """
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
