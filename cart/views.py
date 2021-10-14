from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from cart.models import Cart
from shoes.models import Shoes
from django.contrib import messages
from cart.services import get_total_sum, get_queryset_func, SessionCart, get_total_sum_session


# Create your views here.


class CartView(ListView):
    template_name = 'cart/cart.html'
    model = Shoes
    context_object_name = 'shoes'

    def get_queryset(self):
        if self.request.user.is_anonymous:
            cart = SessionCart(self.request)
            querylist = cart.cart.keys()
            queryset = Shoes.objects.filter(pk__in=querylist)
            for item in queryset:
                item.sum_price = item.price * int(cart.cart[str(item.pk)]['quantity'])
                item.quantity = int(cart.cart[str(item.pk)]['quantity'])
                item.save()
                # print(item.pk)
                # print(item.price)
                # print(cart.cart[str(item.pk)]['quantity'])
                # print(item.sum_price)

        else:
            queryset = get_queryset_func(self.request)
            for item in queryset:
                sum = item.cart_set.get(shoes_id=item.pk)
                item.sum_price = item.price * sum.number
                item.save()
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        total_sum = 0
        quantity = []
        context = super().get_context_data()
        if self.request.user.is_anonymous:
            # cart = SessionCart(self.request)
            # for item in cart:
            #     quantity.append(int(item['quantity']))
            # context['cart'] = quantity
            for item in self.get_queryset():
                total_sum += int(item.sum_price)
        else:
            context['cart'] = Cart.objects.filter(user_id=self.request.user)
            for item in self.get_queryset():
                total_sum += item.sum_price
        # mydict = [{'shoes': 5, 'num':2}, {'shoes':3, 'num': 6}]
        # context['mydict'] = mydict
        context['total_sum'] = total_sum
        return context

    def get(self, request, *args, **kwargs):
        user = request.user
        if request.is_ajax():
            # if self.request.user.is_anonymous:
            #
            #     html = get_total_sum(self, request)
            #     return JsonResponse({'html': html}, status=200, content_type="application/json")
            #else:
            if request.GET.get('action') == 'delete':
                if self.request.user.is_anonymous:
                    try:
                        cart = SessionCart(self.request)
                        # shoes = request.GET.get('shoes_id')
                        # product = Shoes.objects.get(pk=shoes)
                        shoes = get_object_or_404(Shoes, id=request.GET.get('shoes_id'))
                        cart.remove(shoes)
                        html = get_total_sum_session(self, request)
                        return JsonResponse({'html': html}, status=200, content_type="application/json")
                    except Exception:
                        messages.info(request, 'Не удалось удалить обьект с корзины')
                else:
                    try:
                        cartlist = Cart.objects.get(user_id=user, shoes=request.GET.get('shoes_id'))
                        cartlist.delete()
                        html = get_total_sum(self, request)
                        return JsonResponse({'html': html}, status=200, content_type="application/json")
                    except Exception:
                        messages.info(request, 'Не удалось удалить обьект с корзины')
            elif request.GET.get('action') == 'number':
                if self.request.user.is_anonymous:
                    try:
                        cart = SessionCart(self.request)
                        cart.cart[request.GET.get('shoes_id')]['quantity'] = request.GET.get('number')
                        cart.save()
                        html = get_total_sum_session(self, request)
                        return JsonResponse({'html': html}, status=200, content_type="application/json")
                    except Exception:
                        messages.info(request, 'Не удалось обновить количество товара в корзине')
                else:
                    try:
                        cart = Cart.objects.get(Q(user_id=user) & Q(shoes=request.GET.get('shoes_id')))
                        cart.number = request.GET.get('number')
                        cart.save()
                        html = get_total_sum(self, request)
                        return JsonResponse({'html': html}, status=200, content_type="application/json")
                    except Exception:
                        messages.info(request, 'Не удалось обновить количество товара в корзине')
            else:
                messages.info(request, 'Не отработало')
        return super(CartView, self).get(request, *args, **kwargs)
