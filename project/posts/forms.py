"""Forms configuration of posts app"""
from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import PostModel, CommentModel


class PostForm(forms.ModelForm):
    """
    Form for receiving post detail.
    """

    body = forms.CharField(label="", widget=CKEditorWidget())
    image = forms.ImageField(
        label="",
        required=False,
        widget=forms.FileInput(attrs={"class": "form-control"}),
    )

    class Meta:
        """
        Configure the behaviour of PostForm
        """

        model = PostModel
        fields = ["body", "image"]
        exclude = ("likes",)


class CommentForm(forms.ModelForm):
    """
    Form for receiving comments.
    """

    body = forms.CharField(
        label="",
        widget=forms.Textarea(attrs={"rows": 4, "class": "form-control"}),
    )

    class Meta:
        """
        Configure the behaviour of CommentForm
        """

        model = CommentModel
        fields = ["body"]
