from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@shared_task
def hello():
    print('Hello there!~~')
    channel_layer=get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'user_0',
        {
            "type": "user_list",
            "userlist": "ddd",
        }
    )
