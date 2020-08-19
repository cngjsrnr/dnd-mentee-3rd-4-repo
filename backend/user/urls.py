from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

app_name = 'user'

urlpatterns = [
    path('signup/', views.UserList.as_view(), name="signup"),
    path('activate/<str:token>/',
         views.UserActivate.as_view(), name="activate"),
    path('current/', views.current_user),
    path('reset_password/', views.UserPasswordReset.as_view(), name="reset_passowrd"),
    path('reset_password_confirm/<str:token>/',
         views.UserPasswordResetConfirm.as_view(), name="reset_password_confirm"),

]
