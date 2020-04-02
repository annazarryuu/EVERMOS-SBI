from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from evermos import DummyML
from rest_framework import status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import permissions

#Authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

#User for authentication
from django.contrib.auth.models import User
from evermos.serializers import UserSerializer
from rest_framework import generics
from rest_framework.views import APIView

def index(request) :
    context = {
        'heading' : 'Image Search',
        'subheading' : 'Search Products by Your Image',
        'hellowrod' : 'Hello, World!'
    }

    if(request.method == 'POST') :
        try :
            uploaded_image = request.FILES['document']
            fs = FileSystemStorage()
            name = fs.save(uploaded_image.name, uploaded_image)
            url = fs.url(name)
            images = DummyML.getModel(url)
            context['images'] = images['images']
            context['onsearch'] = url
        except MultiValueDictKeyError :
            pass

    return render(request, 'index.html', context)

def imageSearchs(request) :

    return JsonResponse(DummyML.getModel(None), status=status.HTTP_200_OK)

    # response = Response(DummyML.getModel(None), status=status.HTTP_200_OK)
    # response.accepted_renderer = JSONRenderer()
    # response.accepted_media_type = "application/json"
    # response.renderer_context = {}
    # return response

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class imageSearch(APIView) :
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        return JsonResponse(DummyML.getModel(None), status=status.HTTP_200_OK)
    def post(self, request):
        try :
            uploaded_image = request.FILES['document']
            file_extention = uploaded_image.name.split('.')
            file_extention = file_extention[len(file_extention) - 1]
            if(not(file_extention in ['jpg', 'png', 'jpeg'])) :
                return JsonResponse({'status':'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)
            fs = FileSystemStorage()
            name = fs.save(uploaded_image.name, uploaded_image)
            url = fs.url(name)
            images = DummyML.getModel(url)
            return JsonResponse(images, status=status.HTTP_200_OK)
        except MultiValueDictKeyError :
            return JsonResponse({'status' : 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)
