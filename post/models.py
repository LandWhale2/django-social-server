from django.db import models
from user.models import User

# Create your models here.

def image_path(instance, filename): #파라미터 instance는 Photo 모델을 의미 filename은 업로드 된 파일의 파일 이름
    from random import choice
    import string
    arr = [choice(string.ascii_letters) for _ in range(8)]
    pid = ''.join(arr) # 8자리 임의의 문자를 만들어 파일명으로 지정
    extension = filename.split('.')[-1] # 배열로 만들어 마지막 요소를 추출하여 파일확장자로 지정
    # file will be uploaded to MEDIA_ROOT/user_<id>/<random>
    return '%s/%s.%s' % (instance.email, pid, extension) 



class Story(models.Model):
    created = models.DateTimeField(auto_now_add= True)
    content = models.CharField(max_length = 255, null = True)
    email =  models.CharField(max_length = 255, null = True)
    author = models.ForeignKey(User, on_delete= models.CASCADE, null = True, related_name='storys')
    image = models.ImageField(null= True, blank = True, upload_to= image_path)
    likes = models.ManyToManyField(User, blank=True,null= True ,related_name='likes')
    
    class Meta:
        abstract = True
        ordering = ['-id']
    
    @property
    def total_likes(self):
        return self.likes.count()




class ETC(models.Model):
    created = models.DateTimeField(auto_now_add= True)

    class Meta:
        abstract = True