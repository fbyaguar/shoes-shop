from django.urls import path

from shoes.views import *

urlpatterns = [
    path('', Home, name = 'home'),
]