from shoes.models import Shoes
from cart.models import Cart
from cart.services import SessionCart


def add_variable_to_context(request):
    querylist = []
    if request.user.is_anonymous:
        cart = SessionCart(request)
        querylist = cart.cart.keys()
        queryset = Shoes.objects.filter(pk__in=querylist)
        return {

            'shoes_in_cart': queryset,

        }
    else:
        user_cartlist = Cart.objects.filter(user_id=request.user).values_list('shoes',flat=True)
        queryset = Shoes.objects.filter(pk__in=user_cartlist)
        return {
        'shoes_in_cart': queryset,

    }


