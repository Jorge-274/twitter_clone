from django.urls import path
from . import views

urlpatterns = [
    path('tweets/', views.tweets_home, name='tweets_home'),
]
