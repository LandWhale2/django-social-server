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
    serializer_class = serializers.StorySerializer

    def get_queryset(self):
        user = models.User.objects.get(pk = self.kwargs['user_pk'])
        story = models.Story.objects.filter(gender = not user.gender)
        return story


class StoryAlarmViewset(viewsets.ModelViewSet):
    queryset = models.StoryAlarm.objects.all()
    serializer_class = serializers.StoryAlarmSerializer


import requests
import json


def send_fcm_notification(ids, title, body):
    # fcm 푸시 메세지 요청 주소
    url = 'https://fcm.googleapis.com/fcm/send'
    
    # 인증 정보(서버 키)를 헤더에 담아 전달
    headers = { 
        'Authorization': 'key=AAAACekWIbs:APA91bG-VeoSEYHSLX6jSP7_RZJRgcNj4MmgFOZq6RBhG1XAukDGbfVkFhKsyueOjuQ80_rO0hp0m_W8a3dr2LQpdOXLwhyLl4EZm9Uw8LxGIZG1jlyeG3-jvyOq5hTIIdEPF7eR3yjk',
        'Content-Type': 'application/json; UTF-8',
    }
    

    # 보낼 내용과 대상을 지정
    content = {
        'to': ids,
        'notification': {
            'title': title,
            'body': body
        }
    }

    # json 파싱 후 requests 모듈로 FCM 서버에 요청
    response = requests.post(url, data=json.dumps(content), headers=headers)




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
        story_user_get = User.objects.get(id = story_user_id)
        stroy_user_fcmtoken = story_user_get.fcmtoken
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
                send_fcm_notification(stroy_user_fcmtoken, '누카', '누군가가 스토리에 좋아요를 눌렀습니다')
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
            
            send_fcm_notification(stroy_user_fcmtoken, '누카', '누군가가 스토리에 좋아요를 눌렀습니다')
            


    context = {'like_count' : story.total_likes, 'message': message}
    return HttpResponse(json.dumps(context), content_type='application/json')



from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse


def StoryAlarmList(request, user_id=None):
    if request.method == 'GET':
        
        get_alarm = models.StoryAlarm.objects.filter(author = user_id)
        

        serializer = serializers.StoryAlarmSerializer(get_alarm, many=True)
        return JsonResponse(serializer.data, safe=False)