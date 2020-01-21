from django.shortcuts import render
from . import models
from . import serializers
from rest_framework import viewsets
# Create your views here.



class StoryViewset(viewsets.ModelViewSet):
    queryset = models.Story.objects.all()
    serializer_class = serializers.StorySerializer