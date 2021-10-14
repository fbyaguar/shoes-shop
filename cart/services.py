from django.http import JsonResponse
from django.template.loader import render_to_string
from cart.models import Cart
from shoes.models import Shoes
from decimal import Decimal
from django.conf import settings
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


def get_total_sum_session(self,request):
    total_sum = 0
    # cart = SessionCart(self.request)
    # querylist = cart.cart.keys()
    queryset = self.get_queryset()
    for item in queryset:
        total_sum += item.sum_price
    context = {'shoes': queryset, 'total_sum': total_sum}
    html = render_to_string('cart/cart_list.html', context)
    return html


class SessionCart(object):

    def __init__(self, request):
        """
        Инициализируем корзину
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        # print('1')
        # print(self.cart)

    def add(self, product, quantity=1):
        """
        Добавить продукт в корзину или обновить его количество.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price)}
        #if update_quantity:
        self.cart[product_id]['quantity'] = int(quantity)+int(self.cart[product_id]['quantity'])
        #else:
            #self.cart[product_id]['quantity'] += quantity

        self.save()
        # print('2')
        # print(self.cart)

    def save(self):
        # Обновление сессии cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # Отметить сеанс как "измененный", чтобы убедиться, что он сохранен
        self.session.modified = True

    def remove(self, product):
        """
        Удаление товара из корзины.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        Перебор элементов в корзине и получение продуктов из базы данных.
        """
        product_ids = self.cart.keys()
        # получение объектов product и добавление их в корзину
        products = Shoes.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            #item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Подсчет всех товаров в корзине.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        Подсчет стоимости товаров в корзине.
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in
                   self.cart.values())

    def clear(self):
        # удаление корзины из сессии
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True