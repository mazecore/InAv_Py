from django.http import HttpResponse
from django.http import JsonResponse
from . import test_file
from .logic.get_followers import FollowersList

def home(HttpRequest):
    followers = FollowersList(test_file.login, test_file.password).main_function()
    return JsonResponse(followers, safe=False)

