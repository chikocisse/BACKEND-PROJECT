from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Vue du tableau de bord pour un utilisateur authentifié.
        """
        return Response({"message": "Bienvenue sur le tableau de bord!"})
