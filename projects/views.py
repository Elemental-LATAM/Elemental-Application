from django.contrib import messages
from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.utils.datastructures import MultiValueDictKeyError
from django.views import generic

from core.aux import generate_slug
from core.models import InterestCategory, Interest
from members.models import Member, MemberInterest
from notes.models import Petition
from projects.aux import _delete_assignation, add_assignation
from projects.forms import ProjectFileForm
from projects.models import Project, Assignation, ProjectInterest, ProjectInterestCategory


@login_required
def join_project(request, slug):
    user = get_user(request)
    project = Project.objects.get(slug=slug)
    context = {
        'project': project,
    }
    if request.method == 'POST':
        subject = request.POST['subject']
        message = request.POST['message']
        receiver = project.admin
        sender = user
        petitions = Petition.objects.all()
        petition_slug = generate_slug(Petition)
        petition = Petition(sender=sender,
                            receiver=receiver, subject=subject,
                            project=project, message=message,
                            slug=petition_slug)
        petition.save()
        messages.success(request, 'Se envió tu solicitud.')
        return redirect('projects:proyecto', slug=slug)
    else:
        return render(request, 'projects/proyecto_unirse.html', context)


@login_required
def delete_assignation(request, slug):
    assignation = Assignation.objects.get(slug=slug)
    assignation_slug = assignation.slug
    project_slug = assignation.project.slug
    messages.warning(request, 'Se quitó a un miembro del proyecto')
    _delete_assignation(request, assignation_slug)
    try:
        return redirect('projects:proyecto', slug=project_slug)
    except:
        return redirect('projects:proyectos')


class ProjectListView(generic.ListView):
    def get(self, request, *args, **kwargs):
        projects = Project.objects.all()
        paginator = Paginator(projects, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        top_categories = InterestCategory.objects.filter(top=True)
        non_top_categories = InterestCategory.objects.filter(top=False)
        context = {
            'non_top_categories': non_top_categories,
            'top_categories': top_categories,
            'page_obj': page_obj,
        }
        return render(request, 'projects/proyectos.html', context)


class ProjectDetailView(generic.View):
    def get(self, request, slug, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request,
                             'Debes iniciar sesión para ver más sobre un proyecto')
            return redirect('core:login')
        user = get_user(request)
        try:
            project = Project.objects.get(slug=slug)
        except:
            return redirect('projects:proyectos')
        assignations = Assignation.objects.filter(project=project)
        author = False
        if user == project.admin:
            author = True
            action_url = project.get_update_project_url
            color = 'warning'
            button = 'Editar'
        else:
            if assignations.filter(user=user).count() is 0:
                received_petitions = Petition.objects.filter(receiver=user).filter(project=project)
                color = 'success'
                print(received_petitions)
                if received_petitions.count() is 0:
                    action_url = project.get_join_project_url
                    button = 'Join'
                else:
                    action_url = received_petitions[0].get_petitions_url
                    button = 'Ver invitación'
                petitions = Petition.objects.filter(
                    sender=user, project=project)
                if petitions.count() is not 0:
                    action_url = petitions[0].get_cancel_petition_url
                    color = 'danger'
                    button = 'Delete request'
            else:
                my_assignation = assignations.filter(user=user)[0]
                action_url = my_assignation.get_delete_assignation_url
                color = 'danger'
                button = 'Quit'

        project_interests = ProjectInterest.objects.filter(project=project)
        admin = Member.objects.filter(user=user)[0]
        context = {
            'object': project,
            'admin': admin,
            'assignations': assignations,
            'author': author,
            'action_url': action_url,
            'color': color,
            'button': button,
            'project_interests': project_interests,
        }
        return render(request, 'projects/proyecto.html', context)


class ProjectNewMembersView(generic.View, LoginRequiredMixin):
    def get(self, request, slug, *args, **kwargs):
        project = Project.objects.get(slug=slug)
        if request.user != project.admin:
            messages.warning('Elemento no está vinculado al usuario.')
            return redirect('projects:proyectos')
        assignations = Assignation.objects.filter(project=project)
        project_interests = ProjectInterest.objects.filter(project=project)
        already_members = []
        for assignation in assignations:
            user = assignation.user
            member = Member.objects.get(user=user)
            already_members.append(member)
        interests = []
        for project_interest in project_interests:
            interests.append(project_interest.interest)
        members = []
        for interest in interests:
            members_interest = MemberInterest.objects.filter(interest=interest)
            for member_interest in members_interest:
                if member_interest.member not in already_members:
                    members.append(member_interest.member)
        paginator = Paginator(members, 18)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'project': project,
            'page_obj': page_obj,
        }
        return render(request, 'projects/proyecto_nuevos_miembros.html', context)


class ProjectInterestView(generic.View):
    def get(self, request, category, interest=None):
        projects = ProjectInterest.objects.filter(category_slug=category)
        current_category = InterestCategory.objects.get(slug=category)
        top_categories = InterestCategory.objects.filter(top=True)
        non_top_categories = InterestCategory.objects.filter(top=False)
        top_interests = Interest.objects.filter(category=current_category).filter(top_category=True)
        non_top_interests = Interest.objects.filter(category=current_category).filter(top_category=False)
        paginator = Paginator(projects, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        if interest is not None:
            projects = projects.filter(interest_slug=interest)
        else:
            projects = ProjectInterestCategory.objects.filter(category=current_category)
        context = {
            'page_obj': page_obj,
            'top_categories': top_categories,
            'non_top_categories': non_top_categories,
            'top_interests': top_interests,
            'non_top_interests': non_top_interests,
        }
        return render(request, 'projects/proyectos_filter.html', context)


# CRUD Projects

def add_project(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Debes iniciar sesión para ver añadir un proyecto')
        return redirect('core:login')
    if request.method == 'POST':
        user = get_user(request)
        title = request.POST['title']
        summary = request.POST['summary']
        description = request.POST['description']
        project_slug = generate_slug(Project)
        project = Project(admin=user,
                          title=title, summary=summary,
                          description=description, slug=project_slug)
        project.save()
        add_assignation(project, user)
        form = ProjectFileForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
        messages.success(request, '¡Se añadió un proyecto!')
        return redirect('projects:project-add-tags', project_slug=project_slug, category='computacion')
    else:
        form = ProjectFileForm()
        context = {
            'form': form,
        }
        return render(request, 'projects/proyecto_crear.html', context)


@login_required
def update_project(request, slug):
    user = get_user(request)
    project = Project.objects.get(slug=slug)
    if user == project.admin:
        print('view')
        if request.method == 'POST':
            print('post')
            project.title = request.POST['title']
            project.summary = request.POST['summary']
            project.description = request.POST['description']
            project.save()
            form = ProjectFileForm(request.POST, request.FILES, instance=project)
            if form.is_valid():
                form.save()
                messages.success(request, 'Se actualizó la imagen del proyecto.')
            messages.success(request, 'Se actualizó la información del proyecto.')
            return redirect('projects:update-project', slug=project.slug)
        else:
            print('get')
            form = ProjectFileForm()
            context = {
                'project': project,
                'form': form,
            }
            return render(request, 'projects/proyecto_editar.html', context)
    else:
        messages.success(request, 'No puedes editar un proyecto si no eres el administrador.')
        return redirect('projects:proyectos')


@login_required
def delete_project(request, slug):
    user = get_user(request)
    project = Project.objects.filter(slug=slug)
    if user == project[0].admin:
        project.delete()
        messages.warning(request, 'Se eliminó un proyecto.')
    else:
        messages.warning(request, 'No puedes borrar un proyecto que no es tuyo.')
    return redirect('projects:proyectos')


class ProjectAddTagView(LoginRequiredMixin, generic.View):
    def get(self, request, project_slug, category='computacion'):
        user = get_user(request)
        project = Project.objects.get(slug=project_slug)
        if user == project.admin:
            old_tags = ProjectInterest.objects.filter(category_slug=category).filter(project=project)
            categories = InterestCategory.objects.all()
            tag_category = InterestCategory.objects.get(slug=category)
            tags = Interest.objects.filter(category=tag_category)
            new_tags = []
            if old_tags.count() is 0:
                new_tags = tags
            else:
                for tag in tags:
                    for old_tag in old_tags:
                        if old_tag.interest != tag:
                            if tag not in new_tags:
                                new_tags.append(tag)
            context = {
                'categories': categories,
                'tags': new_tags,
                'project': project,
            }
            return render(request, 'projects/project_add_tags.html', context)
        else:
            messages.warning('No puedes alterar un proyecto del cual no eres administrador.')
        return redirect('projects:proyectos')


@login_required
def project_add_interest(request, project_slug, tag):
    user = get_user(request)
    project = Project.objects.get(slug=project_slug)
    if user == project.admin:
        print('is admin')
        interest = Interest.objects.get(slug=tag)
        slug = generate_slug(ProjectInterest)
        is_already = ProjectInterest.objects.filter(project=project).filter(interest=interest)
        category_slug = InterestCategory.objects.filter(interest=interest)[0].slug
        current_category = InterestCategory.objects.get(slug=category_slug)
        if is_already.count() is 0:
            print('is new')
            interest_slug = tag
            new_interest = ProjectInterest(slug=slug, interest=interest, project=project,
                                           category_slug=category_slug, interest_slug=interest_slug)
            new_interest.save()
            print('added')
            is_already = ProjectInterestCategory.objects.filter(category=current_category).filter(project=project)
            if is_already.count() is 0:
                print('adding category')
                new_slug = generate_slug(ProjectInterestCategory)
                new_category = ProjectInterestCategory(slug=new_slug, category=current_category, project=project)
                new_category.save()
        return redirect('projects:project-add-tags', project_slug=project_slug, category=category_slug)
    else:
        messages.warning('No puedes alterar un proyecto del cual no eres administrador.')
        return redirect('notes:peticiones')
    return redirect('projects:proyectos')


class ProjectDeleteTagView(LoginRequiredMixin, generic.View):
    def get(self, request, slug):
        user = get_user(request)
        project = Project.objects.get(slug=slug)
        if user != project.admin:
            messages.warning('No puedes alterar un proyecto ajeno')
            return redirect('projects:proyectos')
        interests = ProjectInterest.objects.filter(project=project)
        context = {
            'interests': interests,
            'project': project,
        }
        return render(request, 'projects/project_delete_tags.html', context)


@login_required
def project_delete_interest(request, project_slug, tag):
    project = Project.objects.get(slug=project_slug)
    if request.user != project.admin:
        messages.warning('No puedes alterar un proyecto ajeno')
        return redirect('projects:proyectos')
    my_tag = ProjectInterest.objects.get(slug=tag)
    my_category = my_tag.interest.category
    category_slug = my_category.slug
    my_tag.delete()
    still_category = ProjectInterest.objects.filter(project=project).filter(category_slug=category_slug)
    if still_category.count() is 0:
        old_category = ProjectInterestCategory.objects.filter(project=project).filter(category=my_category)
        old_category.delete()
    return redirect('projects:project-delete-tags', slug=project_slug)


class ProjectAdvancedFilterView(generic.View):
    _interest_categories = InterestCategory.objects.all()
    interest_categories = []

    for interest_category in _interest_categories:
        x = []
        x.append(False)
        x.append(interest_category)
        interest_categories.append(x)

    def get(self, request):
        selected_interest_categories = []
        for i in range(0, len(self.interest_categories)):
            try:
                interest = self.interest_categories[i][1]
                if request.GET[interest.slug]:
                    self.interest_categories[i][0] = True
                    selected_interest_categories.append(interest)
            except MultiValueDictKeyError:
                self.interest_categories[i][0] = False
                print('none')

        interests_groups = []
        for selected_interest_category in selected_interest_categories:
            interests_groups.append(Interest.objects.filter(category=selected_interest_category))

        selected_interests = []
        for interest_group in interests_groups:
            for interest in interest_group:
                try:
                    if request.GET[interest.slug]:
                        selected_interests.append(interest)
                except MultiValueDictKeyError:
                    print('none')

        projects_groups = []
        for selected_interest in selected_interests:
            projects_groups.append(ProjectInterest.objects.filter(interest=selected_interest))

        projects = []
        for project_group in projects_groups:
            for projectTag in project_group:
                if projectTag.project not in projects:
                    projects.append(projectTag.project)
        paginator = Paginator(projects, 18)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'interest_categories': self.interest_categories,
            'interests_groups': interests_groups,
            'page_obj': page_obj,
        }
        return render(request, 'projects/proyecto_filtro_avanzado.html', context)
