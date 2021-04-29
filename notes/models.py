from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from projects.models import Project


class Petition(models.Model):
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userReceiver')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userSender')
    slug = models.IntegerField(unique=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    subject = models.CharField(max_length=140)
    message = models.TextField()
    sent_date = models.DateTimeField("date created", auto_now_add=True)

    class Meta:
        ordering = ['-slug']

    def __str__(self):
        return self.sender.username + '->' + self.receiver.username

    def get_petitions_url(self):
        return reverse("notes:peticiones")

    def get_deny_petition_url(self):
        return reverse("notes:deny-petition", kwargs={
            'slug': self.slug
        })

    def get_cancel_petition_url(self):
        return reverse("notes:cancel-petition", kwargs={
            'slug': self.slug
        })

    def get_authorize_petition_url(self):
        return reverse("notes:authorize-petition", kwargs={
            'slug': self.slug
        })


class Notification(models.Model):
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notificationReceiver')
    slug = models.IntegerField(unique=True)
    subject = models.CharField(max_length=140)
    message = models.TextField()
    sent_date = models.DateTimeField("date created", auto_now_add=True)

    class Meta:
        ordering = ['-slug']

    def __str__(self):
        return 'Notificación para ' + str(self.receiver)

    def get_delete_notification_url(self):
        return reverse("notes:delete-notification", kwargs={
            'slug': self.slug
        })


# Add member stuff to user
def has_notifications(self):
    petitions = Petition.objects.filter(receiver=self)
    notifications = Notification.objects.filter(receiver=self)
    counter = petitions.count() + notifications.count()
    if counter == 0:
        return False
    else:
        return True


User.add_to_class('has_notifications', has_notifications)
