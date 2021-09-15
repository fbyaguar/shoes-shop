from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView,CreateView
from django.core.paginator import Paginator
from shoesiki import settings
from shoes.models import Shoes, Commentary,Answer, Category, Brand, Country, Season
import statistics
from shoes.forms import  Get_commentary ,  Get_reply
from django.contrib import messages
from django.http import Http404
from shoes.templatetags.shoes_tags import get_rating_for_views, get_shoes_id_list_by_comments
# from user.forms import Add_to_wishlist_form
from user.models import Wishlist

choise_f = 0
average_rating = 0
SEARCH_QUERYSET = []
from shoes.filters import ShoesFilter


class Search(ListView):

    template_name = 'shoes/shop.html'
    #model = Shoes
    context_object_name = 'shoes'

    def get_queryset(self):
        global SEARCH_QUERYSET
        try:
            if self.request.GET.get('s') != None:
                SEARCH_QUERYSET = Shoes.objects.filter(
                    Q(title__icontains=self.request.GET.get('s')) | Q(brand__title__icontains=self.request.GET.get('s'))
                    | Q(content__icontains=self.request.GET.get('s')))
                return SEARCH_QUERYSET
            else:
                return SEARCH_QUERYSET
        except Exception:
            raise Http404("Error. Wrong queryset")

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['s'] = self.request.GET.get('s')
        context['filter'] = ShoesFilter(self.request.GET, queryset=self.get_queryset())
        return context

    def get(self, request, *args, **kwargs):
        user = request.user
        if request.is_ajax():
            wishlist = Wishlist.objects.filter(user_id=user, shoes_id=request.GET.get('shoes_id'))
            if wishlist.count() == 0:
                Wishlist.objects.create(user_id=user, shoes_id_id=request.GET.get('shoes_id'))
            else:
                wishlist.delete()

        return super(Search, self).get(request, *args, **kwargs)






class Shop(ListView):
    """ представление-класс для отображения обуви на странице "магазин" """
    template_name = 'shoes/shop.html'
    model = Shoes
    context_object_name = 'shoes'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        # context['categories'] = Category.objects.all()
        # context['brands'] = Brand.objects.all()
        # context['countries'] = Country.objects.all()
        # context['seasons'] = Season.objects.all()
        context['filter'] = ShoesFilter(self.request.GET, queryset=self.get_queryset())
        return context

    def get(self, request, *args, **kwargs):
        user = request.user
        if request.is_ajax():
            wishlist = Wishlist.objects.filter(user_id=user, shoes_id=request.GET.get('shoes_id'))
            if wishlist.count() == 0:
                Wishlist.objects.create(user_id=user, shoes_id_id=request.GET.get('shoes_id'))
            else:
                wishlist.delete()

        return super(Shop, self).get(request, *args, **kwargs)



# class Home(ListView):
#     """ представление-класс для отображения обуви на главной странице """
#     template_name = 'shoes/index.html'
#     model = Shoes
#     context_object_name = 'shoes'
#
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super(Home,self).get_context_data()
#         context['first'] = Shoes.objects.first()   # получение первого элемента списка обуви. Далее переделать на получение рандомной обуви
#         context["top_shoes_by_comments"] = get_shoes_id_list_by_comments  # топ 20 обуви по количеству комментариев
#         context['form'] = Add_to_wishlist_form()
#         return context
#
#
#     def post(self,request):
#         form = Add_to_wishlist_form(request.POST)
#         if form.is_valid():
#             #wishlist = form.save(commit=False)
#             form.save()
#             return HttpResponseRedirect(request.path_info)
#         else:
#             messages.error(request, 'Не удалось добавить избранное')


def homeview(request):
    shoes = Shoes.objects.all()
    user = request.user
    if request.method=='GET' and request.is_ajax():
        wishlist = Wishlist.objects.filter(user_id=user, shoes_id=request.GET.get('shoes_id'))
        if wishlist.count() == 0:
            Wishlist.objects.create(user_id=user, shoes_id_id=request.GET.get('shoes_id'))
        else:
            wishlist.delete()
        return JsonResponse({"data": request.GET.get('shoes_id')}, status=200)
    elif request.method == 'POST':
        pass
    else:
        first = Shoes.objects.first()  # получение первого элемента списка обуви. Далее переделать на получение рандомной обуви
        top_shoes_by_comments = get_shoes_id_list_by_comments
        return render(request, 'shoes/index.html',
                      {'shoes': shoes, 'first':first, 'top_shoes_by_comments': top_shoes_by_comments, 'user':user })


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

        try:
            if  request.POST['rating']:       # проверяем существует ли ключ "рейтинг". Ловим ошибку, если его нет и обрабатываем форму для
                                             # ответа. Если есть обрабатываем форму для отзыва.
                form = Get_commentary(request.POST)
                print('форма 1')
                if form.is_valid():
                    if comment_exists:  # обновляем отзыв
                        comment_exists.text = form.cleaned_data['text']
                        comment_exists.value = request.POST['rating']
                        comment_exists.save()
                        shoes.rating = get_rating_for_views(id)
                        shoes.save()
                        messages.info(request, 'Отзыв обновлен')
                        return HttpResponseRedirect(request.path_info)
                    else:
                        review = form.save(commit=False)  # добавляем отзыв
                        try:  # если оценку не оставили, она = 0
                            review.value = request.POST['rating']
                        except Exception:
                            review.value = 0
                        review.save()
                        shoes.rating = get_rating_for_views(id)
                        shoes.save()
                        messages.info(request, 'Спасибо за отзыв')
                        return HttpResponseRedirect(request.path_info)
                else:
                    messages.error(request, 'Не удалось добавить отзыв')
        except KeyError:
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
                return HttpResponseRedirect('home')
            else:
                messages.error(request, 'Не правильно заполнена форма 2')
        except Exception:
            print('Чет не то с формой')
    else:
        if (request.GET.get('DeleteReviewButton')):     # удаляем отзыв
            for comment in comments:
                if comment.user == user:
                    comment.delete()
            messages.info(request, 'Отзыв удален')
            return HttpResponseRedirect(request.path_info)

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



