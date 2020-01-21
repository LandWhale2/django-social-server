from django.urls import path
from story import views
from rest_framework.urlpatterns import format_suffix_patterns



urlpatterns = [
    path('story', views.StoryViewset, name='storys'),
]

urlpatterns = format_suffix_patterns(urlpatterns)