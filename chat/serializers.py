from user.models import User
from rest_framework import serializers
from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    """For Serializing Message"""
    sender = serializers.SlugRelatedField(many=False, slug_field='nickname', queryset=User.objects.all())
    receiver = serializers.SlugRelatedField(many=False, slug_field='nickname', queryset=User.objects.all())
    class Meta:
        model = Message
        fields = ['sender', 'receiver', 'message', 'timestamp']


