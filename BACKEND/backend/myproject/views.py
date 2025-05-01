from django.http import HttpResponse

def home(request):
    return HttpResponse("Page d'accueil")
