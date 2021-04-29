from django.contrib import messages
from django.shortcuts import redirect

from core.aux import generate_slug
from projects.models import Assignation


# Solo es usado una vez, debe irse
def add_assignation(project, new_member_user):
    assignation_slug = generate_slug(Assignation)
    assignation = Assignation(user=new_member_user, project=project,
                              slug=assignation_slug)
    assignation.save()


# Solo es usado una vez, debe irse
def _delete_assignation(request, assignation_slug):
    assignation = Assignation.objects.get(slug=assignation_slug)
    admin_user = assignation.project.admin
    member_user = assignation.user
    if not (request.user == member_user or request.user == admin_user):
        messages.warning("Elemento no asociado")
        return redirect('projects:proyectos')
    if admin_user is not member_user:
        assignation.delete()
    else:
        assignation.project.delete()
