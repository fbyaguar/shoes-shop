from django import template
from shoes.models import Shoes, Commentary


register = template.Library()



@register.inclusion_tag('shoes/rating.html')
def get_rating(shoes_pk):
    shoes_rating = Commentary.objects.filter(shoes = shoes_pk).filter(value__gt=0)
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


@register.inclusion_tag('shoes/rating.html')
def get_single_rating(rating):
    return ({'size': 0,'avg_rating': rating  })




@register.inclusion_tag('shoes/rating_detail.html')
def get_rating_detail(shoes_pk):
    shoes_rating = Commentary.objects.filter(shoes = shoes_pk).filter(value__gt=0)
   # shoes_rating = shoes_rating_.filter()
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