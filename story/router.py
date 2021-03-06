from rest_framework import routers
from story import views as storyview

#글 주소
router = routers.DefaultRouter()
router.register(r'story/(?P<user_pk>\d+)', storyview.StoryViewset, basename='story')
router.register(r'alarm', storyview.StoryAlarmViewset)