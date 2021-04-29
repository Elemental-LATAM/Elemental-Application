from django.urls import path

from core.views import *

app_name = 'core'
urlpatterns = [
    path('', about, name='about'),
]
