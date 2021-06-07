from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import models

# class Contact_form(forms.Form):
#     subject = forms.CharField(label='Тема', widget=forms.TextInput(attrs={'class': 'form-control'}))
#     content= forms.CharField(label='Текст', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
#     captcha = CaptchaField()

class Registration_form(UserCreationForm):
    username = forms.CharField(label='Логин пользователя', help_text='Не более 150 символов. Только буквы, цифры и символы @/./+/-/_.', widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
   # phone = models.DecimalField(max_digits=12, verbose_name='Номер телефона')
    email = forms.EmailField(label='Электронная почта', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    #ip = models.CharField(max_length=50, verbose_name='IP пользователя', blank=True)
    url = models.SlugField(max_length=150, unique=True)

    class Meta:
        model = User
        fields = ['username','first_name','last_name', 'email', 'password1', 'password2']


class User_login_form(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))



