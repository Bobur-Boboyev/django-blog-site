from django.urls import path
from .views import add_comment

urlpatterns = [
    path('add/<int:post_id>/', add_comment, name='add-comment'),
]