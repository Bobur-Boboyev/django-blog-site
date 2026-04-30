from django.urls import path
from .views import add_comment, delete_comment

urlpatterns = [
    path("add/<int:post_id>/", add_comment, name="add-comment"),
    path("delete/<int:comment_id>/", delete_comment, name="delete-comment"),
]
