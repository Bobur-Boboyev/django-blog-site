from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q

from .forms import PostForm
from .models import Post
from apps.core.models import Notification


def blog_list(request):
    query = request.GET.get("q")
    page_number = request.GET.get("page")

    blogs = Post.objects.select_related("author").all().order_by("-created_at")

    if query:
        blogs = blogs.filter(Q(title__icontains=query) | Q(content__icontains=query))

    paginator = Paginator(blogs, 5)
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "blogs/blog_list.html",
        {"blogs": page_obj, "query": query, "page_obj": page_obj},
    )


def blog_detail(request, pk):
    blog = get_object_or_404(Post, pk=pk)
    return render(
        request,
        "blogs/blog_detail.html",
        {
            "blog": blog,
            "user": request.user,
            "comments": blog.comments.all(),
            "request": request,
        },
    )


@login_required
def blog_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            return redirect("blog-list")
    else:
        form = PostForm()

    return render(request, "blogs/blog_form.html", {"form": form})


def blog_edit(request, pk):
    blog = get_object_or_404(Post, pk=pk)

    if blog.author != request.user:
        return HttpResponseForbidden("You cannot edit this blog")

    if request.method == "POST":
        form = PostForm(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            return redirect("blog-detail", pk=blog.pk)
    else:
        form = PostForm(instance=blog)

    return render(request, "blogs/blog_form.html", {"form": form})


def blog_delete(request, pk):
    blog = get_object_or_404(Post, pk=pk)

    if blog.author != request.user:
        return HttpResponseForbidden("You cannot delete this blog")

    if request.method == "POST":
        blog.delete()
        return redirect("blog-list")

    return render(request, "blogs/blog_confirm_delete.html", {"blog": blog})


def feed(request):
    user = request.user

    if not user.is_authenticated:
        return redirect("blog-list")
    else:
        following_users = user.profile.followers.all()

        blogs = Post.objects.filter(author__in=following_users).order_by("-id")

    return render(request, "blogs/feed.html", {"blogs": blogs})


@login_required
def like_blog(request, blog_id):
    blog = get_object_or_404(Post, id=blog_id)

    if request.user in blog.likes.all():
        blog.likes.remove(request.user)
    else:
        blog.likes.add(request.user)

    if blog.author != request.user:
        Notification.objects.create(
            sender=request.user,
            receiver=blog.author,
            message=f"{request.user.username} liked your blog: {blog.title}",
        )

    return redirect(request.META.get("HTTP_REFERER", "feed"))


@login_required
def liked_blogs(request):
    blogs = Post.objects.filter(likes=request.user).order_by("-id")

    return render(request, "blogs/liked_blogs.html", {"blogs": blogs})
