from django.db import models
from django.contrib.auth.models import User
from server import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

import datetime

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.TextField(max_length=500)
    bio = models.TextField(max_length=3000, blank=True, default="Описание профиля")
    status = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(blank=True, upload_to='profile_avatars/', default="http://127.0.0.1:8000/media/profile_avatars/default_avatar.png")
    contacts = models.TextField(max_length=1500, blank=True)
    interests = models.TextField(max_length=2000, default="")
    school = models.TextField(max_length=1000, default="")
    subs_profiles = models.TextField(max_length=10000, default="|")
    bookmarks = models.TextField(max_length=5000, default="|")
    readers = models.PositiveIntegerField(default=0)
    posts_count = models.PositiveIntegerField(default=0)

class Settings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    blackout = models.CharField(max_length=4, default='0')
    blur = models.CharField(max_length=3, default='0')
    background = models.ImageField(blank=True, null=True, upload_to='setting_covers/', default="")
    unsplash_background = models.TextField(max_length=300, default="", blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, username=instance.username)
        Settings.objects.create(user=instance)
