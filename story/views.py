from django.shortcuts import render
from . import models
from . import serializers
from user.models import User
from rest_framework import viewsets
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
try:
    from django.utils import simplejson as json
except ImportError:
    import json
# Create your views here.



class StoryViewset(viewsets.ModelViewSet):
    queryset = models.Story.objects.all()
    serializer_class = serializers.StorySerializer


class StoryAlarmViewset(viewsets.ModelViewSet):
    queryset = models.StoryAlarm.objects.all()
    serializer_class = serializers.StoryAlarmSerializer


import datetime

@require_POST
@csrf_exempt
def like(request):
    if request.method == 'POST':
        ds = json.loads(request.body)
        user = ds['userid']
        postid = ds['postid']

        story = models.Story.objects.get(id = postid)
        
        if story.likes.filter(id = user).exists():
            story.likes.remove(user)
            message = "좋아요가 취소되었습니다"
        else:
            story.likes.add(user)
            message = "이글을 좋아합니다"
        

        

        if models.StoryAlarm.objects.filter(message = story.content).exists():
            alarm = models.StoryAlarm.objects.get(message = story.content)
            if alarm.nickname.filter(id = user).exists():
                alarm.nickname.remove(user)
                alarm.updated_ay = datetime.datetime.now()
                
            else:
                alarm.nickname.add(user)
                alarm.updated_ay = datetime.datetime.now()
                
        else:
            user_get = User.objects.get(pk= user)
            alarm_user_id = story.user
            alarm = models.StoryAlarm.objects.create(
                message = story.content,
                author_id = alarm_user_id,
            )
            alarm.nickname.add(user)
        
        alarm.save()

        


    context = {'like_count' : story.total_likes, 'message': message}
    return HttpResponse(json.dumps(context), content_type='application/json')



