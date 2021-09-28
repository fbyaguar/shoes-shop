from django.urls import path

from shoes.views import  review, ShopView, SearchView, HomeView


urlpatterns = [
    path('', HomeView.as_view(), name = 'home'),
    path('shoes/<slug:slug>/', review, name= 'review'),
    path('shop/', ShopView.as_view(), name= 'shop'),
    path('search/', SearchView.as_view(), name='search')
]