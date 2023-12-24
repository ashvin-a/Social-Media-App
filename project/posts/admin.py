"""Admin configuration of posts app"""
from django.contrib import admin
from .models import PostModel,CommentModel
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    """
    Configure display of Post model.
    """
    list_display = ('author','created_on')
    list_filter = ('created_on',)

class CommentAdmin(admin.ModelAdmin):
    """
    Configure display of Comment Model.
    """
    list_display = ('author',)

admin.site.register(PostModel,PostAdmin)
admin.site.register(CommentModel,CommentAdmin)
