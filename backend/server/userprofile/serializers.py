from rest_framework import serializers
from django.contrib.auth.models import User

from . models import Settings, Profile

class ProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = Profile
    fields = '__all__'

class SettingsSerializer(serializers.ModelSerializer):
  class Meta:
    model = Settings
    fields = '__all__'