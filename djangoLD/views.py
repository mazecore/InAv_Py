from django.http import HttpResponse
from django.http import JsonResponse
from . import test_file
from .logic.get_followers import FollowingFollowers
from .logic.compulsive_liker import LikerFollower
from django.views.decorators.csrf import csrf_exempt
import json

def get_followers(HttpRequest):
    followers = FollowingFollowers(test_file.login, test_file.password, 'following').get_em()
    return JsonResponse(followers, safe=False)

@csrf_exempt
def update(HttpRequest):
    
    b = json.loads(HttpRequest.body)
    liked_urls = LikerFollower(test_file.login2, test_file.password2,b['tag'], b['numberOfLikes']).likyLiky()

    #likes = LikerFollower(test_file.boobslogin, test_file.boobspassword,'sonyalpha', 247).likyLiky()
    print(b)
    return JsonResponse({"urls": liked_urls})
