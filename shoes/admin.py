from django.contrib import admin
from .models import Shoes, Category, Size, Season, Brand, Commentary, Country, Material, Rating, Shoes_Images


class ShoesImages(admin.StackedInline):
  model = Shoes_Images
  extra = 5

class ShoesAdmin(admin.ModelAdmin):
  #  list_display =  [field.name for field in Shoes._meta.get_fields()]
    list_display = ['title','price','category','sex','brand','content']
    list_display_links = ('title',)
    list_filter = ('category','sex','brand')
    search_fields = ('title','price')
    readonly_fields = ('views',)
    prepopulated_fields = {'url': ('title',)}
    inlines = [ShoesImages]




# Register your models here.
admin.site.register(Shoes, ShoesAdmin)
admin.site.register(Category)
admin.site.register(Size)
admin.site.register(Season)
admin.site.register(Brand)
admin.site.register(Country)
admin.site.register(Material)
admin.site.register(Commentary)
admin.site.register(Rating)
admin.site.register(Shoes_Images)

