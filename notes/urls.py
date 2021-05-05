from django.urls import path

from notes.views import *

app_name = 'notes'
urlpatterns = [
    path("peticiones/", PetitionListView.as_view(), name="peticiones"),
    path("authorize-petition/<slug>/", authorize_petition, name='authorize-petition'),
    path("deny-petition/<slug>/", deny_petition, name='deny-petition'),
    path("cancel-petition/<slug>/", cancel_petition, name='cancel-petition'),
    path("delete-notification/<slug>/", delete_notification, name="delete-notification"),
    path("miembro/<slug>/send-invitation/", send_invitation_project, name='send-invitation-project'),
]
