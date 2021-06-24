from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView,CreateView
from django.core.paginator import Paginator
from shoesiki import settings
from shoes.models import Shoes, Commentary
import statistics
from shoes.forms import  Get_commentary
from django.contrib import messages
from django.http import Http404



class Home(ListView):
    template_name = 'shoes/index.html'
    model = Shoes
    context_object_name = 'shoes'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['first'] = Shoes.objects.first()
        return context


# Create your views here.

def review(request, slug):
    try:
        shoes = Shoes.objects.get(slug=slug)
    except Exception:
        raise Http404("Shoes object does not exist")
    user = request.user
    id = shoes.id
    non_empty_comments = Commentary.objects.filter(shoes_id=id).exclude(text='') #находим отзывы с комментариями
    comments = Commentary.objects.filter(shoes_id=id)
    if request.user.is_anonymous:
        comment_exists = None
        print('anonim')
    else:
        try:
            comment_exists = comments.get(user=user)
            print('vse norm')
        except  Commentary.DoesNotExist:                 #отзыва не существует
            comment_exists = None
        except 	Exception:                               #невозможно выбрать отзыв. Удаляем
            comment_exists = comments.filter(user=user)
            comment_exists.delete()
    if request.method == 'POST':
        form = Get_commentary(request.POST)
        if form.is_valid():
            if comment_exists:
                comment_exists.text = form.cleaned_data['text']
                comment_exists.value = request.POST['rating']
                comment_exists.save()
                messages.info(request, 'Отзыв обновлен')
                return redirect('home')
            else:
                review = form.save(commit=False)
                try:                                    # если оценку не оставили, она = 0
                    review.value = request.POST['rating']
                except Exception:
                    review.value = 0
                review.save()
                messages.info(request, 'Спасибо за отзыв')
                return redirect('home')
        else:
            messages.error(request, 'Не удалось добавить отзыв')
    else:
        if comment_exists:
            messages.info(request, 'Просто просмотр 2')
            print(str(comment_exists.user) + '  ' + comment_exists.text + '  ' + str(comment_exists.value))
            form = Get_commentary(
                initial={'shoes': shoes, 'user': user, 'text': comment_exists.text, 'value': comment_exists.value})
            return render(request, 'shoes/single.html',
                          {'user': user, "form": form, 'shoes_id': shoes, 'comments': comments,
                           'value': int(comment_exists.value), 'non_empty_comments':non_empty_comments})
        else:
            form = Get_commentary(initial={'user': user, 'shoes': shoes})
            messages.info(request, 'Просто просмотр')
            print(str(comment_exists)+'  '+ str(user))
            return render(request, 'shoes/single.html', {'user': user, "form": form, 'shoes_id': shoes, 'comments': comments,'non_empty_comments':non_empty_comments})
