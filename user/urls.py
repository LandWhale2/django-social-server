from django.urls import path
from django.conf.urls import url,include
from rest_framework.urlpatterns import format_suffix_patterns
from user import views
from rest_framework import routers

app_name = 'user'

router = routers.SimpleRouter()
router.register(r'user', views.UserViewSet)    
# router.register(r'user-photo', views.UserPhotoViewSet)

urlpatterns = [
    path('signup', views.SignUp.as_view(), name='signup'),
    url(r'^', include(router.urls)),
    # path('signin', views.SignIn.as_view(), name='signin'),
    # path('check', views.EmailCheckView.as_view(), name='check'),
    # path('activate/<str:uidb64>/<str:token>', views.UserActivate.as_view(), name="activate"),
    # path('userupdate', views.userupdate, name="userupdate"),
]

urlpatterns = format_suffix_patterns(urlpatterns)