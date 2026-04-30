from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def notifications(request):
    notifications = request.user.notifications.all().order_by("-created_at")

    return render(request, "core/notifications.html", {"notifications": notifications})
