from django.urls import path

from shoes.views import Home, ShoesDetailview, rating

#app_name = 'shoes'

urlpatterns = [
    path('', Home.as_view(), name = 'home'),
    path('shoes/<slug:slug>/',ShoesDetailview.as_view(), name= 'ShoesDetailview'),
    path('shoes/rating', rating , name= 'rating')

]