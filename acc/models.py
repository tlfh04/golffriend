from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    rank = models.TextField(max_length=10)
    age = models.IntegerField(default=0)
    salary = models.IntegerField(blank=True, null=True)
    sell_count = models.IntegerField(default=0,blank=True, null=True)
    pic = models.ImageField(upload_to="user/%y")

    def getpic(self):
        if self.pic:
            return self.pic.url
        return "/media/noimage.png"