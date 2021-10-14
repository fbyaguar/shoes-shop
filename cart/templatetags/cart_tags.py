from django import template
TOTAL_PRICE = 0


register = template.Library()

# @register.simple_tag()
# def sum(price, amount):
#     global TOTAL_PRICE
#     TOTAL_PRICE += price * amount
#     return price * amount
#
@register.simple_tag()
def select_number(quantity):
    print(quantity)
    for item in quantity:
        print('1')
        print(item)
        yield item


# @register.filter
# def sel_num(numlist, num):
#         return numlist[num-1]