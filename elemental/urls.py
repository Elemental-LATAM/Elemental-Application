from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from elemental import settings

urlpatterns = [
    path('', include('core.urls', namespace='core')),
    path('members/', include('members.urls', namespace='members')),
    path('projects/', include('projects.urls', namespace='projects')),
    path('notes/', include('notes.urls', namespace='notes')),
    path('el3m3nt4l/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + \
              static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
