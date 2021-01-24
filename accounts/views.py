from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages

from images.models import Image
from common.decorators import ajax_required

from .forms import (LoginForm, UserRegistrationForm,
                    ProfileEditForm, UserEditForm)
from .models import Profile, Contact

User = get_user_model()


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
    user_posts = Image.objects.filter(user=request.user)
    context = {'section': 'dashboard',
               'user_posts': user_posts}
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


@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    context = {
        'section': 'people',
        'users': users
    }
    return render(request, 'accounts/user/list.html', context)


@login_required
def user_detail(request, username):
    user = get_object_or_404(User, username=username, is_active=True)
    context = {
        'section': 'people',
        'user': user
    }
    return render(request, 'accounts/user/detail.html', context)


@login_required
@require_POST
@ajax_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action').strip()
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(user_from=request.user,
                                              user_to=user)
            else:
                Contact.objects.filter(user_from=request.user,
                                       user_to=user).delete()
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error'})
    return JsonResponse({'status': 'error'})
