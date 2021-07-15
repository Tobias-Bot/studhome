from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics
from django.views.generic import ListView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from . serializers import RoomSerializer

from . models import Room
from userprofile.models import Profile

class RoomCreateView(generics.CreateAPIView):
    serializer_class = RoomSerializer
    permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        username = self.kwargs['username']
        profile = Profile.objects.get(username=username)
        room = self.create(request, *args, **kwargs)
        profile.rooms_count = Room.objects.filter(adminname=username).count()
        profile.save()
        return Response(status=201)

class UserRoomsListView(generics.ListAPIView):
    serializer_class = RoomSerializer
    model = serializer_class.Meta.model

    def get_queryset(self):
        username = self.kwargs['username']
        queryset = Room.objects.filter(adminname=username).order_by('-creation_date')
        return queryset