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
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.forms.models import model_to_dict
import json

@require_POST
@csrf_exempt
def like(request):
    if request.method == 'POST':
        ds = json.loads(request.body)
        user = ds['userid']
        postid = ds['postid']

        story = models.Story.objects.get(id = postid)
        story_user_id = story.user
        story_message = story.content
        alarm_name = 'user_' + str(story_user_id)
        user_get = User.objects.get(pk= user)
        peer_nickname = user_get.nickname
        
        
        if story.likes.filter(id = user).exists():
            story.likes.remove(user)
            message = "좋아요가 취소되었습니다"
        else:
            story.likes.add(user)
            message = "이글을 좋아합니다"
        



        
        if models.StoryAlarm.objects.filter(message = story_message).exists():
            alarm = models.StoryAlarm.objects.get(message = story_message)
            #알림 모델에 해당 유저가 존재하는지 확인함, 확인후 없으면 추가
            if alarm.nickname.filter(id = user).exists():
                alarm.nickname.remove(user)
                alarm.updated_ay = datetime.datetime.now()    
            else:
                alarm.nickname.add(user)
                alarm.updated_ay = datetime.datetime.now()
            #소켓
            if alarm.nickname.count() == 0:
                # 만약 모든 유저가 좋아요를 취소한다면, 에러를 발생시켜 소켓을 보내지않음
                alarm.delete()
            else:
                channel_layer=get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    alarm_name,
                    {
                        "type": "share_message",
                        "message": story_message,
                        "updated_ay" : str(datetime.datetime.now()),
                        "nickname" : peer_nickname,
                        "like_counts": alarm.nickname.count(),
                    }
                )
                alarm.save()

                
        else:
            
            #최초 알람 모델 생성
            alarm = models.StoryAlarm.objects.create(
                message = story_message,
                author_id = story_user_id,
            ).nickname.add(user)
            
            #소켓
            channel_layer=get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                alarm_name,
                {
                    "type": "share_message",
                    "message": story_message,
                    "updated_ay" : str(datetime.datetime.now()),
                    "nickname" : peer_nickname,
                    "like_counts" : 1
                }
            )
            


    context = {'like_count' : story.total_likes, 'message': message}
    return HttpResponse(json.dumps(context), content_type='application/json')



from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse


def StoryAlarmList(request, user_id=None):
    if request.method == 'GET':
        
        get_alarm = models.StoryAlarm.objects.filter(author = user_id)
        

        serializer = serializers.StoryAlarmSerializer(get_alarm, many=True)
        return JsonResponse(serializer.data, safe=False)