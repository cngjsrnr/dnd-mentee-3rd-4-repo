from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager

class UserManager(BaseUserManager):
    def _create_user(self,email,password=None, **kwargs):
        if(not email):
            raise ValueError("이메일을 입력해주세요")
        
        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save(using=self._db)

    def create_user(self, email, password, **kwargs):
        """
        일반 유저 생성
        """
        kwargs.setdefault('is_admin', False)
        return self._create_user(email, password, **kwargs)

    def create_superuser(self, email, password, **kwargs):
        """
        관리자 유저 생성
        """
        kwargs.setdefault('is_admin', True)
        return self._create_user(email, password, **kwargs)
    

class User(AbstractUser):
    email = models.EmailField(max_length=128,verbose_name='이메일', unique=True)
    username=models.CharField(max_length=32,verbose_name='닉네임',unique=True)

    objects=UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS= []

    def __str__(self):
        return self.email