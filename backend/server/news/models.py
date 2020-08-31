from django.db import models
from django.contrib.auth.models import User
from server import settings
from django.dispatch import receiver
from django.db.models.signals import post_save

import datetime

class Post(models.Model):

    #post's fields
    title = models.CharField(max_length=1000, default='', blank=True)
    video_url = models.TextField(max_length=300, default='', blank=True)
    tags = models.TextField(max_length=500, default='', blank=True)
    date = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0)
    comments_count = models.PositiveSmallIntegerField(default=0)
    type = models.CharField(max_length=50)
    marks = models.TextField(max_length=500, default='|', blank=True)
    language = models.CharField(max_length=100, default='ru')
    username = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # note's fields
    text = models.TextField(max_length=10000, default='', blank=True)
    blog_name = models.CharField(max_length=200, default='')
    note_color = models.CharField(max_length=7, default='white', blank=True)
    text_color = models.CharField(max_length=7, default='#212121', blank=True)

class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    text = models.TextField(max_length=1500, default='')
    image = models.ImageField(blank=True, upload_to='post_images/')
    username = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Document(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField(max_length=1000, default='')
    cover = models.ImageField(blank=True, upload_to='doc_covers/')
    file = models.FileField(upload_to=None)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', blank=True, default='', null=True, on_delete=models.CASCADE, related_name='children')
    text = models.TextField(max_length=1500)
    date = models.DateTimeField(auto_now=True)
    likes = models.TextField(max_length=5000, default='|')
    username = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

@receiver(post_save, sender=Comment)
def update_post(sender, instance, created, **kwargs):
    if created:
        post = Post.objects.filter(id=instance.post.id)
        post.update(comments_count=Comment.objects.filter(post=instance.post.id).count())