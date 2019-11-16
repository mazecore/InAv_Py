from django.http import HttpResponse
from django.http import JsonResponse
from . import test_file
from .logic.get_followers import InstaHub

def get_followers(HttpRequest):
    followers = InstaHub(test_file.login, test_file.password).get_followers()
    return JsonResponse(followers, safe=False)

def update(HttpRequest):
    return HttpResponse('yo')
