from django.shortcuts import render

from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets

from .models import Post
from .serializers import *

class PostAPIView(APIView): #APIView는 껍데기 부분(최상위)
    def post(self, request): #get, patch 다 가능, 프론트에 넘어오는 데이터가 request
        serializer = PostBaseSerializer(data = request.data) #번역기로 돌린 후(json을 query로)
        if serializer.is_valid(): #save하기 위해서는 반드시 필요!!!!!
            if serializer.validated_data['bad_post'] == True:
                return Response({"message": "bad post" }, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer.save()
                return Response({"message": "post success"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetAPIView(APIView):
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

class PostCommentAPIView(APIView):
    def post(self, request): #get, patch 다 가능, 프론트에 넘어오는 데이터가 request
        serializer = PostCommentSerializer(data = request.data) #번역기로 돌린 후(json을 query로)
        if serializer.is_valid(): #save하기 위해서는 반드시 필요!!!!!
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


'''
# PostAPIView2 추가
class PostAPIView2(APIView):
    def post(self, request): #FBV는 if request.method =="POST"로
        serializer = PostSerializer(data = request.data)
        print(serializer.initial_data)
        if serializer.is_valid():
            print(serializer.validated_data)
            if serializer.initial_data['bad_post'] == True:
                return Response({"message": "bad post" }, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer.save()
                print(serializer.data)
                return Response({"message": "post success"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# FBV
# posts > views.py
# PostAPI_FBV 추가
@api_view(['POST']) #데코레이터로 메소드 판별
def PostAPI_FBV(request):
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        if serializer.initial_data['bad_post'] == True:
            return Response({"message": "bad post" }, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer.save()
            return Response({"message": "post success"}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Mixins
# posts > views.py
class PostListCreateMixin(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Post.objects.all() #filter 활용 가능
    serializer_class = PostSerializer #번역기 정의

    def get(self, request): #메소드 매핑
        return self.list(request) #get 요청 들어왔을 때 ListModelMixin의 list함수 불러옴
    
    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.initial_data['bad_post'] == True:
            return Response({"message": "bad post" }, status=status.HTTP_400_BAD_REQUEST)
        return self.create(request)

# GenericView
# posts > views.py
class PostListCreateGeneric(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def post(self, request): #오버라이딩 -> ListCreateAPIView에는 post 메소드 존재하므로
        serializer = PostSerializer(data=request.data)
        if serializer.initial_data['bad_post'] == True:
            return Response({"message": "bad post" }, status=status.HTTP_400_BAD_REQUEST)
        return self.create(request)

# ModelViewSet
# posts > views.py
class PostModelViewSet(viewsets.ModelViewSet): #ModelViewSet -> 다섯개 다 상속 받음
    queryset = Post.objects.all()
    serializer_class = PostSerializer

'''
    
