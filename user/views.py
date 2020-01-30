from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserSerializer,RelationSerializer, UserProfileSerializer, PersonTypeSerializer
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import User, Relation, PersonType
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
    queryset = User.objects.all()
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
        serializer = RelationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)



def get_top_rating(request):
    if request.method == 'GET':
        get_user = User.objects.all().order_by('-rating')[:10]
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
        
        get_user = User.objects.filter(birthday__year = 1996)
        
        # get_user = User.objects.filter(bodytype__overlap= user_type.bodytype_type).exclude(id=user_id)
        # if get_user.count() > 2:
        #     get_user2 = get_user.filter(personality__overlap=)
        serializer = UserProfileSerializer(get_user, many=True)
        return JsonResponse(serializer.data, safe=False)




# def delete(self, *args, **kwargs):
#     # You have to prepare what you need before delete the model
#     storage, path = self.image.storage, self.image.path
#     # Delete the model before the file
#     super(Profile, self).delete(*args, **kwargs)
#     # Delete the file after the model
#     storage.delete(path)