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
    
    response = LikerFollower(b['login'], b['password'], b['tag'], b['numberOfLikes']).likyLiky()
    # if response['error']:
    #     return JsonResponse({'status':'false','message':response['message']}, status=401)
    return JsonResponse(response)
