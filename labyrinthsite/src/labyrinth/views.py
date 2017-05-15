# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from .models import MyUser
from labyrinth.forms import RegistrationForm

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
import json
import re
# Create your views here.

def index(request):
    return render(request, 'index.html', {'form': login(request)})

def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(
                username = cd['username'],
                first_name = cd['first_name'],
                password = cd['password1'],
                email = cd['email'])
            profile = MyUser.objects.create(
                user = user,
                phone = cd['phone'],
                age = cd['age'],
                gender = cd['gender']
            )
            profile.save()
            auth.login(request, profile.user)
            return redirect(index)
    else:
        form = RegistrationForm()
 
    return render(request, 'registration.html', {'form': form})

def get_profile(request):
    profile = None
    if request.user.is_authenticated():
        profile = MyUser.objects.get(user=request.user)
    return profile

def logout(request):
    auth.logout(request)
    return redirect(index)

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = auth.authenticate(username=form.cleaned_data['username'],
                                     password=form.cleaned_data['password'])
            if user and user.is_active:
                auth.login(request, form.get_user())
                return HttpResponseRedirect('/')
    else:
        form = AuthenticationForm()
    return form

def info(request):
    return render(request, 'info.html', {'profile': get_profile(request)})