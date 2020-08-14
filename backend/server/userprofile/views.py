from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from django.views.generic import ListView
from rest_framework.response import Response
from . serializers import ProfileSerializer, SettingsSerializer
from . permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

from django.db.models import F
from django.db.models import Q

from . models import Profile, Settings

PostsPerPage = 10

class ProfileView(generics.ListAPIView):
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        username = self.kwargs['username']
        profile = Profile.objects.filter(username=username)
        return profile

class ProfileDetailView(generics.UpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly, )
    lookup_field = 'user'
    queryset = Profile.objects.all()

class UserProfilesListView(generics.ListAPIView):
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        str = self.kwargs['users']
        names = str[1:-1].split("|")
        queryset = Profile.objects.filter(username__in=names)[:PostsPerPage]
        return queryset

class SettingsDetailView(generics.ListAPIView):
    serializer_class = SettingsSerializer
    model = serializer_class.Meta.model
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly, )

    def get_queryset(self):
        user_id = self.request.GET.get("q")
        queryset = Settings.objects.filter(user=user_id)
        return queryset

class SettingsUpdateView(generics.UpdateAPIView):
    serializer_class = SettingsSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly, )
    lookup_field = 'user'
    queryset = Settings.objects.all()

    

