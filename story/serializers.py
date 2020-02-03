from rest_framework import serializers
from . import models
from user.models import User
from user.serializers import UserSerializer, StoryLikeSerializer, UserProfileSerializer
from django.views.decorators.csrf import csrf_exempt


class StorySerializer(serializers.HyperlinkedModelSerializer):
    image = serializers.ImageField(use_url = True, required=False)
    likes = StoryLikeSerializer(many=True,required=False)
    # author = serializers.HyperlinkedIdentityField(view_name='user-detail')
    

    class Meta:
        model = models.Story
        fields = ('content','image', 'created', 'email', 'id', 'likes','user')



class StoryAlarmSerializer(serializers.ModelSerializer):
    nickname = UserProfileSerializer(many=True,required=False)

    class Meta:
        model = models.StoryAlarm
        fields = '__all__'