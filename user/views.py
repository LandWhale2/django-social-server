from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserSerializer,RelationSerializer
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import User, Relation
from rest_framework import viewsets



class SignUp(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('updated_ay')
    serializer_class = UserSerializer



class RelationViewSet(viewsets.ModelViewSet):
    queryset = Relation.objects.all()
    serializer_class = RelationSerializer




# from django.views.decorators.http import require_POST
# from django.http import HttpResponse
# try:
#     from django.utils import simplejson as json
# except ImportError:
#     import json
# from user import models
# from django.views.decorators.csrf import csrf_exempt



# @require_POST
# @csrf_exempt
# def Relations(request):
#     if request.method == 'POST':
#         ds = json.loads(request.body)
#         from_user = ds['from_user']
#         to_user = ds['to_user']
#         relation_type = ds['type']

#         if relation_type == 'f':
#             print('rrrrrr')
#             R = Relation(from_user=from_user, to_user=to_user, type='f')
#             R.save()
#             message = '팔로우'
#         elif relation_type == 'b':
#             R = Relation(from_user=from_user, to_user=to_user, type='b')
#             R.save()
#             message = '차단'
#         else:
#             message = '알 수 없는 입력'
        
#         print('aaaaaa')
        

#     context = {'like_count' : 'dd', 'message': message}
#     response = HttpResponse(json.dumps(context), content_type='application/json')
#     return response


# class UserPhotoViewSet(viewsets.ModelViewSet):
#     queryset = UserPhoto.objects.all().order_by('date_added')
#     serializer_class = UserPhotoSerializer



# def delete(self, *args, **kwargs):
#     # You have to prepare what you need before delete the model
#     storage, path = self.image.storage, self.image.path
#     # Delete the model before the file
#     super(Profile, self).delete(*args, **kwargs)
#     # Delete the file after the model
#     storage.delete(path)