from shoes.models import Shoes
from cart.models import Cart


def add_variable_to_context(request):
    if request.user.is_anonymous:
        return {
            'shoes_in_cart': '',

        }
    else:
        user_cartlist = Cart.objects.filter(user_id=request.user).values_list('shoes',flat=True)
        queryset = Shoes.objects.filter(pk__in=user_cartlist)
        return {
        'shoes_in_cart': queryset,

    }