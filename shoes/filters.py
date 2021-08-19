import django_filters
from django import forms

from shoes.models import Shoes, Category, Season, Brand


class ShoesFilter(django_filters.FilterSet):

    CHOICE_SEX = ((0, 'для девочки'),(1, 'для мальчика'))

    price = django_filters.filters.RangeFilter()
    category = django_filters.filters.ModelMultipleChoiceFilter(queryset=Category.objects.all(), widget=forms.CheckboxSelectMultiple(attrs={"checked":""}) )
    #sex = django_filters.filters.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=CHOICE_SEX,)
    sex = django_filters.filters.ChoiceFilter(choices=CHOICE_SEX)
    season = django_filters.filters.ModelMultipleChoiceFilter(queryset=Season.objects.all(), widget=forms.CheckboxSelectMultiple(attrs={"checked":""}))
    brand = django_filters.filters.ModelMultipleChoiceFilter(queryset=Brand.objects.all(),
                                                              widget=forms.CheckboxSelectMultiple(attrs={"checked":""}))
    class Meta:
        model = Shoes
        fields = ('price', 'category', 'sex', 'season', 'brand')