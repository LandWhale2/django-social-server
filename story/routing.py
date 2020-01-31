from . import consumers
from django.conf.urls import url
from django.urls import re_path

websocket_urlpatterns = [
    re_path(r'ws/alarm/(?P<username>.*)/', consumers.UserConsumer),
]

