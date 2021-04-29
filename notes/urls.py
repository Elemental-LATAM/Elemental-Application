from django.urls import path

from notes.views import PetitionListView

app_name = 'notes'
urlpatterns = [
    path('peticiones/', PetitionListView.as_view(), name='peticiones'),
]
