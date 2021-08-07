from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView,CreateView
from django.core.paginator import Paginator
from shoesiki import settings
from shoes.models import Shoes, Commentary,Answer
import statistics
from shoes.forms import  Get_commentary ,  Get_reply
from django.contrib import messages
from django.http import Http404
from shoes.templatetags.shoes_tags import get_rating_for_views
choise_f = 0
average_rating = 0



class Home(ListView):
    """ представление-класс для отображения обуви на главной странице """
    template_name = 'shoes/index.html'
    model = Shoes
    context_object_name = 'shoes'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['first'] = Shoes.objects.first()   # получение первого элемента списка обуви. Далее переделать на получение рандомной обуви
        return context


# Create your views here.

def review(request, slug):
    """ Функция-представление для страницы single.html """
    try:
        shoes = Shoes.objects.get(slug=slug)
    except Exception:
        raise Http404("Shoes object does not exist") # если обувь не найдена
    shoes.views+=1
    shoes.save()
    user = request.user
    id = shoes.id
    non_empty_comments = Commentary.objects.filter(shoes_id=id).exclude(text='') #находим отзывы с комментариями
    comments = Commentary.objects.filter(shoes_id=id)
    answers = Answer.objects.filter(commentary__in=comments)
    print(answers)
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
        if choise_f == 0:
            form = Get_commentary(request.POST)
            print('форма 1')
            if form.is_valid():
                if comment_exists:  # обновляем отзыв
                    comment_exists.text = form.cleaned_data['text']
                    comment_exists.value = request.POST['rating']
                    comment_exists.save()
             #       get_rating_for_views(id)
                    messages.info(request, 'Отзыв обновлен')
                    return HttpResponseRedirect(request.path_info)
                else:
                    review = form.save(commit=False)  # добавляем отзыв
                    try:  # если оценку не оставили, она = 0
                        review.value = request.POST['rating']
                    except Exception:
                        review.value = 0
                    review.save()
                    messages.info(request, 'Спасибо за отзыв')
                    return HttpResponseRedirect(request.path_info)
            else:
                messages.error(request, 'Не удалось добавить отзыв')
        elif choise_f == 1:
            form = Get_reply(request.POST)
            print('форма 2')
            if form.is_valid():
                answer = form.save(commit=False)
                try:
                    print(type(answer.commentary))
                    print(type(request.POST['comment-id']))
                    answer.commentary_id = int(request.POST.get('comment-id'))
                except Exception:
                    messages.error(request, 'Не удалось добавить отзыв. Не правильно добвлен пользователь')
                answer.save()
                messages.info(request, 'Ответ добавлен')
                return HttpResponseRedirect(request.path_info)
            else:
                messages.error(request, 'Не правильно заполнена форма 2')
        else:
            print('Чет не то с формой')
    else:
        if (request.GET.get('DeleteReviewButton')):     # удаляем отзыв
            for comment in comments:
                if comment.user == user:
                    comment.delete()
            messages.info(request, 'Отзыв удален')
            return HttpResponseRedirect(request.path_info)

        # if (request.GET.get('ReplyReviewbutton')):
        #     commentary = get_comment_text
        #     form = Get_reply(initial={'user': user, 'commentary': commentary})
        #     messages.info(request, 'Просто просмотр')
        #     print(str(comment_exists) + '  ' + str(user))
        #     return render(request, 'shoes/single.html',
        #                   {'user': user, "form": form, 'shoes_id': shoes, 'comments': comments,
        #                    'non_empty_comments': non_empty_comments})

        # if choise_f == 1:
        #     print('форма 2 загружена')
        #     form = Get_reply(
        #     initial={ 'user': user})
        #     return render(request, 'shoes/single.html',
        #               {'user': user, "form": form, 'shoes_id': shoes,'comments': comments})

        if comment_exists:                               # создание формы для обновления отзыва
            messages.info(request, 'Просто просмотр 2')
            print(str(comment_exists.user) + '  ' + comment_exists.text + '  ' + str(comment_exists.value))
            form = Get_commentary(
                initial={'shoes': shoes, 'user': user, 'text': comment_exists.text, 'value': comment_exists.value})
            form2 = Get_reply(initial={ 'user': user})
            return render(request, 'shoes/single.html',
                          {'form2': form2, 'user': user, "form": form, 'shoes_id': shoes, 'comments': comments,
                           'value': int(comment_exists.value), 'non_empty_comments':non_empty_comments, 'answers':answers})
        else:
            form = Get_commentary(initial={'user': user, 'shoes': shoes})
            form2 = Get_reply(initial={'user': user})
            messages.info(request, 'Просто просмотр')
            print(str(comment_exists)+'  '+ str(user))
            return render(request, 'shoes/single.html', {'form2': form2,'user': user, "form": form, 'shoes_id': shoes, 'comments': comments,'non_empty_comments':non_empty_comments,'answers':answers})
