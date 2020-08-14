from django.urls import path
from . import views
from . views import UserProfilesListView, SettingsUpdateView, SettingsDetailView, ProfileView, ProfileDetailView

urlpatterns = [
    path('profile/<slug:username>/', ProfileView.as_view()),
    path('profile_update/<int:user>/', ProfileDetailView.as_view()),
    path('profile/get_profiles/<str:users>', UserProfilesListView.as_view()),

    path('settings_get/', SettingsDetailView.as_view()),
    path('settings_update/<int:user>/', SettingsUpdateView.as_view()),
]