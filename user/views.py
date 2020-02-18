from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserSerializer,RelationSerializer, UserProfileSerializer, PersonTypeSerializer,ChatListSerializer
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import User, Relation, PersonType, ChattingList
from rest_framework import viewsets
from datetime import date



class SignUp(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



from rest_framework.decorators import action
import datetime

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-created_at')
    serializer_class = UserSerializer



class RelationViewSet(viewsets.ModelViewSet):
    queryset = Relation.objects.all()
    serializer_class = RelationSerializer


class PersonTypeViewSet(viewsets.ModelViewSet):
    queryset = PersonType.objects.all()
    serializer_class = PersonTypeSerializer


from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.db.models import Avg, Max


@csrf_exempt
def Sign(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        email = data['email']
        token = data['token']
        if User.objects.filter(email = email, token = token).exists():
            user = User.objects.get(email = email)
            
            serializer = UserSerializer(user)
            return JsonResponse(serializer.data, safe=False)
        user = User.objects.create(
            email = email,
            token = token
        )
        user.save()
        serializer = UserSerializer(user)
        return JsonResponse(serializer.data, safe=False)



@csrf_exempt
def relation_list(request, to_user=None, relation_type=None):
    if request.method == 'GET':
        relation_user_list = Relation.objects.filter(relation_type=relation_type, to_user= to_user)
        serializer = RelationSerializer(relation_user_list, many=True, context={'request': request})
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        user = User.objects.get(pk=data['to_user'])
        user.rating = user.like_rating
        user.save()
        if data['relation_type'] == "l":
            if Relation.objects.filter(to_user= data['to_user'], from_user = data['from_user']).exists():
                #이미 좋아요 한 유저, 취소함
                Relation.objects.filter(to_user= data['to_user'], from_user = data['from_user']).delete()
            else:
                if Relation.objects.filter(relation_type='l', to_user= data['from_user'], from_user=data['to_user']).exists():
                # 둘다 좋아하면 채팅
                    if ChattingList.objects.filter(author = data['to_user']).exists():
                        chatting_user = ChattingList.objects.get(author = data['to_user'])
                        chatting_user.chttingwith.add(data['from_user'])
                    else:
                        get_user = User.objects.get(pk =data['to_user'])
                        ChattingList.objects.create(
                            author=get_user
                        ).chttingwith.add(data['from_user'])

                    if ChattingList.objects.filter(author = data['from_user']).exists():
                        chatting_user = ChattingList.objects.get(author = data['from_user'])
                        chatting_user.chttingwith.add(data['to_user'])
                    else:
                        get_user = User.objects.get(pk =data['from_user'])
                        ChattingList.objects.create(
                            author=get_user
                        ).chttingwith.add(data['to_user'])

        serializer = RelationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)



def get_top_rating(request, user_id = None):
    if request.method == 'GET':
        get_user = User.objects.get(pk = user_id)
        gender = get_user.gender
        get_user = User.objects.filter(gender = not gender).order_by('-rating')[:10]
        serializer = UserProfileSerializer(get_user, many=True)
        return JsonResponse(serializer.data, safe=False)





def get_matching_hobby(request, user_id=None):
    if request.method == 'GET':
        user = User.objects.get(pk=user_id)
        hobby = user.hobby
        get_user = User.objects.filter(hobby__overlap= hobby, gender=not user.gender).exclude(id=user_id)
        get_user2 = User.objects.none()

        if get_user.count() > 2:
            get_user_2 = get_user.filter(hobby__contained_by= hobby)
            serializer = UserProfileSerializer(get_user2, many=True)
            if get_user_2.count() > 2:
                get_user_3 = get_user_2.filter(hobby__contains = hobby)
                serializer = UserProfileSerializer(get_user3, many=True)
                if get_user_3.count() <= 2:
                    serializer = UserProfileSerializer(get_user2, many=True)
            else:
                serializer = UserProfileSerializer(get_user, many=True)
        else:
            serializer = UserProfileSerializer(get_user, many=True)
        
        
        
        
        return JsonResponse(serializer.data, safe=False)



def get_matching_type(request, user_id=None):
    if request.method == 'GET':
        user_type = PersonType.objects.get(user=user_id)
        user = User.objects.get(pk = user_id)
        
        get_user_age = User.objects.filter(age__range = (user_type.min_age_type, user_type.max_age_type))
        get_user_height = get_user_age.filter(height__range = (user_type.height_min_type, user_type.height_max_type))
        
        
        # get_user = User.objects.filter(bodytype__overlap= user_type.bodytype_type).exclude(id=user_id)
        # if get_user.count() > 2:
        #     get_user2 = get_user.filter(personality__overlap=)
        serializer = UserProfileSerializer(get_user_height, many=True)
        return JsonResponse(serializer.data, safe=False)


def get_chatting_list(request, user_id=None):
    if request.method == 'GET':
        get_chatting_list = ChattingList.objects.filter(author = user_id)

        serializer = ChatListSerializer(get_chatting_list, many=True)
        return JsonResponse(serializer.data, safe=False)


from django.contrib.gis.geos import *
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance

def get_location_type_list(request, user_id = None):
    if request.method == 'GET':
        distance = 5000
        user_get = User.objects.get(pk= user_id)
        longitude = user_get.longitude
        latitude = user_get.latitude
        gender = user_get.gender
        
        ref_location = Point(longitude, latitude)

        res = User.objects.filter(location__distance_lte=(ref_location, D(m=distance)), gender= not gender).order_by('location')
        
        serializer = UserProfileSerializer(res, many=True)
        return JsonResponse(serializer.data, safe=False)



def random_people_list(request, user_id=None):
    if request.method == 'GET':
        user_get = User.objects.get(pk= user_id)
        gender = user_get.gender

        user_list = User.objects.filter(gender= not gender).order_by('?')[:5]
        
        serializer = UserProfileSerializer(user_list, many=True)
        return JsonResponse(serializer.data, safe=False)




# def delete(self, *args, **kwargs):
#     # You have to prepare what you need before delete the model
#     storage, path = self.image.storage, self.image.path
#     # Delete the model before the file
#     super(Profile, self).delete(*args, **kwargs)
#     # Delete the file after the model
#     storage.delete(path)