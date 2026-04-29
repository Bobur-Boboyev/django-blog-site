from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from apps.blogs.models import Post
from .models import Comment
from .forms import CommentForm


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()

    return redirect('blog-detail', pk=post.id)