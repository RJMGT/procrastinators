from django.contrib import admin
from .models import Post, Like, Dislike


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'hours_procrastinated', 'created_at', 'get_like_count', 'get_dislike_count']
    list_filter = ['created_at', 'author']
    search_fields = ['title', 'description', 'author__username']
    readonly_fields = ['created_at']
    
    def get_like_count(self, obj):
        return obj.get_like_count()
    get_like_count.short_description = 'Likes'
    
    def get_dislike_count(self, obj):
        return obj.get_dislike_count()
    get_dislike_count.short_description = 'Dislikes'


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'post__title']


@admin.register(Dislike)
class DislikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'post__title']

