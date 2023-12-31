"""Views of posts app"""
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import View
from django.http import HttpRequest, JsonResponse
from .models import PostModel
from .forms import CommentForm


class DeletePostView(View):
    """
    This view manages the deletion of posts
    """

    def post(self, request: HttpRequest, post_id: int):
        """
        Deletes the post and redirects
        """
        post = get_object_or_404(PostModel, id=post_id)
        post.delete()
        if request.user.is_staff:
            return redirect("all-posts")
        return redirect("homepage")


class LikePostView(View):
    """
    This view manages the like button
    """

    def post(self, request: HttpRequest, post_id: int):
        """
        Adds the like to a post.
        """
        post = get_object_or_404(PostModel, id=post_id)
        if post.likes.filter(id=request.user.id):
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        data = {
            "likes": post.count_likes(),
        }
        return JsonResponse(data, safe=False)


class CommentView(View):
    """
    This view manages the comment section.
    """

    def post(self, request: HttpRequest, post_id: int):
        """
        Adds comment to the post.
        """
        user = request.user
        post = get_object_or_404(PostModel, id=post_id)
        comment = CommentForm(request.POST)
        if comment.is_valid():
            new = comment.save(commit=False)
            new.post, new.author = post, user
            new.save()
            return redirect("homepage")
        return redirect("homepage")
