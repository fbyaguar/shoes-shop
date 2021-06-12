from django.urls import path

from shoes.views import Home, ShoesDetailview

#app_name = 'shoes'

urlpatterns = [
    path('', Home.as_view(), name = 'home'),
    path('<slug:slug>/',ShoesDetailview.as_view(), name= 'ShoesDetailview')
]