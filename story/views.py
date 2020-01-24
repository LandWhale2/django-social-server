from django.shortcuts import render
from . import models
from . import serializers
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
    queryset = models.Story.objects.all()
    serializer_class = serializers.StorySerializer





@require_POST
@csrf_exempt
def like(request):
    if request.method == 'POST':
        ds = json.loads(request.body)
        user = ds['userid']
        postid = ds['postid']

        story = models.Story.objects.get(id = postid)
        
        if story.likes.filter(id = user).exists():
            story.likes.remove(user)
            message = "좋아요가 취소되었습니다"
        else:
            story.likes.add(user)
            message = "이글을 좋아합니다"

    context = {'like_count' : story.total_likes, 'message': message}
    return HttpResponse(json.dumps(context), content_type='application/json')



class TestModelViewset(viewsets.ModelViewSet):
    queryset = models.TestModel.objects.all()
    serializer_class = serializers.TestModelSerializer