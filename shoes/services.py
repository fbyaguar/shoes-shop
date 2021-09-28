from shoes.models import Shoes, Commentary
from django.db.models import Count


def get_rating_for_views(shoes_pk):
    '''получение рейтинга товара'''
    shoes_rating = Commentary.objects.filter(shoes = shoes_pk).filter(value__gt=0)
    sum = 0
    size = len(shoes_rating)
    if size == 0:
        return 0
    else:
        for item in shoes_rating:
            sum += item.value
    avg_rating = sum / size
    return avg_rating


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