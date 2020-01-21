from rest_framework import serializers
from . import models
from user.serializers import UserSerializer



class StorySerializer(serializers.HyperlinkedModelSerializer):
    image = serializers.ImageField(use_url = True, required=False)
    likes = UserSerializer(many=True,required=False)

    class Meta:
        model = models.Story
        fields = ('content','image', 'created', 'email', 'id', 'likes',)