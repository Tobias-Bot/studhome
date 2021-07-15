from django.db import models

from django.contrib.auth.models import User

class Room(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=3000, default='')
    subs = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    creation_date = models.DateTimeField(auto_now=True)
    image = models.ImageField(blank=True, upload_to='room_covers/')
    adminname = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
