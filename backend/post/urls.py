from django.urls import path

from . import views

urlpatterns = [
    path('posts/', views.posts, name='posts'),
    path('crawling/', views.crawling.as_view(), name='crawling'),
    
]