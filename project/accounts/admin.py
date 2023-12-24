"""Admin configuration for accounts model"""
from django.contrib import admin
from .models import FollowersModel, ProfileDataModel
# Register your models here.


class ProfileDataAdmin(admin.ModelAdmin):
    """Admin configuration for ProfileDataModel"""
    list_display = ('first_name', 'last_name',)


class FollowersAdmin(admin.ModelAdmin):
    """Admin configuration for FollowersModel"""
    list_display = ('follower', 'user')


admin.site.register(FollowersModel, FollowersAdmin)
admin.site.register(ProfileDataModel, ProfileDataAdmin)
