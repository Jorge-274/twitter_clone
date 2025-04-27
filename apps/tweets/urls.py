from django.urls import path
from . import views
from .api import api_create_tweet, TweetListView

urlpatterns = [
    path('api/tweets/', api_create_tweet, name='api_create_tweet'),
    path('api/tweets/list/', TweetListView.as_view(), name='tweet-list'),
    path('tweets/', views.tweets_home, name='tweets_home'),
]
