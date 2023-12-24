"""Endpoints for Social Media App"""
from django.urls import path
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_view
from posts import views as post_view
from . import views
from .decorators import allowed_users

urlpatterns = [
    path('password-change/done/', auth_view.PasswordResetDoneView.as_view(
                                template_name="accounts/reset_password_sent.html"),
                                name="password_reset_done"),
    path('password-change/', auth_view.PasswordResetView.as_view(
                                template_name="accounts/reset_password.html"),
                                name="password_reset"),
    path('password-change/<uidb64>/<token>/', auth_view.
                                PasswordResetConfirmView.as_view(
                                template_name="accounts/reset_password_confirm.html"),
                                name="password_reset_confirm"),
    path('password-change/complete/', auth_view.
                                PasswordResetCompleteView.as_view(
                                template_name="accounts/reset_password_done.html"),
                                name="password_reset_complete"),
    path('profile/<int:profile_id>/', login_required(views.ProfileView.as_view(),
                                login_url='login-page'), name='profile'),
    path('my-profile/connections/', login_required(views.ConnectionView.as_view(),
                                login_url='login-page'), name='connections'),
    path('<int:post_id>/comment/',login_required(post_view.CommentView.as_view(),
                                login_url='login-page'), name='comment_post'),
    path('<int:post_id>/delete/', login_required(post_view.DeletePostView.as_view(),
                                login_url='login-page'), name='delete_post'),
    path('<int:post_id>/like/',login_required(post_view.LikePostView.as_view(),
                                login_url='login-page'), name='like_post'),
    path('<int:post_id>/profile-like/',login_required(post_view.LikeProfilePostView
                     .as_view(),login_url='login-page'), name='profile_like_post'),
    path('my-profile/', login_required(views.EditProfileView.as_view(),
                                login_url='login-page'), name='profile-page'),
    path('search/',login_required(views.SearchView.as_view(),
                                login_url='login-page'), name='search'),
    path('',login_required(views.PostListView.as_view(),
                                login_url='login-page'), name='homepage'),
    path('<int:user_id>/modify/',login_required(allowed_users(
                                allowed_roles=['admin'])(views.DeactivateUser.as_view()),
                                login_url='login-page'), name='deactivate'),
    path('admin-profile/',login_required(allowed_users(
                                allowed_roles=['admin'])(views.AdminView.as_view()),
                                login_url='login-page'), name='admin'),
    path('view-users/',login_required(allowed_users(
                                allowed_roles=['admin'])(views.ViewUsers.as_view()),
                                login_url='login-page'),name='all-users'),
    path('view-posts/',login_required(allowed_users(
                                allowed_roles=['admin'])(views.ViewPosts.as_view()),
                                login_url='login-page'),name='all-posts'),
    path('signup/', views.RegisterUser.as_view(), name='signup-page'),
    path('login/', views.LoginUser.as_view(), name='login-page'),
    path('logout/', views.Logout.as_view(), name='logout'),
]
