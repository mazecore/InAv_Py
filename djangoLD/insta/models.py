from django.db import models

class MyUser(models.Model):
    user_name = models.CharField(max_length=50)
    profile_info = models.CharField(max_length=300)

class Follower(models.Model):
    user_name = models.CharField(max_length=50)
    user_pic = models.CharField(max_length=300)
    MyUser = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    
class Following(models.Model):
    user_name = models.CharField(max_length=50)
    user_pic = models.CharField(max_length=300)
    MyUser = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    
