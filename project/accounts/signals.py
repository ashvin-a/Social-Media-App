"""Signals for superuser creation"""
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def add_superuser_to_admin(instance: User, created: bool, **kwargs):
    """
    Add super user to admin group during creation
    """
    if created and instance.is_superuser:
        admin = Group.objects.get(name="admin")
        instance.groups.add(admin)
