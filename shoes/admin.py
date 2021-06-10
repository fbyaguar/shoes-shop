from django.contrib import admin
from .models import Shoes, Category, Size, Season, Brand, Commentary, Country, Material, Rating, Shoes_Images


class ShoesImages(admin.StackedInline):
    model = Shoes_Images
    extra = 5


class ShoesMaterial(admin.StackedInline):
    model = Material
    extra = 1

class ShoesAdmin(admin.ModelAdmin):
  #  list_display =  [field.name for field in Shoes._meta.get_fields()]
    list_display = ['title','price','category','sex','brand','content']
    list_display_links = ('title',)
    list_filter = ('category','sex','brand')
    search_fields = ('title','price')
    readonly_fields = ('views',)
    prepopulated_fields = {'url': ('title',)}
    inlines = [ ShoesImages, ShoesMaterial,]


class CategoryAdmin(admin.ModelAdmin):

    list_display = ['title','url']
    list_display_links = ('title',)
    prepopulated_fields = {'url': ('title',)}


class SizeAdmin(admin.ModelAdmin):
    list_display = ['number', 'url']
    list_display_links = ('number',)
    prepopulated_fields = {'url': ('number',)}


class SeasonAdmin(admin.ModelAdmin):
    list_display = ['title', 'url']
    list_display_links = ('title',)
    prepopulated_fields = {'url': ('title',)}


class BrandAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'logo', 'content']
    list_display_links =  ('title',)
    prepopulated_fields = {'url': ('title',)}

class CountryAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'flag']
    list_display_links = ('title',)
    prepopulated_fields = {'url': ('title',)}


class CommentaryAdmin(admin.ModelAdmin):
    list_display = ['shoes', 'user_id', 'parent', 'title', 'text']
    list_display_links = ('title',)


class RatingAdmin(admin.ModelAdmin):
  list_display = ['shoes', 'user_id', 'value']
  list_display_links = ('shoes',)
# class MaterialAdmin(admin.ModelAdmin):
#   list_display = ['top', 'sole', 'strap', 'lining']
#   list_display_links = ('title',)
#   prepopulated_fields = {'url': ('title',)}

# Register your models here.
admin.site.register(Shoes, ShoesAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(Season, SeasonAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Commentary, CommentaryAdmin)
admin.site.register(Rating, RatingAdmin )
#admin.site.register(Shoes_Images)
#admin.site.register(Material)
