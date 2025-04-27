from django.urls import path
from . import views
from .api import api_create_tweet

urlpatterns = [
    path('api/tweets/', api_create_tweet, name='api_create_tweet'),
    path('tweets/', views.tweets_home, name='tweets_home'),
]
