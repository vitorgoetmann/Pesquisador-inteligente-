from django.contrib import admin
from .models import SearchQuery, Article, Summary

@admin.register(SearchQuery)
class SearchQueryAdmin(admin.ModelAdmin):
    list_display = ("termo","created_at")

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title","url","query","fetched_at")

@admin.register(Summary)
class SummaryAdmin(admin.ModelAdmin):
    list_display = ("article","method","created_at")
