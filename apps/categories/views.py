from django.shortcuts import render
from .models import Category
from apps.blogs.models import Post


def category_list(request):
    categories = Category.objects.all()
    return render(request, 'categories/category_list.html', {
        'categories': categories
    })

def blogs_by_category(request, slug):
    blogs = Post.objects.filter(category__slug=slug).order_by('-created_at')
    return render(request, 'blogs/blog_list.html', {'blogs': blogs})