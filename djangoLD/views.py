from django.http import HttpResponse
from django.http import JsonResponse
from . import test_file
from .logic.get_followers import FollowingFollowers
from .logic.compulsive_liker import LikerFollower
from django.views.decorators.csrf import csrf_exempt
from .logic import receiver
import json

def get_followers(HttpRequest):
    followers = FollowingFollowers(test_file.login, test_file.password, 'following').get_em()
    return JsonResponse(followers, safe=False)

@csrf_exempt
def like_tags(HttpRequest):
    
    b = json.loads(HttpRequest.body)
    
    response = LikerFollower(b['login'], b['password'], b['tag'], b['numberOfLikes']).likyLiky()
    # if response['error']:
    #     return JsonResponse({'status':'false','message':response['message']}, status=401)
    return JsonResponse(response)

@csrf_exempt
def like_followers(HttpRequest):
    
    b = json.loads(HttpRequest.body)
    
    response = LikerFollower(b['login'], b['password'], b['tag'], b['numberOfLikes']).likeAnothersFollowers()
    if response['error']:
        return JsonResponse({'status':'false','message':response['message']}, status=500)
    return JsonResponse(response)

@csrf_exempt
def collect(HttpRequest):
    
    b = json.loads(HttpRequest.body)
    
    response = receiver.collect(b)
    if response['error']:
        return JsonResponse({'status':'false','message':response['message']}, status=500)
    return JsonResponse(response, safe=False)

@csrf_exempt
def collect_photos(HttpRequest):
    
    b = json.loads(HttpRequest.body)
    
    response = LikerFollower(b['login'], b['password'], b['tag'], b['numberOfLikes'], b['shutDown']).collectFirstPhotosOfFollowers()
    if response['error']:
        return JsonResponse({'status':'false','message':response['message']}, status=500)
    return JsonResponse(response)

@csrf_exempt
def stop_collection(HttpRequest):
    
    with open('stopper.json', 'w') as file:
        json.dump({"manual_stop" : True}, file)
    return HttpResponse(200)