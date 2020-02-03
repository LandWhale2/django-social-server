from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from .models import StoryAlarm

@receiver(post_save, sender=StoryAlarm)
def announce_likes(sender, instance,**kwargs):
    print('user_'+ str(instance.author.pk))
    if kwargs['created']:
        channel_layer=get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'user_'+ str(instance.author.pk),
            {
                "type": "share_message",
                "message": instance.message,
            }
        )
    else:
        channel_layer=get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'user_'+ str(instance.author.pk),
            {
                "type": "share_message",
                "message": instance.message,
            }
        )
        


class UserConsumer(WebsocketConsumer):

    def connect(self):
        
        self.groupname= self.scope['url_route']['kwargs']['username']
        self.alarm_name = 'user_' + self.groupname
        print(self.alarm_name)
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
                'message': message
            }
        )

    # Receive message from room group
    def share_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))