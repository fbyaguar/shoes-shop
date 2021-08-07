from django.contrib import admin
from .models import Shoes, Category, Size, Season, Brand, Commentary, Country, Material, Shoes_Images, Answer


class ShoesImages(admin.StackedInline):
    model = Shoes_Images
    extra = 5


class ShoesMaterial(admin.StackedInline):
    model = Material
    extra = 1

class ShoesAdmin(admin.ModelAdmin):
  #  list_display =  [field.name for field in Shoes._meta.get_fields()]
    list_display = ['title','price','rating','category','sex','brand','content']
    list_display_links = ('title',)
    list_filter = ('category','sex','brand',"rating")
    search_fields = ('title','price')
    readonly_fields = ('views',)
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ ShoesImages, ShoesMaterial,]


class CategoryAdmin(admin.ModelAdmin):

    list_display = ['title','url']
    list_display_links = ('title',)
    prepopulated_fields = {'url': ('title',)}


class SizeAdmin(admin.ModelAdmin):
    list_display = ['number', 'url']
    list_display_links = ('number',)
    prepopulated_fields = {'url': ('number',)}

class AnswerAdmin(admin.ModelAdmin):
    list_display = ['user', 'commentary', 'text']
    list_display_links = ('user', 'commentary')
    #prepopulated_fields = {'url': ('number',)}

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
    list_display = ['user', 'text', 'shoes','value']
    list_display_links = ('user',)

    # def has_add_permission(self, request):
    #     return False




# Register your models here.
admin.site.register(Shoes, ShoesAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(Season, SeasonAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Commentary, CommentaryAdmin)
admin.site.register(Answer,AnswerAdmin)

