from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.defaults import page_not_found
from rest_framework.decorators import api_view

from core.aux import generate_slug


def about(request):
    return render(request, 'core/about.html')


