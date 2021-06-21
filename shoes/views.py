from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView,CreateView
from django.core.paginator import Paginator
from shoesiki import settings
from shoes.models import Shoes, Commentary
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
    id = shoes.id
    comments = Commentary.objects.filter(shoes_id=id)
    comment_exists = comments.get(user=user)
    if request.method == 'POST':
        form = Get_commentary(request.POST)
        if form.is_valid():
            if comment_exists:
                comment_exists.text = form.cleaned_data['text']
                comment_exists.value = request.POST['rating']
                comment_exists.save()
                messages.info(request, 'Отзыв обновлен')
            else:
                review = form.save(commit=False)
                review.value = request.POST['rating']
                review.save()
                messages.info(request, 'Спасибо за отзыв')
                return redirect('home')
        else:
            messages.error(request, 'Не удалось добавить отзыв')
    else :
        if comment_exists:
            print(str(comment_exists.user)+ '  ' + comment_exists.text +'  ' + str(comment_exists.value))
            form = Get_commentary(initial={'shoes':shoes,'user':user,'text':comment_exists.text,'value':comment_exists.value})
        else:
            form = Get_commentary(initial={'user': user, 'shoes':shoes})
        messages.info(request, 'Просто просмотр')


    return render(request, 'shoes/single.html', { 'user': user, "form": form, 'shoes_id': shoes, 'comments':comments, 'value':int(comment_exists.value)})
