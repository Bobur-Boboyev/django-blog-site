from django.urls import path
from .views import edit_profile, follow_user, profile_view, register_view

urlpatterns = [
    path('register/', register_view, name='register'),
    path('profile/<str:username>/', profile_view, name='profile'),
    path('follow/<str:username>/', follow_user, name='follow'),
    path('profile/<str:username>/edit/', edit_profile, name='edit-profile'),
]