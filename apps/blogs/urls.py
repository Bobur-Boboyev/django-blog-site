from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_list, name='blog-list'),
    path('<int:pk>/', views.blog_detail, name='blog-detail'),
    path('create/', views.blog_create, name='blog-create'),
    path('<int:pk>/edit/', views.blog_edit, name='blog-edit'),
    path('<int:pk>/delete/', views.blog_delete, name='blog-delete'),
    path('feed/', views.feed, name='feed'),
    path('like/<int:blog_id>/', views.like_blog, name='like-blog'),
    path('liked/', views.liked_blogs, name='liked-blogs'),
]