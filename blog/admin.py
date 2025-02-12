from django.contrib import admin
from .models import News, NewsUser, NewsTag, Article

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'slug')
    search_fields = ('title', 'slug')

@admin.register(NewsUser)
class NewsUserAdmin(admin.ModelAdmin):
    list_display = ('role',)
    
@admin.register(NewsTag)
class NewsTagAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_published')
    search_fields = ('title', 'slug')
