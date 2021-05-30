from django.urls import path

from shoes.views import *

urlpatterns = [
    path('', Home.as_view(), name = 'home'),
    path('<int:pk>/',ShoesDetailview.as_view(), name= 'ShoesDetailview')
]