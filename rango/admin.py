from django.contrib import admin
from rango.models import Category, Page

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    fields = ['name',]
    list_display = ('name',)
    list_filter = ['views']
    prepopulate_fields = {'slug':('name',)}


class PageAdmin(admin.ModelAdmin):
    fields = ['title', 'category', 'url',]
    list_display = ('title', 'category', 'url',)
    list_filter = ['category']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)
