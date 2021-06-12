from django.shortcuts import render
from django.views.generic import ListView, DetailView,CreateView
from django.core.paginator import Paginator
from shoesiki import settings
from shoes.models import Shoes, Rating
import statistics

class Home(ListView):
    template_name = 'shoes/index.html'
    model = Shoes
    context_object_name = 'shoes'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['first'] = Shoes.objects.first()
        return context

    # def get_queryset(self, *args, **kwargs):
    #     return Shoes.objects.filter(tags__name=self.kwargs['slug'])

class ShoesDetailview(DetailView):
    template_name = 'shoes/single.html'
    model = Shoes
    context_object_name = 'shoes_id'
    slug_field = 'url'

    # def get_queryset(self, *args, **kwargs):
    #     return Shoes.objects.get(pk=self.kwargs['pk'])


# Create your views here.


