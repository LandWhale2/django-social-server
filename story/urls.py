from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('like', views.like),
    path('storyalarmlist/<int:user_id>', views.StoryAlarmList, name='storyalarmlist'),
]

urlpatterns = format_suffix_patterns(urlpatterns)