from django.http import JsonResponse
from django.template.loader import render_to_string
from cart.models import Cart
from shoes.models import Shoes



def get_queryset_func(request):
    cart = Cart.objects.filter(user_id=request.user).values_list('shoes', flat=True)
    queryset = Shoes.objects.filter(pk__in=cart)
    return queryset


def get_total_sum(self,request):
    total_sum = 0
    queryset = get_queryset_func(request)
    for item in queryset:
        sum = item.cart_set.get(shoes_id=item.pk)
        item.sum_price = item.price * sum.number
        item.save()
    for item in self.get_queryset():
        total_sum += item.sum_price
    context = {'shoes': queryset, 'total_sum': total_sum}
    html = render_to_string('cart/cart_list.html', context)
    return html