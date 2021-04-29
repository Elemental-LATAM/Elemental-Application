from django.contrib import messages
from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import generic

from core.aux import generate_slug
from members.models import Member
from notes.models import Petition, Notification
from projects.aux import add_assignation
from projects.models import Project, Assignation


@login_required
def send_invitation_project(request, slug):
    user = get_user(request)
    receiver = Member.objects.get(slug=slug)
    if request.method == "POST":
        subject = request.POST['subject']
        message = request.POST['message']
        project_choice = request.POST['project_choice']
        project = Project.objects.get(slug=project_choice)
        receiver_user = receiver.user
        sender = user
        petition_slug = generate_slug(Petition)
        petition = Petition(sender=sender,
                            receiver=receiver_user, subject=subject,
                            project=project, message=message,
                            slug=petition_slug)
        petition.save()
        messages.success(request, "Se envió tu invitación.")
        return redirect('members:miembro', slug=slug)
    else:
        projects = []
        assignations = Assignation.objects.filter(user=user)
        member_assignations = Assignation.objects.filter(user=receiver.user)
        for assignation in assignations:
            if assignation.project.admin == user:
                projects.append(assignation.project)

        for assignation in member_assignations:
            try:
                projects.remove(assignation.project)
            except:
                print("good to go")

        context = {
            'receiver': receiver,
            'projects': projects,
        }
        return render(request, "notes/send_invitation_project.html", context)


class PetitionListView(LoginRequiredMixin, generic.View):
    def get(self, request, *args, **kwargs):
        user = get_user(request)
        petitions_received = Petition.objects.filter(receiver=user)
        join_requests = []
        invitations = []
        for petition_received in petitions_received:
            if user != petition_received.project.admin:
                join_requests.append(petition_received)
            else:
                invitations.append(petition_received)

        petitions_sent = Petition.objects.filter(sender=user)
        notifications = Notification.objects.filter(receiver=user)
        context = {
            'notifications': notifications,
            'join_requests': join_requests,
            'invitations': invitations,
            'petitions_sent': petitions_sent,
        }
        return render(request, 'notes/peticiones.html', context)


@login_required
def authorize_petition(request, slug):
    petition = Petition.objects.get(slug=slug)
    user = get_user(request)
    if user == petition.receiver:
        if user == petition.project.admin:
            new_member = petition.sender
            new_project = petition.project
            add_assignation(new_project, new_member)
            messages.warning(request, "Se añadió a un usuario al proyecto")
            petition.delete()
            notification_slug = generate_slug(Notification)
            notification_receiver = new_member
            notification_subject = "El usuario " + str(user) + " aceptó tu solicitud"
            notification_message = "Ahora eres parte del proyecto " + str(new_project)
            notification = Notification(
                slug=notification_slug,
                receiver=notification_receiver,
                subject=notification_subject,
                message=notification_message,
            )
            notification.save()
        else:
            new_member = petition.receiver
            new_project = petition.project
            add_assignation(new_project, new_member)
            messages.warning(request, "Te uniste al proyecto")
            petition.delete()
            notification_slug = generate_slug(Notification)
            notification_receiver = new_project.admin
            notification_subject = "El usuario " + str(user) + " aceptó tu solicitud"
            notification_message = "Ahora " + str(user) + " es parte de " + str(new_project)
            notification = Notification(
                slug=notification_slug,
                receiver=notification_receiver,
                subject=notification_subject,
                message=notification_message, )
            notification.save()
    else:
        messages.warning("No puedes alterar una petición que no te pertenece")
    return redirect('notes:peticiones')


@login_required
def deny_petition(request, slug):
    petition = Petition.objects.get(slug=slug)
    if not (request.user == petition.receiver or request.user == petition.sender):
        messages.warning("Elemento no vinculado al usuario.")
        return redirect('notes:peticiones')
    notification_slug = generate_slug(Notification)
    notification_receiver = petition.sender
    notification_subject = "El usuario " + str(petition.receiver) + " denegó tu solicitud"
    notification_message = str(petition.receiver) + " no aceptó tu solicitud para el proyecto " + str(petition.project)
    notification = Notification(
        slug=notification_slug,
        receiver=notification_receiver,
        subject=notification_subject,
        message=notification_message, )
    notification.save()
    petition.delete()
    return redirect('notes:peticiones')


@login_required
def cancel_petition(request, slug):
    petition = Petition.objects.get(slug=slug)
    if petition.sender != request.user:
        messages.warning('No puedes alterar una petición ajena.')
        return redirect('notes:peticiones')
    project = petition.project
    petition.delete()
    return redirect('projects:proyecto', slug=project.slug)


@login_required
def delete_notification(request, slug, notification=None):
    if request.user != notification.receiver:
        messages.warning('No puedes alterar una notificación ajena.')
        return redirect('peticiones')
    notification = Notification.objects.get(slug=slug)
    notification.delete()
    return redirect('notes:peticiones')
