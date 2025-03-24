from django.contrib import admin
from .models import Post, Comment, BloggerProfile

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    search_fields = ('title', 'content')
    list_filter = ('created_at', 'author')
    ordering = ('-created_at',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_at')
    search_fields = ('content',)
    list_filter = ('created_at', 'author')
    ordering = ('-created_at',)


@admin.register(BloggerProfile)
class BloggerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')
    search_fields = ('user__username', 'bio')
    list_filter = ('user',)
