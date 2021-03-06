"""djangoreactapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token
from .views import validate_jwt_token


urlpatterns = [
    path('admin/', admin.site.urls),

    #토큰 발행
    path('user/login/', obtain_jwt_token),
    
    #토큰이 유효한지 검증
    path('user/validate/', validate_jwt_token),
    #path('verify/', verify_jwt_token),

    #토큰 갱신
    path('user/refresh/', refresh_jwt_token),
    

    path('user/', include('user.urls'),),
    path('api/', include('post.urls')),

]
