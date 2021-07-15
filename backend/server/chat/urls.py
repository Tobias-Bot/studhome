from django.urls import path
from . views import RoomCreateView, UserRoomsListView

from . import views

urlpatterns = [
    path('create/<slug:username>/', RoomCreateView.as_view()), 
    path('<slug:username>/', UserRoomsListView.as_view()), 
]