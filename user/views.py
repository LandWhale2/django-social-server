from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import User
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