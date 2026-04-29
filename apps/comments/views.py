from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from apps.blogs.models import Post
from .models import Comment
from .forms import CommentForm
from apps.core.models import Notification


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

            if post.author != request.user:
                Notification.objects.create(
                    sender=request.user,
                    receiver=post.author,
                    message=f"{request.user.username} commented on your post '{post.title}'"
                )

    return redirect('blog-detail', pk=post.id)


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)


    if comment.author != request.user:
        return HttpResponseForbidden("You cannot delete this comment")

    blog_id = comment.post.id
    comment.delete()

    return redirect('blog-detail', pk=blog_id)