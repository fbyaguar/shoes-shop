from django import template
TOTAL_PRICE = 0


register = template.Library()

# @register.simple_tag()
# def sum(price, amount):
#     global TOTAL_PRICE
#     TOTAL_PRICE += price * amount
#     return price * amount
#
# @register.simple_tag()
# def total_price():
#     return TOTAL_PRICE