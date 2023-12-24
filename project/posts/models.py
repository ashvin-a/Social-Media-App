"""Models of posts app"""
from django.db import models
from django.utils import timezone
from django.db.models.query import QuerySet
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

# Create your models here.
class BaseModel(models.Model):
    """
    Configure delete function.
    """
    deleted = models.BooleanField(default=False)

    class Meta:
        """
        Configure BaseModel.
        """
        abstract = True

    def delete(self):
        """
        Override delete function
        """
        self.deleted = True
        self.save()


class BaseModelManager(models.Manager):
    """
    Model manager for objects.
    """
    def get_queryset(self)-> QuerySet[User]:
        """
        Overrides get_queryset function.
        """
        return super().get_queryset().filter(deleted=False)


class PostModel(BaseModel):
    """
    The post model.
    """
    body = RichTextField()
    image = models.ImageField(upload_to='post_images',blank=True,null=True)   
    created_on = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    likes = models.ManyToManyField(User,related_name='likes',blank=True)
    objects = BaseModelManager()

    def count_likes(self):
        """
        Counts the number of likes in a post
        """
        return self.likes.count()

class CommentModel(models.Model):
    """
    The comment model.
    """
    post = models.ForeignKey(PostModel,related_name='comments',on_delete=models.CASCADE)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    body = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)
