from django.shortcuts import render
from django.views.generic import ListView, DetailView,CreateView
from django.core.paginator import Paginator
from shoesiki import settings
from shoes.models import *

class Home(ListView):
    template_name = 'shoes/index.html'
    model = Shoes
    context_object_name = 'shoes'

    # def get_queryset(self, *args, **kwargs):
    #     return Shoes.objects.filter(tags__name=self.kwargs['slug'])

class ShoesDetailview(DetailView):
    template_name = 'shoes/index.html'
    model = Shoes
    context_object_name = 'shoes'

    def get_queryset(self, *args, **kwargs):
        return Shoes.objects.get(id=self.kwargs['pk'])
# Create your views here.
