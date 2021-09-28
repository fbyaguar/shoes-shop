from django.urls import path
from user.services import user_logout, user_login, registration
from user.views import WishlistView


urlpatterns = [
    path('login/',user_login, name ='login'),
    path('logout/',user_logout, name ='logout'),
    path('registration/', registration, name='registration'),
    path('wishlist/', WishlistView.as_view(), name='wishlist'),
    ]