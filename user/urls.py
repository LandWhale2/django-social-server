from django.urls import path
from django.conf.urls import url,include
from rest_framework.urlpatterns import format_suffix_patterns
from user import views
from rest_framework import routers

app_name = 'user'

router = routers.SimpleRouter()
router.register(r'user', views.UserViewSet)
router.register(r'relations', views.RelationViewSet)
router.register(r'persontype', views.PersonTypeViewSet)
router.register(r'persontype/<int:user>', views.PersonTypeViewSet)
# router.register(r'relation', views.relation_list, basename='relations')
# router.register(r'user-photo', views.UserPhotoViewSet)

urlpatterns = [
    path('signup', views.SignUp.as_view(), name='signup'),
    path('relation/<int:to_user>/<str:relation_type>', views.relation_list, name='relations-list'),
    path('relation', views.relation_list, name='relations'),
    path('toprating', views.get_top_rating, name='toprating'),
    path('hobbymatching/<int:user_id>', views.get_matching_hobby, name='hobbymatch'),
    # path('relation', views.RelationViewSet, name='relations'),
    url(r'^', include(router.urls)),
]

urlpatterns = format_suffix_patterns(urlpatterns)