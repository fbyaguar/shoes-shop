from django.shortcuts import render
from django.views.generic import ListView, DetailView,CreateView
from django.core.paginator import Paginator
from shoesiki import settings


# class Home(ListView):
#     template_name = 'shoes/index.html'
from shoesiki.settings import *


def Home(request):
    return render(request, 'shoes/index.html')
# Create your views here.
