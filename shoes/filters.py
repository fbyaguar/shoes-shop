import django_filters
from django import forms

from shoes.models import Shoes, Category, Season, Brand


class ShoesFilter(django_filters.FilterSet):
    #CHOICE_SEX = ((0, 'для девочки'),(1, 'для мальчика'))
    price = django_filters.filters.RangeFilter()
    category = django_filters.filters.ModelMultipleChoiceFilter(queryset=Category.objects.all(), widget=forms.CheckboxSelectMultiple() )
    #sex = django_filters.filters.MultipleChoiceFilter( choices=Shoes.CHOICES, widget=forms.CheckboxSelectMultiple(attrs={"checked":""}) )

    season = django_filters.filters.ModelMultipleChoiceFilter(queryset=Season.objects.all(), widget=forms.CheckboxSelectMultiple())
    brand = django_filters.filters.ModelMultipleChoiceFilter(queryset=Brand.objects.all(),
                                                              widget=forms.CheckboxSelectMultiple())
    class Meta:
        model = Shoes
        fields = ('price', 'category', 'season', 'brand')