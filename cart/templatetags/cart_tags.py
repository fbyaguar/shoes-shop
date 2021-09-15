from django import template

register = template.Library()

@register.simple_tag()
def sum(price, amount):
    return price * amount
