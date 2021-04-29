from django.contrib import messages
from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils.datastructures import MultiValueDictKeyError
from django.views import generic
from rest_framework.decorators import api_view

from core.models import SkillCategory, Skill, InterestCategory, Interest
from core.serializers import SkillsSerializer, InterestSerializer
from projects.models import Assignation
from .aux import add_skill_generic, add_interest_generic
from .forms import MemberFileForm
from .models import Member, MemberInterest, MemberSkill, MemberSkillCategory, MemberInterestCategory


class MemberListView(generic.ListView):
    model = Member
    paginate_by = 9
    template_name = 'members/miembros.html'


class MemberInterestView(generic.View):
    def get(self, request, category='computacion', interest=None):
        top_categories = InterestCategory.objects.filter(top=True)
        non_top_categories = InterestCategory.objects.filter(top=False)
        current_category = InterestCategory.objects.get(slug=category)
        top_interests = Interest.objects.filter(category=current_category).filter(top_category=True)
        non_top_interests = Interest.objects.filter(category=current_category).filter(top_category=False)
        if interest is not None:
            members = MemberInterest.objects.filter(category_slug=category).filter(interest_slug=interest)
        else:
            members = MemberInterestCategory.objects.filter(category=current_category)
        filter_used = 'intereses'
        filter_interest = True
        paginator = Paginator(members, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'page_obj': page_obj,
            'top_categories': top_categories,
            'top_interests': top_interests,
            'non_top_categories': non_top_categories,
            'non_top_interests': non_top_interests,
            'filter_used': filter_used,
            'filter_interest': filter_interest,
        }
        return render(request, 'members/miembros_filter.html', context)


class MemberSkillView(generic.View):
    def get(self, request, category='programacion', skill=None):
        top_categories = SkillCategory.objects.filter(top=True)
        non_top_categories = SkillCategory.objects.filter(top=False)
        current_category = SkillCategory.objects.get(slug=category)
        top_skills = Skill.objects.filter(category=current_category).filter(top_category=True)
        non_top_skills = Skill.objects.filter(category=current_category).filter(top_category=False)
        if skill is not None:
            members = MemberSkill.objects.filter(category_slug=category).filter(skill_slug=skill)
        else:
            members = MemberSkillCategory.objects.filter(category=current_category)
        filter_used = 'skills'
        filter_interest = False
        paginator = Paginator(members, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'page_obj': page_obj,
            'top_categories': top_categories,
            'top_interests': top_skills,
            'non_top_categories': non_top_categories,
            'non_top_interests': non_top_skills,
            'filter_used': filter_used,
            'filter_interest': filter_interest,
        }
        return render(request, 'members/miembros_filter.html', context)


class MemberAdvancedFilterView(generic.View):
    _interest_categories = InterestCategory.objects.all()
    _skill_categories = SkillCategory.objects.all()
    interest_categories = []
    skill_categories = []

    for interest_category in _interest_categories:
        x = []
        x.append(False)
        x.append(interest_category)
        interest_categories.append(x)

    for skill_category in _skill_categories:
        x = []
        x.append(False)
        x.append(skill_category)
        skill_categories.append(x)

    def get(self, request):
        selected_interest_categories = []
        selected_skill_categories = []
        for i in range(0, len(self.interest_categories)):
            try:
                interest = self.interest_categories[i][1]
                if request.GET[interest.slug]:
                    self.interest_categories[i][0] = True
                    selected_interest_categories.append(interest)
            except MultiValueDictKeyError:
                self.interest_categories[i][0] = False
                print('none')
        for i in range(0, len(self.skill_categories)):
            try:
                skill = self.skill_categories[i][1]
                if request.GET[skill.slug]:
                    self.skill_categories[i][0] = True
                    selected_skill_categories.append(skill)
            except MultiValueDictKeyError:
                self.skill_categories[i][0] = False
                print('none')

        interests_groups = []
        for selected_interest_category in selected_interest_categories:
            interests_groups.append(Interest.objects.filter(category=selected_interest_category))
        skills_groups = []
        for selected_skill_category in selected_skill_categories:
            skills_groups.append(Skill.objects.filter(category=selected_skill_category))

        selected_interests = []
        for interest_group in interests_groups:
            for interest in interest_group:
                try:
                    if request.GET[interest.slug]:
                        selected_interests.append(interest)
                except MultiValueDictKeyError:
                    print('none')
        selected_skills = []
        for skill_group in skills_groups:
            for skill in skill_group:
                try:
                    if request.GET[skill.slug]:
                        selected_skills.append(skill)
                except MultiValueDictKeyError:
                    print('none')
        members_groups = []
        for selected_interest in selected_interests:
            members_groups.append(MemberInterest.objects.filter(interest=selected_interest))
        for selected_skill in selected_skills:
            members_groups.append(MemberSkill.objects.filter(skill=selected_skill))

        members = []
        for member_group in members_groups:
            for memberTag in member_group:
                if memberTag.member not in members:
                    members.append(memberTag.member)
        paginator = Paginator(members, 18)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'interest_categories': self.interest_categories,
            'skill_categories': self.skill_categories,
            'interests_groups': interests_groups,
            'skills_groups': skills_groups,
            'page_obj': page_obj,
        }
        return render(request, 'members/miembro_filtro_avanzado.html', context)


class MemberDetailView(generic.View):
    def get(self, request, slug, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Debes iniciar sesión para ver más sobre un usuario')
            return redirect('core:login')
        try:
            member = Member.objects.get(slug=slug)
        except:
            return redirect('members:miembros')
        assignations = Assignation.objects.filter(user=member.user)
        user = get_user(request)
        author = False
        if user == member.user:
            author = True
        interests = MemberInterest.objects.filter(member=member)
        skills = MemberSkill.objects.filter(member=member)
        context = {
            'object': member,
            'assignations': assignations,
            'author': author,
            'interests': interests,
            'skills': skills,
        }
        return render(request, 'members/miembro.html', context)


class MemberAddTagView(LoginRequiredMixin, generic.View):
    def get(self, request, designation='intereses', category='computacion'):
        user = get_user(request)
        member = Member.objects.get(user=user)
        new_tags = []
        if designation == 'intereses':
            designation_is_interests = True
            categories = InterestCategory.objects.all()
            tag_category = InterestCategory.objects.get(slug=category)
            tags = Interest.objects.filter(category=tag_category)
            old_tags = MemberInterest.objects.filter(category_slug=category).filter(member=member)
            if old_tags.count() == 0:
                new_tags = tags
            else:
                for tag in tags:
                    for old_tag in old_tags:
                        if old_tag.interest != tag:
                            new_tags.append(tag)
        if designation == 'skills':
            designation_is_interests = False
            categories = SkillCategory.objects.all()
            tag_category = SkillCategory.objects.get(slug=category)
            tags = Skill.objects.filter(category=tag_category)
            old_tags = MemberSkill.objects.filter(category_slug=category).filter(member=member)
            if old_tags.count() == 0:
                new_tags = tags
            else:
                for tag in tags:
                    for old_tag in old_tags:
                        if old_tag.skill != tag:
                            new_tags.append(tag)
        context = {
            'categories': categories,
            'tags': new_tags,
            'current_designation': designation,
            'current_category': category,
            'designation_is_interests': designation_is_interests,
        }
        return render(request, 'members/add_tags_user.html', context)


class MemberDeleteTagView(LoginRequiredMixin, generic.View):
    def get(self, request):
        user = get_user(request)
        member = Member.objects.get(user=user)
        interests = MemberInterest.objects.filter(member=member)
        skills = MemberSkill.objects.filter(member=member)
        context = {
            'interests': interests,
            'skills': skills,
            'member': member,
        }
        return render(request, 'members/delete_tags_user.html', context)


@login_required
def add_skill(request, tag):
    user = get_user(request)
    category_slug = add_skill_generic(tag, user)
    return redirect('members:add-tags', designation='skills', category=category_slug)


@login_required
def delete_skill(request, tag):
    my_tag = MemberSkill.objects.get(slug=tag)
    my_category = my_tag.skill.category
    category_slug = my_category.slug
    my_tag.delete()
    user = get_user(request)
    member = Member.objects.get(user=user)
    still_category = MemberSkill.objects.filter(member=member).filter(category_slug=category_slug)
    messages.warning(request, 'Se eliminó un interés del usuario.')
    if still_category.count() == 0:
        old_category = MemberSkillCategory.objects.filter(member=member).filter(category=my_category)
        old_category.delete()
    return redirect('members:delete-tags')


@login_required
def add_interest(request, tag):
    user = get_user(request)
    category_slug = add_interest_generic(tag, user)
    return redirect('members:add-tags', designation='intereses', category=category_slug)


@login_required
def delete_interest(request, tag):
    my_tag = MemberInterest.objects.get(slug=tag)
    my_category = my_tag.interest.category
    category_slug = my_category.slug
    my_tag.delete()
    user = get_user(request)
    member = Member.objects.get(user=user)
    still_category = MemberInterest.objects.filter(member=member).filter(category_slug=category_slug)
    messages.warning(request, 'Se eliminó un interés del usuario.')
    if still_category.count() == 0:
        old_category = MemberInterestCategory.objects.filter(member=member).filter(category=my_category)
        old_category.delete()
    return redirect('members:delete-tags')


@login_required
def update_user(request):
    if request.method == 'POST':
        user = get_user(request)
        username = request.POST['username']
        member = Member.objects.filter(user=user)
        user.username = username
        user.save()
        member.update(
            name=request.POST['name'],
            summary=request.POST['summary'],
            description=request.POST['description'],
            phone=request.POST['phone'],
            linkedin=request.POST['linkedin'],
        )
        member = member[0]
        form = MemberFileForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            form.save()
            print(form)
            messages.success(request, 'Se actualizó los archivos del usuario.')
        messages.success(request, 'Se actualizó la información del usuario.')
        return redirect('members:update-user')
    else:
        user = get_user(request)
        member = Member.objects.get(user=user)
        form = MemberFileForm()
        context = {
            'member': member,
            'form': form,
        }
        return render(request, 'members/miembro_editar.html', context)


@api_view(['GET'])
def get_skill_for_register(request):
    if request.method == 'GET':
        snippets = Skill.objects.all()
        serializer = SkillsSerializer(snippets, many=True)
        jsonResponse = JsonResponse(serializer.data, safe=False)
        jsonResponse['Access-Control-Allow-Origin'] = '*'
        return jsonResponse


@api_view(['GET'])
def get_interest_for_register(request):
    if request.method == 'GET':
        snippets = Interest.objects.all()
        serializer = InterestSerializer(snippets, many=True)
        jsonResponse = JsonResponse(serializer.data, safe=False)
        jsonResponse['Access-Control-Allow-Origin'] = '*'
        return jsonResponse
