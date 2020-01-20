from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone
# Create your models here.


class User(models.Model):
    class Meta:
        db_table = "users"
    
    created_at = models.DateTimeField(default = timezone.now)
    updated_ay = models.DateTimeField(auto_now= True)
    email = models.CharField(max_length = 128, unique= True)
    active = models.BooleanField(default=False)
    token = models.CharField(max_length= 255, null = True)
    nickname = models.CharField(max_length = 14, null = True)
    school = models.CharField(max_length = 40, null = True)
    intro = models.CharField(max_length = 255, null = True)
    bodytype = ArrayField(models.CharField(max_length=200), blank=True, null=True)
    personality = ArrayField(models.CharField(max_length=200), blank=True, null=True)
    hobby = ArrayField(models.CharField(max_length=200), blank=True, null=True)
    height = models.IntegerField()
    birth = models.IntegerField()




class UserPhoto(models.Model):
    user = models.ForeignKey(
            User, related_name='photos', on_delete=models.CASCADE
        )
    image = models.ImageField()
    date_added = models.DateTimeField(auto_now_add=True)