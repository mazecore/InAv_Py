# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 00:49:35 2019

@author: Ldeezy
"""
import test_file
from compulsive_liker import LikerFollower
from get_followers import FollowingFollowers

# likes = LikerFollower(test_file.login2, test_file.password2, 'art', 247).likyLiky()
unfollowers = FollowingFollowers(test_file.login, test_file.password, 'followers').get_unfollowers()
#followers = FollowingFollowers(test_file.login, test_file.password, 'followers').get_em()
#following = FollowingFollowers(test_file.login, test_file.password, 'following').get_em()
print('success')
#print('received {}'.format(likes))
print('received {}'.format(unfollowers))