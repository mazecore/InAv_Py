# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 00:49:35 2019

@author: Ldeezy
"""
import test_file
from compulsive_liker import InstaHub

followers = InstaHub(test_file.login, test_file.password).likyLiky()
print('success')
print('received {}'.format(followers))