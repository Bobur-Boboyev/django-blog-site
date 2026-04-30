from django.urls import path
from .views import category_list, blogs_by_category

urlpatterns = [
    path("", category_list, name="category-list"),
    path("<slug:slug>/", blogs_by_category, name="blogs-by-category"),
]
