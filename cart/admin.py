from django.contrib import admin
from  cart.models import Cart

class CartAdmin(admin.ModelAdmin):
    list_display = ['shoes','number','user_id']
    list_display_links = ('shoes',)
    list_filter = ('shoes','user_id')
    search_fields = ('shoes','user_id')
    readonly_fields = ('number',)

# Register your models here.
admin.site.register(Cart, CartAdmin)




