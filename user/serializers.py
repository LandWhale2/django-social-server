from rest_framework import serializers
from .models import User



class UserSerializer(serializers.ModelSerializer):
    # created_by = serializers.CharField(max_length=64, required=False)
    # updated_by = serializers.CharField(max_length=64, required=False)
    email = serializers.EmailField()
    image1 = serializers.ImageField(use_url = True, required=False)
    

    class Meta:
        model = User
        fields = '__all__'
        # extra_kwargs = ['photos']

    def to_internal_value(self, data):
        #POST/PUT 과 같이 데이터변경이있을떄 데이터 저장하기 전에 핸들링 가능한 함수
        ret = super(UserSerializer, self).to_internal_value(data)

        # cipher = AESSipher()
        # ret['password'] = cipher.encrypt_str(ret['password'])

        return ret
    
    def to_representation(self, obj):
        #GET/POST/Put 과 같이 데이터 변경이있고 그이후 data로 접근할떄 값을 변환하여 보여줍니다
        ret = super(UserSerializer, self).to_representation(obj)
        return ret
    
    def validate_email(self, value):
        #이메일이 데이터베이스에 존재하는지 확인함
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("이메일이 이미 존재합니다")
        return value

    def validate_password(self, value):
        #패스워드 8자 이하
        if len(value) < 8:
            raise serializers.ValidationError("패스워드는 최소 %s 자 이상이어야합니다 " % 8)
        return value

    def create(self, validate_data):
        #데이터 저장할때 필요한 과정을 구현합니다
        user = User.objects.create(
            email = validate_data['email'],
            token = validate_data['token'],
        )
        
        
        user.active = True
        user.save()

        return validate_data


# class UserPhotoSerializer(serializers.ModelSerializer):

#   class Meta:
#     model = UserPhoto
#     fields = '__all__'
#     depth = 2
