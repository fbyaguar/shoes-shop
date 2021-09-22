from django import template
from shoes.models import Shoes, Commentary
import shoes.views as vie
from django.db.models import Count

register = template.Library()

# @register.simple_tag()
# def choise_form(choise):
#     vie.choise_f = choise
#     return choise

def get_shoes_id_list_by_comments():
    """получение списка топ 20 обуви по количеству комментариев"""
    shoes_id_with_max_comments = Commentary.objects.values('shoes').annotate(Count('shoes')).order_by('-shoes__count')[:20]
    shoes_id_list = []
    try:
        for item in shoes_id_with_max_comments:
            shoes_id_list.append(Shoes.objects.get(pk=item['shoes']))
    except Exception:
        return None
    return shoes_id_list


@register.inclusion_tag('shoes/rating.html')
def get_rating(shoes_pk):
    # shoes_rating = Commentary.objects.filter(shoes = shoes_pk).filter(value__gt=0)
    # sum = 0
    # size = len(shoes_rating)
    # if size == 0:
    #     return ({'size': '0','avg_rating': 0 })
    # else:
    #     for item in shoes_rating:
    #         sum += item.value
    # avg_rating = sum / size
    # Shoe = Shoes.objects.get(id = shoes_pk)
    # Shoe.rating = avg_rating

    # Shoe.save()
    # shoes_rating = Commentary.objects.filter(shoes=shoes_pk).filter(value__gt=0)
    # size = len(shoes_rating)
    # if size == 0:
    #     return ({'avg_rating': 0 })
    # else:
    Shoe = Shoes.objects.get(id=shoes_pk)
    avg_rating = Shoe.rating

    return ({'avg_rating': avg_rating })

def get_rating_for_views(shoes_pk):
    shoes_rating = Commentary.objects.filter(shoes = shoes_pk).filter(value__gt=0)
    sum = 0
    size = len(shoes_rating)
    if size == 0:
        return 0
    else:
        for item in shoes_rating:
            sum += item.value
    avg_rating = sum / size
    # Shoe = Shoes.objects.get(id = shoes_pk)
    # Shoe.rating = avg_rating
    # Shoe.save()
    # views.views +=1
    # views.save()
    return avg_rating


@register.inclusion_tag('shoes/rating.html')
def get_single_rating(rating):
    return ({'size': 0,'avg_rating': rating  })


@register.simple_tag()
def get_comment_text(text):
    return text

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