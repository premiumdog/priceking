from django.contrib import admin
from . models import Article, Category, Tags

# Register your models here.

class SlugAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'category', 'date')
    prepopulated_fields = {'slug': ('title',)}

class TagsAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')



admin.site.register(Article, SlugAdmin)
admin.site.register(Category)
admin.site.register(Tags, TagsAdmin)
