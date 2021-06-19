from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView,CreateView
from django.core.paginator import Paginator
from shoesiki import settings
from shoes.models import Shoes
import statistics
from shoes.forms import  Get_commentary
from django.contrib import messages



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

# class ShoesDetailview(DetailView):
#     template_name = 'shoes/single.html'
#     model = Shoes
#     context_object_name = 'shoes_id'
#     slug_field = 'url'

    # def get_queryset(self, *args, **kwargs):
    #     return Shoes.objects.get(pk=self.kwargs['pk'])


# Create your views here.

def review(request, slug):
    shoes = Shoes.objects.get(slug=slug)
    user = request.user
    if request.method == 'POST':
        form = Get_commentary(request.POST)
        # form.fields['value'] =str(1) # form.cleaned_data['rating']
        # form.fields['shoes'] = shoes.id
       # print (form.is_valid())
        if form.is_valid():

            review = form.save(commit=False)
            review.value = request.POST['rating']
            review.save()
            messages.info(request, 'Спасибо за оценку')
            return redirect('home')
         #   News.objects.create(**form.cleaned_data)    для не связанной с моделью формы
           # return redirect(review)
        else:
            #form.errors.
            messages.error(request, 'Не удалось поставить оценку')
    else :
        form = Get_commentary(initial={'user': user, 'shoes':shoes, 'parent': None})
        messages.info(request, 'Просто просмотр')

    return render(request, 'shoes/single.html', { 'user': user, "form": form, 'shoes_id': shoes})
