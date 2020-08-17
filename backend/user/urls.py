from django.urls import path
from .views import current_user, UserList, UserActivate

urlpatterns = [
    path('signup/', UserList.as_view(),name="signup"),
    path('activate/<str:uid64>/<str:token>/', UserActivate.as_view(),name="activate"),
    path('current/', current_user),
]
