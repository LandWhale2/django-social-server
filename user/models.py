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
    photo = 'photo'
    return '%s/%s/%s.%s' % (instance.email, photo, pid, extension) 



# class UploadTo:
#   def __init__(self, name):
#     self.name = name

#   def __call__(self, instance, filename):
#     return '{}/{}.jpg'.format(instance.email, self.name)

#   def deconstruct(self):
#     return ('user.models.UploadTo', [self.fieldname], {})




def rating_save():
    return 3



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
    birthday = models.DateField(null=True, blank= True)
    relations = models.ManyToManyField(
        'self',
        # 비대칭 적용
        symmetrical=False,
        # 중개 모델 적용
        through='Relation',
        # 역참조를 없앰
        related_name='+'
    )
    image1 = models.ImageField(null= True, blank = True, upload_to = user_path)
    rating = models.IntegerField(null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    longitude = models.FloatField(null=True)
    latitude = models.FloatField(null=True)
    fcmtoken = models.CharField(max_length= 255, null = True)

    @property
    def age_cal(self):
        import datetime
        return int((datetime.date.today() - self.birthday).days / 365.25)
    
    

    @property
    def like_rating(self):
        like_count = self.relations_by_to_user.filter(
            relation_type=Relation.RELATION_TYPE_LIKE,
        ).count()
        hate_count = self.relations_by_to_user.filter(
            relation_type=Relation.RELATION_TYPE_HATE,
        ).count()

        total_count = like_count + hate_count
        if total_count >= 10:
            rating = like_count / total_count * 100
        else:
            rating = 0
        
        # total_count = like_count+hate_count
        return rating

    @property
    def mylikelist(self):
        """
        내가 좋아하고 있는 User목록 가져옴
        """
        like_relations = self.relations_by_from_user.filter(
            type=Relation.RELATION_TYPE_LIKE,
        )
        # 위에서 정제한 쿼리셋에서 'pk'값만 리스트로 가져옴( 내가 좋아하는 유저의 pk리스트)
        like_pk_list = like_relations.values_list('to_user', flat=True)

        # User테이블에서 pk가 like_pk_list에 포함되는 User목록을
        # like_users변수로 할당
        like_users = User.objects.filter(pk__in=like_pk_list)
        return like_users
    
    
    
    



class Relation(models.Model):
    RELATION_TYPE_LIKE = 'l'
    RELATION_TYPE_BLOCK = 'b'
    RELATION_TYPE_HATE = 'h'
    RELATION_TYPE_CHAT = 'c'
    CHOICES_TYPE = (
        (RELATION_TYPE_LIKE, '좋아요'),
        (RELATION_TYPE_BLOCK, '차단'),
        (RELATION_TYPE_HATE, '싫어요'),
        (RELATION_TYPE_CHAT, '채팅'),
    )
    from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null = True,
        related_name='relations_by_from_user',
    )
    relation_type = models.CharField(max_length=1, choices=CHOICES_TYPE, blank=True)
    to_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null = True,
        related_name='relations_by_to_user',
    )


    class Meta:
        ordering = ['-relation_type']
    





class PersonType(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null = True,
        related_name='person_type_user',
    )
    max_age_type = models.IntegerField(null=True, blank=True)
    min_age_type = models.IntegerField(null=True, blank=True)
    height_max_type = models.IntegerField(null=True, blank=True)
    height_min_type = models.IntegerField(null=True, blank=True)
    personality_type = ArrayField(models.CharField(max_length=30), blank=True, null=True)
    bodytype_type = ArrayField(models.CharField(max_length=200), blank=True, null=True)

    class Meta:
        ordering = ['-id']



class ChattingList(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null = True,
        related_name='chatting_list',
    )
    chttingwith = models.ManyToManyField(User, blank=True,null= True ,related_name='chattingwith')
    class Meta:
        ordering = ['-id']