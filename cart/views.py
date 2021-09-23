from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic import ListView
from cart.models import Cart
from shoes.models import Shoes
from django.contrib import messages
# Create your views here.




class CartView(ListView):
    template_name = 'cart/cart.html'
    model = Shoes
    context_object_name = 'shoes'

    def get_queryset(self):
        cart = Cart.objects.filter(user_id=self.request.user).values_list('shoes', flat=True)
        queryset = Shoes.objects.filter(pk__in=cart)
        for item in queryset:
            sum = item.cart_set.get(shoes_id=item.pk)
            item.sum_price = item.price * sum.number
            item.save()
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        total_sum = 0
        context = super().get_context_data()
        context['cart'] = Cart.objects.filter(user_id=self.request.user)
        for item in self.get_queryset():
            total_sum += item.sum_price
        context['total_sum'] = total_sum
        return context

    def get(self, request, *args, **kwargs):
        user = request.user

        if request.is_ajax():
            if request.GET.get('action')== 'delete':
                total_sum = 0
                try:
                    cartlist = Cart.objects.get(user_id=user, shoes=request.GET.get('shoes_id'))
                    cartlist.delete()
                    user_cartlist = Cart.objects.filter(user_id=self.request.user).values_list('shoes',
                                                                                               flat=True)

                    queryset = Shoes.objects.filter(pk__in=user_cartlist)
                    for item in queryset:
                        sum = item.cart_set.get(shoes_id=item.pk)
                        item.sum_price = item.price * sum.number
                        item.save()

                    for item in self.get_queryset():
                        total_sum += item.sum_price
                    context = {'shoes': queryset, 'total_sum': total_sum}
                    html = render_to_string('cart/cart_list.html', context)
                    print('должен быть хтмл')
                    print(html)
                    return JsonResponse({'html':html}, status=200,content_type="application/json")
                except Exception:
                    messages.info(request, 'Не удалось удалить обьект с корзины')
            elif request.GET.get('action') == 'number':
                total_sum = 0
                try:
                    cart = Cart.objects.get(Q(user_id=user) & Q(shoes=request.GET.get('shoes_id')))
                    cart.number = request.GET.get('number')
                    cart.save()
                    user_cartlist = Cart.objects.filter(user_id=self.request.user).values_list('shoes',
                                                                                               flat=True)
                    queryset = Shoes.objects.filter(pk__in=user_cartlist)
                    for item in queryset:
                        sum = item.cart_set.get(shoes_id=item.pk)
                        item.sum_price = item.price * sum.number
                        item.save()

                    for item in self.get_queryset():
                        total_sum += item.sum_price
                    context = {'shoes': queryset, 'total_sum': total_sum}
                    html = render_to_string('cart/cart_list.html', context)
                    print('должен быть хтмл')
                    print(html)
                    print('а это контекст')
                    print(context)
                    return JsonResponse({'html': html}, status=200, content_type="application/json")
                except Exception:
                    messages.info(request, 'Не удалось обновить количество товара в корзине')
            else:
                messages.info(request, 'Не отработало')
        return super(CartView, self).get(request, *args, **kwargs)
