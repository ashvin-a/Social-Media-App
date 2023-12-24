"""App configuration of posts app"""
from django.apps import AppConfig


class PostsConfig(AppConfig):
    """
    Post app configuration.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'posts'
