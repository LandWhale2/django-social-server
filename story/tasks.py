from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from user import models
from django.forms.models import model_to_dict
import json


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'isoformat'):
            return obj.isoformat()
        else:
            return str(obj)
        return json.JSONEncoder.default(self, obj)


from django.core.serializers.json import DjangoJSONEncoder


@shared_task
def hello():
    get_users = models.User.objects.all()[:5].values()
    get_user_list = list()
    for get_user in get_users:
        get_user['created_at'] = str(get_user['created_at'])
        get_user['updated_ay'] = str(get_user['updated_ay'])
        get_user['birthday'] = str(get_user['birthday'])
        get_user_list.append(get_user)
    

    channel_layer=get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'user_0',
        {
            "type": "user_list",
            "userlist": get_user_list,
        }
    )


