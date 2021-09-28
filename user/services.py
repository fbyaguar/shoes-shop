from django.contrib.auth import logout, login
from django.shortcuts import render, redirect
from user.forms import RegistrationForm, UserLoginForm
from django.contrib import messages


def registration(request):
    if request.method=='POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            messages.info(request,'Спасибо за регистрацию')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = RegistrationForm()
    return render(request,'user/registration.html',{'form':form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            messages.info(request, 'Успешная авторизация')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка авторизации')
    else:
        form = UserLoginForm()
    return render(request, 'user/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home')