from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_list, name='blog-list'),
    path('<int:pk>/', views.blog_detail, name='blog-detail'),
    path('create/', views.blog_create, name='blog-create'),
    path('<int:pk>/edit/', views.blog_edit, name='blog-edit'),
    path('<int:pk>/delete/', views.blog_delete, name='blog-delete'),
]