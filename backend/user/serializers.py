import jwt
from djangoreactapi.settings import get_secret
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
#from django.contrib.auth.models import User
from .models import User
from django.core.exceptions import ValidationError

# SMTP 관련 인증
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes
from .tokens import account_activation_token


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email')


class UserSerializerWithToken(serializers.ModelSerializer):

    token = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    def get_token(self, value):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(value)
        token = jwt_encode_handler(payload)
        return token

    def validate_email(self, value):
        if(User.objects.filter(email=value).exists()):
            raise serializers.ValidationError("이미 존재하는 이메일 입니다")
        print("suc1")
        return value

    def validate_username(self, value):
        if(len(value) < 2 or len(value) > 15):
            raise serializers.ValidationError("닉네임은 2글자이상 15글자 이하로 작성해주세요")
        if(User.objects.filter(first_name=value).exists()):
            raise serializers.ValidationError("이미 존재하는 닉네임입니다")
        print("suc2")
        return value

    def validate_password(self, value):
        if(len(value) < 8):
            raise serializers.ValidationError("비밀번호를 8이상으로 입력해주세요")
        print("suc3")
        return value


    # 회원가입이니까 해당 값이 없으니 serializer.save()할때 create()를 통해 저장이 이루어짐 그래서 create만들어줌
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)

        instance.is_active = False
        instance.save()
        print(instance.__dict__)
        # current_site=get_current_site(self.context['request'])
        message = render_to_string('user/email_confirm.html', {
            'user': instance.username, 'domain': "localhost:8000",
            'uid':  jwt.encode({'pk': instance.pk},get_secret("SECRET_KEY"),algorithm='HS256').decode('utf-8'),
            'token': account_activation_token.make_token(instance),
        })

        mail_subject = '계정을 활성화 해주세요'
        to_email = validated_data['email']
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()

        return instance

    class Meta:
        model = User
        fields = ('token', 'username', 'first_name', 'email', 'password')
