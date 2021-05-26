from django.contrib import admin
from .models import *


class ShoesAdmin(admin.ModelAdmin):
  #  list_display =  [field.name for field in Shoes._meta.get_fields()]
    list_display = ['title','price','category','sex','brand','photo','content']
    list_display_links = ('title',)
    list_filter = ('category','sex','brand')
    search_fields = ('title','price')
    readonly_fields = ('views',)


# Register your models here.
admin.site.register(Shoes, ShoesAdmin)
admin.site.register(Category)
admin.site.register(Size)
admin.site.register(Season)
admin.site.register(Brand)
admin.site.register(Country)
admin.site.register(Material)
admin.site.register(Users)
admin.site.register(Commentary)
admin.site.register(Rating)
admin.site.register(Favorites)
admin.site.register(Cart)
admin.site.register(Order)
