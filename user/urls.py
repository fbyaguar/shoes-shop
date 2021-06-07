from django.urls import path
from user.views import user_logout, user_login, registration, Wishlist

urlpatterns = [
    path('login/',user_login, name ='login'),
    path('logout/',user_logout, name ='logout'),
    path('registration/', registration, name='registration'),
    path('wishlist/', Wishlist.as_view(), name='wishlist'),
    #path('contact/', user_mail, name='contact'),
    ]