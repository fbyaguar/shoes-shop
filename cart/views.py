from django.shortcuts import render
from django.views.generic import ListView
from cart.models import Cart
from shoes.models import Shoes
# Create your views here.




class CartView(ListView):
    template_name = 'cart/cart.html'
    model = Shoes
    context_object_name = 'shoes'

    def get_queryset(self):
        cart = Cart.objects.filter(user_id=self.request.user).values_list('shoes', flat=True)
        queryset = Shoes.objects.filter(pk__in=cart)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['cart'] = Cart.objects.filter(user_id=self.request.user)
        return context