from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('like', views.like),
]

urlpatterns = format_suffix_patterns(urlpatterns)