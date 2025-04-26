
from django.http import HttpResponse

def tweets_home(request):
    return HttpResponse("Página principal de Tweets")
