from django.urls import path
from . import views
from .views import login_view, ProfileView, follow_user, unfollow_user
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register, name='register'),
    path('users/', views.users_home, name='users_home'),
    path('<str:username>/', ProfileView.as_view(), name='profile'),
    path('<str:username>/follow/', follow_user, name='follow_user'),
    path('<str:username>/unfollow/', unfollow_user, name='unfollow_user'),
]
