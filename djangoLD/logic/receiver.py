# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 00:49:35 2019

@author: Ldeezy
"""
import djangoLD.test_file as test_file
from .compulsive_liker import LikerFollower
from .get_followers import FollowingFollowers

def collect(b):

   collectFollowers = FollowingFollowers(b['login'], b['password'], 'followers', b['tag']).getDifferentUserFollowers()
   print('success')
   print('received {}'.format(collectFollowers))
   return collectFollowers
#likes = LikerFollower(test_file.login2, test_file.password2,'nietzsche', 247).likyLiky()

#likes = LikerFollower(test_file.boobslogin, test_file.boobspassword,'sonyalpha', 247).likyLiky()

##followers = FollowingFollowers(test_file.login, test_file.password, 'followers').get_em()
#unfollow = FollowingFollowers(test_file.login2, test_file.password2, 'following').get_unfollowers()

# follow = LikerFollower(test_file.login2, test_file.password2, 'painting', 247).followFollow()

#print('received {}'.format(unfollow))
# print('received {}'.format(unfollowers))
