from django import template
from shoes.models import Shoes, Rating


register = template.Library()



@register.inclusion_tag('shoes/rating.html')
def get_rating(shoes_pk):
    shoes_rating = Rating.objects.filter(shoes = shoes_pk)
    sum = 0
    size = len(shoes_rating)
    if size == 0:
        return ({'size': '','avg_rating': 0 })
    else:
        for item in shoes_rating:
            sum += item.value
    avg_rating = sum / size
    # views.views +=1
    # views.save()
    return ({'size': size,'avg_rating': avg_rating })


@register.inclusion_tag('shoes/rating_detail.html')
def get_rating_detail(shoes_pk):
    shoes_rating = Rating.objects.filter(shoes = shoes_pk)
    sum = 0
    size = len(shoes_rating)
    if size == 0:
        return ({'size': '0','avg_rating': 0 })
    else:
        for item in shoes_rating:
            sum += item.value
    avg_rating = sum / size
    # views.views +=1
    # views.save()
    return ({'size': size,'avg_rating': avg_rating })