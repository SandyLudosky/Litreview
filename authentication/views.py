from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.conf import settings

from . import forms


def signup(request):
    form = forms.SignupForm
    template_name = 'authentication/signup.html'
    if request.method == 'POST':
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    context = {
        'form': form,
    }
    return render(
        request,
        template_name,
        context
    )


def login_user(request):
    form = forms.LoginForm()
    template_name = 'authentication/login.html'
    message = ''
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                message = 'Identifiants invalides.'
    context = {
        'form': form,
        'message': message,
    }
    return render(
        request,
        template_name,
        context
    )


def logout_user(request):
    logout(request)
    return redirect('login')
