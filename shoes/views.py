from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from cart.models import Cart
from shoes.models import Shoes, Commentary, Answer
from shoes.forms import  GetCommentary, GetReply
from django.contrib import messages
from django.http import Http404
from user.models import Wishlist
from shoes.filters import ShoesFilter
from shoes.services import get_rating_for_views, get_shoes_id_list_by_comments
from cart.services import SessionCart

SEARCH_QUERYSET = [] # сохраняется результат поиска


class SearchView(ListView):
    template_name = 'shoes/shop.html'
    context_object_name = 'shoes'

    def get_queryset(self):
        global SEARCH_QUERYSET
        try:
            if self.request.GET.get('s') != None: # отображаем товары соответствующие поиску
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
        if request.is_ajax(): # добавляем товар в избранное, если он уже там - удаляем
            wishlist = Wishlist.objects.filter(user_id=user, shoes_id=request.GET.get('shoes_id'))
            if wishlist.count() == 0:
                Wishlist.objects.create(user_id=user, shoes_id_id=request.GET.get('shoes_id'))
            else:
                wishlist.delete()
        return super(SearchView, self).get(request, *args, **kwargs)


class ShopView(ListView):
    """ представление-класс для отображения обуви на странице "магазин" """
    template_name = 'shoes/shop.html'
    model = Shoes
    context_object_name = 'shoes'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['filter'] = ShoesFilter(self.request.GET, queryset=self.get_queryset())
        return context

    def get(self, request, *args, **kwargs):
        user = request.user
        if request.is_ajax():
            if request.GET.get('action') == 'wishlist':
                wishlist = Wishlist.objects.filter(user_id=user, shoes_id=request.GET.get('shoes_id'))
                if wishlist.count() == 0:
                    Wishlist.objects.create(user_id=user, shoes_id_id=request.GET.get('shoes_id'))
                else:
                    wishlist.delete()
            else: # добавлем товар в корзину или увеличиваем количество товара в корзине на 1
                if Cart.objects.filter(Q(user_id=user) & Q(shoes_id=request.GET.get('shoes_id'))).count() == 0:
                    Cart.objects.create(user_id=user, shoes_id=request.GET.get('shoes_id'), number=1)
                else:
                    cart = Cart.objects.get(Q(user_id=user) & Q(shoes_id=request.GET.get('shoes_id')))
                    cart.number += 1
                    cart.save()
        return super(ShopView, self).get(request, *args, **kwargs)


class HomeView(ListView):
    """ представление-класс для отображения обуви на главной странице """
    template_name = 'shoes/index.html'
    model = Shoes
    context_object_name = 'shoes'

    # def __init__(self,request, **kwargs):
    #     super().__init__(**kwargs)
    #     if request.user.is_anonymous:



    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(HomeView,self).get_context_data()
        context['first'] = Shoes.objects.first()   # получение первого элемента списка обуви. Далее переделать на получение рандомной обуви
        context["top_shoes_by_comments"] = get_shoes_id_list_by_comments  # топ 20 обуви по количеству комментариев
        user = self.request.user
        context['user'] = user
        return context

    def get(self, request, *args, **kwargs):
        user = request.user
        if request.is_ajax():
            if request.GET.get('action') == 'wishlist':
                wishlist = Wishlist.objects.filter(user_id=user, shoes_id=request.GET.get('shoes_id'))
                if wishlist.count() == 0:
                    Wishlist.objects.create(user_id=user, shoes_id_id=request.GET.get('shoes_id'))
                else:
                    wishlist.delete()
            else:
                if request.user.is_anonymous:
                    cart = SessionCart(request)
                    shoes = get_object_or_404(Shoes, id=request.GET.get('shoes_id'))
                    cart.add(product=shoes,
                             quantity='1')
                else:
                    if Cart.objects.filter(Q(user_id=user) & Q(shoes_id=request.GET.get('shoes_id'))).count() == 0:
                        Cart.objects.create(user_id=user, shoes_id=request.GET.get('shoes_id'), number=1)
                    else:
                        cart = Cart.objects.get(Q(user_id=user) & Q(shoes_id=request.GET.get('shoes_id')))
                        cart.number += 1
                        cart.save()
            return JsonResponse({"data": request.GET.get('shoes_id')}, status=200)
        return super(HomeView, self).get(request, *args, **kwargs)


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
                form = GetCommentary(request.POST)
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
            form = GetReply(request.POST)
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
                return HttpResponseRedirect('request.path_info')
            else:
                messages.error(request, 'Не правильно заполнена форма 2')
        except Exception:
            print('Чет не то с формой')
    else:
        if request.method == 'GET' and request.is_ajax():
            if request.GET.get('action') == 'wishlist':
                wishlist = Wishlist.objects.filter(user_id=user, shoes_id=request.GET.get('shoes_id'))
                if wishlist.count() == 0:
                    Wishlist.objects.create(user_id=user, shoes_id_id=request.GET.get('shoes_id'), size=request.GET.get('size'))
                else:
                    wishlist.delete()
            else:
                if Cart.objects.filter(Q(user_id=user) & Q(shoes_id=request.GET.get('shoes_id'))).count() == 0:
                    Cart.objects.create(user_id=user, shoes_id=request.GET.get('shoes_id'), number=int(request.GET.get('number')))
                else:
                    cart = Cart.objects.get(Q(user_id=user) & Q(shoes_id=request.GET.get('shoes_id')))
                    cart.number += int(request.GET.get('number'))
                    print(request.GET.get('number'))
                    cart.save()
            return JsonResponse({},status=200)
        if (request.GET.get('DeleteReviewButton')):     # удаляем отзыв
            for comment in comments:
                if comment.user == user:
                    comment.delete()
            messages.info(request, 'Отзыв удален')
            return HttpResponseRedirect(request.path_info)
        if comment_exists:                               # создание формы для обновления отзыва
            messages.info(request, 'Просто просмотр 2')
            print(str(comment_exists.user) + '  ' + comment_exists.text + '  ' + str(comment_exists.value))
            form = GetCommentary(
                initial={'shoes': shoes, 'user': user, 'text': comment_exists.text, 'value': comment_exists.value})
            form2 = GetReply(initial={ 'user': user})
            return render(request, 'shoes/single.html',
                          {'form2': form2, 'user': user, "form": form, 'shoes_id': shoes, 'comments': comments,
                           'value': int(comment_exists.value), 'non_empty_comments':non_empty_comments, 'answers':answers})
        else:
            form = GetCommentary(initial={'user': user, 'shoes': shoes})
            form2 = GetReply(initial={'user': user})
            messages.info(request, 'Просто просмотр')
            print(str(comment_exists)+'  '+ str(user))
            return render(request, 'shoes/single.html', {'form2': form2,'user': user, "form": form, 'shoes_id': shoes, 'comments': comments,'non_empty_comments':non_empty_comments,'answers':answers})



