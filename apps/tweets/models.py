from django.db.models import TextField

from apps.users.models import User
from django.db import models
from django_quill.fields import QuillField


class Tweet(models.Model):
    user = models.ForeignKey(User, related_name='tweets', on_delete=models.CASCADE)
    content = TextField(max_length=280)  # Editor de texto enriquecido con formato, imágenes, etc.
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_tweets', blank=True)
    retweets = models.ManyToManyField(User, related_name='retweeted_tweets', blank=True)
    parent_tweet = models.ForeignKey('self', null=True, blank=True,
                                     on_delete=models.CASCADE, related_name='replies')
    is_retweet = models.BooleanField(default=False)
    original_tweet = models.ForeignKey('self', null=True, blank=True,
                                       on_delete=models.CASCADE, related_name='retweeted_by')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}: {self.content.html[:20]}..." if self.content else f"{self.user.username}: [Empty tweet]"

    def like_count(self):
        return self.likes.count()

    def retweet_count(self):
        return self.retweets.count()

    def reply_count(self):
        return self.replies.count()


class TweetFiles(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name='media_files')
    file = models.FileField(upload_to='tweets/media/')
    file_type = models.CharField(max_length=10, blank=True)  # 'image', 'video', 'gif', etc.
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Tweet media'

    def __str__(self):
        return f"Media for tweet #{self.tweet.id}"
