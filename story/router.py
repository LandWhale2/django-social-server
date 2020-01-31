from rest_framework import routers
from story import views as storyview

#글 주소
router = routers.DefaultRouter()
router.register(r'story', storyview.StoryViewset)
router.register(r'alarm', storyview.StoryAlarmViewset)