from django.http import HttpResponse
from django.http import JsonResponse
from . import test_file
from .logic.get_followers import InstaHub
from django.views.decorators.csrf import csrf_exempt
import json

def get_followers(HttpRequest):
    followers = InstaHub(test_file.login, test_file.password).get_followers()
    return JsonResponse(followers, safe=False)

@csrf_exempt
def update(HttpRequest):
    b = json.loads(HttpRequest.body)
    print(b['hello'])
    
    return JsonResponse(b['hello'], safe=False)
