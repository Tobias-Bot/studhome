from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from . import settings

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('silk/', include('silk.urls', namespace='silk')),

    path('api/v1/news/', include('news.urls')),
    path('api/v1/home/', include('userprofile.urls')),

    path('api/v1/auth/', include('djoser.urls')),
    path('api/v1/auth_token/', include('djoser.urls.authtoken')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
