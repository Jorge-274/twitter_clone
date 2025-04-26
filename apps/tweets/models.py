from django.db import models

from apps.users.models import User


# from users.models import User


class Tweet(models.Model):
    user = models.ForeignKey(User, related_name='tweets', on_delete=models.CASCADE)
    content = models.CharField(max_length=280)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_tweets', blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}: {self.content[:20]}..."


class TweetFiles(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    archivos = models.FileField(upload_to='tweets_file/')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
