from django.contrib.auth import logout, login
from django.shortcuts import render, redirect
from django.views.generic import ListView

from user.forms import Registration_form, User_login_form
from django.contrib import messages
# Create your views here.
from user.models import Favorites


def registration(request):
    if request.method=='POST':
        form = Registration_form(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            messages.info(request,'Спасибо за регистрацию')
            return redirect('shoes:home')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = Registration_form()
    return render(request,'user/registration.html',{'form':form})

def user_login(request):
    if request.method == 'POST':
        form = User_login_form(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            messages.info(request, 'Успешная авторизация')
            return redirect('shoes:home')
        else:
            messages.error(request, 'Ошибка авторизации')

    else:
        form = User_login_form()
    return render(request, 'user/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')


class Wishlist(ListView):
    template_name = 'user/wishlist.html'
    model = Favorites
    context_object_name = 'favorite'
