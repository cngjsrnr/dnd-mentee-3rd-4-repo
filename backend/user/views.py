import jwt
from djangoreactapi.settings import get_secret
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
#from django.contrib.auth.models import User
from .models import User
from rest_framework import permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer, UserSerializerWithToken
from .tokens import account_activation_token
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.contrib import auth

# 현재 유저 정보 반환


@api_view(['GET'])
def current_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


# 회원가입
class UserList(APIView):

    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        ret_val = request.data['password'] != request.data['password2']
        request.data.pop("password2", None)
        serializer = UserSerializerWithToken(data=request.data)
        print("1")
        # 비밀번호 1, 2가 다를경우
        if(ret_val):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        print("2")

        if serializer.is_valid():
            print("3")
            serializer.save()
            print("4")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# 계정 활성화 함수(토큰을 통해 인증)
class UserActivate(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, uid64, token):
        try:

            uid=jwt.decode(uid64,get_secret("SECRET_KEY"),algorithm='HS256')
            user = User.objects.get(pk=uid['pk'])

        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if (user is not None and account_activation_token.check_token(user, token)):
            user.is_active = True
            user.save()
            auth.login(request, user)
            return redirect("/")
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
