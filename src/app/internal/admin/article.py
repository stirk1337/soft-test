from django.contrib import admin

from app.internal.models.article import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    pass
