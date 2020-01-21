from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone
# Create your models here.


# class UploadTo:
#     def __init__(self, name):
#         self.name = name


#     def __call__(self ,instance, filename): #파라미터 instance는 User 모델을 의미 filename은 업로드 된 파일의 파일 이름
#         from random import choice
#         import string # string.ascii_letters : ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz
#         # arr = [choice(string.ascii_letters) for _ in range(8)]
#         # pid = ''.join(arr) # 8자리 임의의 문자를 만들어 파일명으로 지정
#         pid = self.name
#         extension = filename.split('.')[-1] # 배열로 만들어 마지막 요소를 추출하여 파일확장자로 지정
#         # file will be uploaded to MEDIA_ROOT/user_<id>/<random>
#         return '%s/%s.%s' % (instance.email, pid, extension)

#     def deconstruct(self):
#         return ('myapp.models.UploadTo', [self.fieldname], {})


def user_path(instance, filename): #파라미터 instance는 Photo 모델을 의미 filename은 업로드 된 파일의 파일 이름
    from random import choice
    import string
    arr = [choice(string.ascii_letters) for _ in range(8)]
    pid = ''.join(arr) # 8자리 임의의 문자를 만들어 파일명으로 지정
    extension = filename.split('.')[-1] # 배열로 만들어 마지막 요소를 추출하여 파일확장자로 지정
    # file will be uploaded to MEDIA_ROOT/user_<id>/<random>
    return '%s/%s.%s' % (instance.email, pid, extension) 



# class UploadTo:
#   def __init__(self, name):
#     self.name = name

#   def __call__(self, instance, filename):
#     return '{}/{}.jpg'.format(instance.email, self.name)

#   def deconstruct(self):
#     return ('user.models.UploadTo', [self.fieldname], {})





class User(models.Model):
    class Meta:
        db_table = "users"
    
    created_at = models.DateTimeField(default = timezone.now)
    updated_ay = models.DateTimeField(auto_now= True)
    email = models.CharField(max_length = 128, unique= True)
    active = models.BooleanField(default=False)
    gender = models.BooleanField(default=False)
    token = models.CharField(max_length= 255, null = True)
    nickname = models.CharField(max_length = 14, null = True)
    school = models.CharField(max_length = 40, null = True)
    intro = models.CharField(max_length = 255, null = True)
    bodytype = ArrayField(models.CharField(max_length=200), blank=True, null=True)
    personality = ArrayField(models.CharField(max_length=200), blank=True, null=True)
    hobby = ArrayField(models.CharField(max_length=200), blank=True, null=True)
    height = models.IntegerField(null=True, blank=True)
    birth = models.IntegerField(null=True, blank=True)
    like = models.IntegerField(null=True, blank=True)
    hate = models.IntegerField(null=True, blank=True)
    image1 = models.ImageField(null= True, blank = True, upload_to = user_path)




# class UserPhoto(models.Model):
#     user = models.ForeignKey(
#             User, related_name='photos', on_delete=models.CASCADE
#         )
#     image = models.ImageField()
#     date_added = models.DateTimeField(auto_now_add=True)