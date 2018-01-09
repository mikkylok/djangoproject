from django.db import models
from django.contrib.auth.models import User
# Create your models here.
'''
class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.EmailField()
'''
class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True, verbose_name=('User'))
    phone = models.CharField(max_length=20)
    avatar = models.ImageField(upload_to='avatar',default='avatar/default-avatar.jpg',max_length=1024,null=True,blank=True)
    is_repairman = models.BooleanField(default=False)
