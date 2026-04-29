from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import PostForm
from .models import Post


def blog_list(request):
    query = request.GET.get('q')

    blogs = Post.objects.select_related('author').all().order_by('-created_at')

    if query:
        blogs = blogs.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        )

    return render(request, 'blogs/blog_list.html', {'blogs': blogs, 'query': query})


def blog_detail(request, pk):
    blog = get_object_or_404(Post, pk=pk)
    return render(request, 'blogs/blog_detail.html', {'blog': blog, 'user': request.user, 'comments': blog.comments.all()})


@login_required
def blog_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            return redirect('blog-list')
    else:
        form = PostForm()

    return render(request, 'blogs/blog_form.html', {'form': form})


def blog_edit(request, pk):
    blog = get_object_or_404(Post, pk=pk)

    if blog.author != request.user:
        return HttpResponseForbidden("You cannot edit this blog")

    if request.method == "POST":
        form = PostForm(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('blog-detail', pk=blog.pk)
    else:
        form = PostForm(instance=blog)

    return render(request, 'blogs/blog_form.html', {'form': form})


def blog_delete(request, pk):
    blog = get_object_or_404(Post, pk=pk)

    if blog.author != request.user:
        return HttpResponseForbidden("You cannot delete this blog")

    if request.method == "POST":
        blog.delete()
        return redirect('blog-list')

    return render(request, 'blogs/blog_confirm_delete.html', {'blog': blog})