from django.shortcuts import render, redirect
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
from django.views.generic import TemplateView

class home(TemplateView) :

    def get(self, request):
        return redirect('/image-search')

class imageSearch(TemplateView) :

    def get(self, request):
        context = {
            'heading' : 'Image Search',
            'subheading' : 'Search Products by Your Image',
            'hellowrod' : 'Hello, World!'
        }
        return render(request, 'index.html', context)

    def post(self, request) :
        try :
            uploaded_image = request.FILES['document']
            fs = FileSystemStorage()
            name = fs.save(uploaded_image.name, uploaded_image)
            path = fs.url(name).split('/')[2]
            return redirect('/image-search/' + path)
        except :
            return redirect('/image-search')

class imageSearchResult(TemplateView) :

    def get(self, request, path):
        context = {
            'heading' : 'Image Search',
            'subheading' : 'Search Products by Your Image',
            'hellowrod' : 'Hello, World!'
        }
        images = DummyML.getModel(path)
        context['images'] = images['images']
        context['onsearch'] = '/media/' + path
        return render(request, 'index.html', context)

    def post(self, request, path) :
        try :
            uploaded_image = request.FILES['document']
            fs = FileSystemStorage()
            name = fs.save(uploaded_image.name, uploaded_image)
            path = fs.url(name).split('/')[2]
            return redirect('/image-search/' + path)
        except :
            return redirect('/image-search')

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class imageSearchAPI(APIView) :
    permission_classes = (IsAuthenticated,)

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
