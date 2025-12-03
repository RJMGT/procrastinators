from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('create-post/', views.create_post_view, name='create_post'),
    path('leaderboard/', views.leaderboard_view, name='leaderboard'),
    path('user-leaderboard/', views.user_leaderboard_view, name='user_leaderboard'),
    path('like-post/<int:post_id>/', views.like_post_view, name='like_post'),
    path('dislike-post/<int:post_id>/', views.dislike_post_view, name='dislike_post'),
    path('check-new-posts/', views.check_new_posts_view, name='check_new_posts'),
    path('d92e206/', views.abtest_view, name='abtest'),
    path('d92e206/track-click/', views.abtest_button_click_view, name='abtest_button_click'),
]

