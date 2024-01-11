"""Endpoints for Social Media App"""
from django.urls import path
from django.contrib.auth import views as auth_view
from posts import views as post_view
from . import views

urlpatterns = [
    path(
        "password-change/done/",
        auth_view.PasswordResetDoneView.as_view(
            template_name="accounts/reset_password_sent.html"
        ),
        name="password_reset_done",
    ),
    path(
        "password-change/",
        auth_view.PasswordResetView.as_view(
            template_name="accounts/reset_password.html"
        ),
        name="password_reset",
    ),
    path(
        "password-change/<uidb64>/<token>/",
        auth_view.PasswordResetConfirmView.as_view(
            template_name="accounts/reset_password_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-change/complete/",
        auth_view.PasswordResetCompleteView.as_view(
            template_name="accounts/reset_password_done.html"
        ),
        name="password_reset_complete",
    ),
    path(
        "profile/<int:profile_id>/",
        views.ProfileView.as_view(),
        name="profile",
    ),
    path(
        "my-profile/connections/",
        views.ConnectionView.as_view(),
        name="connections",
    ),
    path(
        "<int:post_id>/comment/",
        post_view.CommentView.as_view(),
        name="comment_post",
    ),
    path(
        "<int:post_id>/delete/",
        post_view.DeletePostView.as_view(),
        name="delete_post",
    ),
    path(
        "<int:post_id>/like/",
        post_view.LikePostView.as_view(),
        name="like_post",
    ),
    path("my-profile/", views.EditProfileView.as_view(), name="profile-page"),
    path("search/", views.SearchView.as_view(), name="search"),
    path("", views.PostListView.as_view(), name="homepage"),
    path(
        "<int:user_id>/modify/",
        views.DeactivateUser.as_view(),
        name="deactivate",
    ),
    path("admin-profile/", views.AdminView.as_view(), name="admin"),
    path("view-users/", views.ViewUsers.as_view(), name="all-users"),
    path("view-posts/", views.ViewPosts.as_view(), name="all-posts"),
    path("signup/", views.RegisterUser.as_view(), name="signup-page"),
    path("login/", views.LoginUser.as_view(), name="login-page"),
    path("logout/", views.Logout.as_view(), name="logout"),
]
