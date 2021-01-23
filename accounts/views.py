from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import (LoginForm, UserRegistrationForm,
                    ProfileEditForm, UserEditForm)
from .models import Profile


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            username = cd['username']
            password = cd['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated Successfully')
                else:
                    return HttpResponse('Disabled Account')
            else:
                return HttpResponse('Invalid Login')
    form = LoginForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/login.html', context)


@login_required
def dashboard(request):
    context = {'section': 'dashboard'}
    return render(request, 'accounts/dashboard.html', context)


def register_view(request):
    if request.method == 'POST':
        register_form = UserRegistrationForm(data=request.POST)
        if register_form.is_valid():
            new_user = register_form.save(commit=False)
            new_user.set_password(register_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            context = {'new_user': new_user}
            return render(request, 'accounts/register_done.html', context)
    register_form = UserRegistrationForm()
    context = {'user_form': register_form}
    return render(request, 'accounts/register.html', context)


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile Updated Successfully")
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'accounts/edit.html', context)
