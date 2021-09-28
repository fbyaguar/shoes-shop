from django.contrib import admin
from .models import Wishlist

# Register your models here.


class WishllistAdmin(admin.ModelAdmin):
    list_display = ('user_id','shoes_id')
    list_display_links = ('user_id','shoes_id')
    list_filter = ('user_id','shoes_id')
    search_fields = ('user_id','shoes_id')


admin.site.register(Wishlist, WishllistAdmin)