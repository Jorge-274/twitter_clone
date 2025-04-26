from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('users/', views.users_home, name='users_home'),
    path('<str:username>/', ProfileView.as_view(), name='profile'),
    path('<str:username>/follow/', follow_user, name='follow_user'),
    path('<str:username>/unfollow/', unfollow_user, name='unfollow_user'),
]
