from django.db.models import Q
from django.views.generic import ListView
from shoes.models import Shoes
from django.contrib import messages
from user.models import Wishlist
from cart.models import Cart
from django.http import  JsonResponse
from django.template.loader import render_to_string


class WishlistView(ListView):
    template_name = 'user/wishlist.html'
    model = Shoes
    context_object_name = 'favorite'

    def get_queryset(self):
        user_wishlist = Wishlist.objects.filter(user_id=self.request.user).values_list('shoes_id', flat=True)
        queryset = Shoes.objects.filter(pk__in=user_wishlist)
        return queryset

    def get(self, request, *args, **kwargs):
        user = request.user
        if request.is_ajax():
            if request.GET.get('action')== 'delete':
                try:
                    wishlist = Wishlist.objects.get(user_id=user, shoes_id=request.GET.get('shoes_id'))
                    wishlist.delete()
                    user_wishlist = Wishlist.objects.filter(user_id=self.request.user).values_list('shoes_id',
                                                                                                flat=True)
                    context = {'favorite': Shoes.objects.filter(pk__in=user_wishlist)}
                    html = render_to_string('user/favorites_list.html', context)
                    return JsonResponse({'html':html}, status=200,content_type="application/json")
                except Exception:
                    messages.info(request, 'Не удалось удалить обьект с избранного')
            if request.GET.get('action') == 'cart':
                try:
                    if Cart.objects.filter(Q(user_id=user) & Q(shoes_id=request.GET.get('shoes_id'))).count() == 0:
                        Cart.objects.create(user_id=user, shoes_id=request.GET.get('shoes_id'), number=1)
                    else:
                        cart = Cart.objects.get(Q(user_id=user) & Q(shoes_id=request.GET.get('shoes_id')))
                        cart.number+=1
                        cart.save()
                except Exception:
                    messages.info(request, 'Не удалось обавить обьект в корзину')
        return super(WishlistView, self).get(request, *args, **kwargs)

