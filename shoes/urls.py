from django.urls import path

from shoes.views import Home, review, Shop

#app_name = 'shoes'

urlpatterns = [
    path('', Home.as_view(), name = 'home'),
    path('shoes/<slug:slug>/', review, name= 'ShoesDetailview'),
    #path('shoes/rating', rating , name= 'rating')
    path('shop', Shop.as_view(), name= 'shop')
]