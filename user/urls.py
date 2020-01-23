from django.urls import path
from django.conf.urls import url,include
from rest_framework.urlpatterns import format_suffix_patterns
from user import views
from rest_framework import routers

app_name = 'user'

router = routers.SimpleRouter()
router.register(r'user', views.UserViewSet)
router.register(r'relation', views.RelationViewSet)
# router.register(r'user-photo', views.UserPhotoViewSet)

urlpatterns = [
    path('signup', views.SignUp.as_view(), name='signup'),
    # path('relation', views.RelationViewSet, name='relations'),
    url(r'^', include(router.urls)),
]

urlpatterns = format_suffix_patterns(urlpatterns)