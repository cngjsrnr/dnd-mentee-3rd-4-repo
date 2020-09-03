from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from .models import Post
#from .serializers import PostSerializer
from .news_crawl import Crawl

@api_view(['GET'])
@permission_classes((AllowAny, ))
def posts(request):
    posts = Post.objects.all()
    post_list = serializers.serialize('json', posts)
    return HttpResponse(post_list, content_type="text/json-comment-filtered")
    
#크롤링
class crawling(APIView):

    def get(self, request):
        Crawl()
        return Response({'message': "크롤링 완료"}, status=status.HTTP_200_OK)

