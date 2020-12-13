from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from account.forms import LoginForm, UserRegistrationForm, ProfileEditForm, UserEditForm
from account.models import Profile


@login_required
def user_list(req):
    users = User.objects.filter(is_active=True)

    return render(req, 'account/user/list.html', {'section': 'people', 'users': users})


@login_required
def user_detail(req, username):
    user = get_object_or_404(User,
                             username=username,
                             is_active=True)

    return render(req, 'account/user/detail.html', {'section': 'people', 'user': user})


@login_required
def edit(req):

    if req.method == 'POST':
        user_form = UserEditForm(
            instance=req.user, data=req.POST
        )
        profile_form = ProfileEditForm(
            instance=req.user.profile, data=req.POST, files=req.FILES
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            messages.success(req, 'It did what it did...')
        else:
            messages.error(req, 'Not good...')
    else:
        user_form = UserEditForm(instance=req.user)
        profile_form = ProfileEditForm(instance=req.user.profile)

    return render(req, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form})


def user_login(req):

    if req.method == 'POST':
        form = LoginForm(req.POST)

        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(req,
                                username=cd['username'],
                                password=cd['password'])

            if user is not None:
                if user.is_active:
                    login(req, user)

                    return HttpResponse('Authenticated successfuly')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()

    return render(req, 'account/login.html', {'form': form})


@login_required
def dashboard(req):
    return render(req, 'account/dashboard.html', {'selection': 'dashboard'})


def register(req):

    if req.method == 'POST':
        user_form = UserRegistrationForm(req.POST)

        if user_form.is_valid():
            new_user = user_form.save(commit=False)

            new_user.set_password(
                user_form.cleaned_data['password']
            )
            new_user.save()

            Profile.objects.create(user=new_user)

            return render(req, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()

    return render(req, 'account/register.html', {'user_form': user_form})
