from django.db import models
from user.models import User
from django.utils import timezone


# Create your models here.

class Message(models.Model):
     sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='senders')        
     receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receivers')        
     message = models.CharField(max_length=1200)
     timestamp = models.DateTimeField(auto_now_add=True)
     is_read = models.BooleanField(default= False)
     def __str__(self):
           return self.message
     class Meta:
           ordering = ('-timestamp',)