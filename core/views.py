from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.defaults import page_not_found
from rest_framework.decorators import api_view

from core.aux import generate_slug
from members.aux import add_skill_generic, add_interest_generic
from members.forms import MemberFileForm
from members.models import Member


def about(request):
    return render(request, 'core/about.html')


def social_register(request):
    messages.warning(request, 'Este correo ya tiene una cuenta asociada')
    return redirect('core:register')


def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']
        already_register_email = User.objects.filter(email=email)
        already_register_username = User.objects.filter(username=username)

        if already_register_email.count() != 0:
            messages.warning(request, 'Este correo ya tiene una cuenta asociada')
            return redirect('core:register')

        if already_register_username.count() != 0:
            messages.warning(request, 'Este username ya fue tomado')
            return redirect('core:register')

        if password != password2:
            messages.warning(request, 'Ambas contraseñas deben coincidir.')
            return redirect('core:register')
        user = User.objects.create_user(username=username,
                                        email=email, password=password)
        user.save()
        slug_member = generate_slug(Member)
        member = Member(user=user, slug=slug_member)
        member.save()
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('members:update-user')
        else:
            return render(request, 'core/register.html')
    else:
        return render(request, 'core/register.html')


def newRegister(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        summary = request.POST.get('summary')
        phone = request.POST.get('phone')
        linkin = request.POST.get('linkin')
        description = request.POST.get('description')
        interest = request.POST.getlist('interest')
        skill = request.POST.getlist('skill')
        # image = request.FILES['image']

        already_register_email = User.objects.filter(email=email)
        already_register_username = User.objects.filter(username=username)

        if already_register_email.count() != 0:
            messages.warning(request, 'Este correo ya tiene una cuenta asociada')
            return redirect('core:newRegister')

        if already_register_username.count() != 0:
            messages.warning(request, 'Este username ya fue tomado')
            return redirect('core:newRegister')

        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            user.save()
            print('Usuario creado correctamente')

        except Exception as e:
            print('Error al crear el usuario', e)

        try:
            slug_member = generate_slug(Member)
            member = Member(
                user=user,
                slug=slug_member,
                name=name,
                summary=summary,
                description=description,
                linkedin=linkin,
                phone=phone
            )
            member.save()

            form = MemberFileForm(request.POST, request.FILES, instance=member)

            if form.is_valid():
                form.save()
                print(form)
                print('archivos creados correctamente')

            print('Miembro creado correctamente')

        except Exception as e:
            print('Error al crear el miembro', e)

        try:
            user = authenticate(
                request,
                username=username,
                password=password
            )
            print('Auth creada correctamente')

        except Exception as e:
            print('Error al  auth', e)

        try:
            for s in skill:
                add_skill_generic(s, user)
            print('SKILL creado correctamente')
        except Exception as e:
            print('Error al crear el SKILL', e)

        try:
            for i in interest:
                add_interest_generic(i, user)
            print('SKILL creado correctamente')
        except Exception as e:
            print('Error al crear el SKILL', e)

        if user is not None:
            login(request, user)
            return redirect('members:miembros')
        else:
            return render(request, 'core/newRegister.html')
    else:
        return render(request, 'core/newRegister.html')


@api_view(['POST'])
def verify_mail(request):
    if request.method == 'POST':
        email = request.POST['email']
        already_register_email = User.objects.filter(email=email)
        if already_register_email.count() != 0:
            data = {'existe': 'true'}
        else:
            data = {'existe': 'false'}
        response = JsonResponse(data, status=200)
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Headers'] = 'Content-Type, Access-Control-Allow-Headers, Authorization, ' \
                                                   'X-Requested-With '
        return response


@api_view(['POST'])
def verify_username(request):
    if request.method == 'POST':
        username = request.POST['username']
        already_register_username = User.objects.filter(username=username)

        if already_register_username.count() != 0:
            data = {'existe': 'true'}
        else:
            data = {'existe': 'false'}
        response = JsonResponse(data, status=200)
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Headers'] = 'Content-Type, Access-Control-Allow-Headers, Authorization, ' \
                                                   'X-Requested-With '
        return response


def login_view(request):
    if request.method == 'POST':
        print('Yeet')
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            messages.success(request, 'Bienvenido.')
            login(request, user)
            return redirect('projects:proyectos')
        else:
            print('is none')
            return redirect('core:login')
    else:
        messages.warning(request, 'Correo o contraseña incorrecto.')
        return render(request, 'core/login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('core:about')


def user_verification(request):
    user = get_user(request)
    member = Member.objects.filter(user=user)
    if member.count() == 0:
        slug_member = generate_slug(Member)
        member = Member(user=user, slug=slug_member)
        member.save()
        return redirect('members:update-user')
    else:
        return redirect('core:about')


def handler404(request, exception):
    return page_not_found(request, exception, template_name='core/404.html')
