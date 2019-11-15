# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 00:49:35 2019

@author: Ldeezy
"""
from djangoLD import test_file
from get_followers import FollowersList

followers = FollowersList(test_file.login, test_file.password).main_function()
print('success')
print('received {}'.format(followers))