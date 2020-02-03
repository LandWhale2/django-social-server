from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from .models import StoryAlarm
import datetime

# @receiver(post_save, sender=StoryAlarm)
# def announce_likes(sender, instance,**kwargs):
#     print(instance.nickname.all()[0].nickname)
    
    
    
#     if kwargs['created']:
#         channel_layer=get_channel_layer()
#         async_to_sync(channel_layer.group_send)(
#             'user_'+ str(instance.author.pk),
#             {
#                 "type": "share_message",
#                 "message": instance.message,
#                 "updated_ay" : str(instance.updated_ay),
#                 # "nickname" : instance.nickname,
#             }
#         )
#     else:
#         channel_layer=get_channel_layer()
#         async_to_sync(channel_layer.group_send)(
#             'user_'+ str(instance.author.pk),
#             {
#                 "type": "share_message",
#                 "message": instance.message,
#                 "updated_ay" : str(instance.updated_ay),
#                 # "nickname" : instance.nickname,
#             }
#         )
        


class UserConsumer(WebsocketConsumer):

    def connect(self):
        
        self.groupname= self.scope['url_route']['kwargs']['username']
        self.alarm_name = 'user_' + self.groupname
        self.accept()

        async_to_sync(self.channel_layer.group_add)(
            self.alarm_name,
            self.channel_name
        )

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.alarm_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        async_to_sync(self.channel_layer.group_send)(
            self.alarm_name,
            {
                'type': 'share_message',
                'message': message,
            }
        )

    # Receive message from room group
    def share_message(self, event):
        message = event['message']
        updated_ay = event['updated_ay']
        nickname = event['nickname']
        like_counts = event['like_counts']
        
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            "updated_ay" : updated_ay,
            "nickname" : nickname,
            "like_counts" :like_counts
        }))