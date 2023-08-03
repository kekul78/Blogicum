from django.contrib import admin

from .models import Category, Location, Post, Comment


@admin.register(Category, Location, Post, Comment)
class BlogAdmin(admin.ModelAdmin):
    pass
