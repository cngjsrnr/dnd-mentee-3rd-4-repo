import jwt
from django.shortcuts import render
from djangoreactapi.settings import get_secret
from .models import User
from rest_framework import permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib import auth
from .models import User
from pytz import timezone
from datetime import datetime, timedelta

# SMTP
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from .tokens import account_activation_token

from .serializers import UserSerializer, UserSerializerWithToken

# from rest_auth.views import PasswordResetView

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

        # 비밀번호 1, 2가 다를경우
        if serializer.is_valid():
            if(ret_val):
                return Response({'message': '비밀번호가 일치하지 않습니다'}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        error_message = {}
        if 'email' in serializer.errors:
            error_message['message'] = serializer.errors['email'][0]
        elif 'username' in serializer.errors:
            error_message['message'] = serializer.errors['username'][0]
        elif 'password' in serializer.errors:
            error_message['message'] = serializer.errors['password'][0]

        return Response(error_message, status=status.HTTP_400_BAD_REQUEST)


# 계정 활성화 함수(토큰을 통해 인증)
class UserActivate(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, token):
        try:
            uid = jwt.decode(token, get_secret(
                "SECRET_KEY"), algorithm='HS256')

            if User.objects.filter(pk=uid['pk']).exists():
                user = User.objects.get(pk=uid['pk'])
                user.is_active = True
                user.save()
                auth.login(request, user)
                return render(request, 'user/signup_success.html')
            else:
                return render(request, 'user/dont_exist_user.html')
        except jwt.ExpiredSignatureError:
            return render(request, 'user/invalide_link.html')

# 비밀번호 초기화
class UserPasswordReset(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        email = request.data['email']
        if User.objects.filter(email=email).exists():
            instance = User.objects.filter(email=email).get()
            token = jwt.encode({
                'pk': instance.pk,
                'exp': datetime.now(timezone('Asia/Seoul')) + timedelta(minutes=10)
            }, get_secret("SECRET_KEY"), algorithm='HS256').decode('utf-8')

            message = render_to_string('user/password_reset_email.html', {
                'user': instance.username, 'domain': "localhost:8000",
                'token': token,
            })
            mail_subject = '비밀번호 초기화'
            to_email = email
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()

        else:
            return Response({'message': '존재하지않는 이메일입니다'}, status=status.HTTP_400_BAD_REQUEST)


class UserPasswordResetConfirm(APIView):

    def get(self, request, token):
        try:
            uid = jwt.decode(token, get_secret(
                "SECRET_KEY"), algorithm='HS256')

            form = {
                'domain': "localhost:8000",
                'token': token,
            }

            return render(request, 'user/password_reset.html', form)

        except jwt.ExpiredSignatureError:
            return render(request, 'user/invalide_link.html')

    def post(self, request, token):
        try:
            password1 = request.data['password1']
            password2 = request.data['password2']
            
            uid = jwt.decode(token, get_secret(
                "SECRET_KEY"), algorithm='HS256')

            if User.objects.filter(pk=uid['pk']).exists():
                if password1 != password2:
                    return render(request, 'user/not_same_password.html')
                if len(password1) < 8:
                    return render(request, 'user/password_length_error.html')
                instance = User.objects.filter(pk=uid['pk']).get()
                instance.set_password(password1)
                instance.save()
                return render(request, 'user/password_reset_success.html')
            else:
                return render(request, 'user/dont_exist_user.html')

        except jwt.ExpiredSignatureError:
            return render(request, 'user/invalide_link.html')
