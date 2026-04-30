from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib.auth import login

from apps.core.models import Notification
from apps.users.models import Profile
from .forms import ProfileForm, RegisterForm


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = Profile.objects.create(user=user)
            user.profile = profile
            login(request, user)
            return redirect("blog-list")
    else:
        form = RegisterForm()

    return render(request, "users/register.html", {"form": form})


def profile_view(request, username):
    User = get_user_model()
    user = get_object_or_404(User, username=username)

    return render(
        request,
        "users/profile.html",
        {"profile_user": user, "current_user": request.user},
    )


@login_required
def follow_user(request, username):
    if request.user.username == username:
        return redirect("profile", username=username)

    User = get_user_model()
    target_user = get_object_or_404(User, username=username)

    profile = target_user.profile

    if request.user in profile.followers.all():
        profile.followers.remove(request.user)

        notification = Notification.objects.filter(
            sender=request.user, receiver=target_user
        ).first()

        if notification:
            notification.delete()
    else:
        profile.followers.add(request.user)

        Notification.objects.create(
            sender=request.user,
            receiver=target_user,
            message=f"{request.user.username} followed you",
        )

    return redirect("profile", username=username)


@login_required
def edit_profile(request, username):
    User = get_user_model()
    user = get_object_or_404(User, username=username)
    profile = user.profile

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
    else:
        form = ProfileForm(instance=profile)

    return render(request, "users/edit_profile.html", {"form": form})
