# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 00:49:35 2019

@author: Ldeezy
"""
import test_file
from compulsive_liker import LikerFollower

likes = LikerFollower(test_file.login2, test_file.password2, 'Nietzsche', 100).likyLiky()
print('success')
print('received {}'.format(likes))