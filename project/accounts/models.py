"""Models for accounts app"""
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.


class FollowersModel(models.Model):
    """
    Followers model
    """

    follower = models.ForeignKey(
        User, related_name="following", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User, related_name="followers", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.follower}, {self.user}"


class ProfileDataModel(models.Model):
    """
    User Profile model
    """

    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profileimg = models.ImageField(
        upload_to="profile_images", default="blank-profile-picture.png"
    )
    last_updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user}"
