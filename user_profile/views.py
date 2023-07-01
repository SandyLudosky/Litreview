from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from authentication.models import User


@login_required
def user_profile(request, user):
    user = User.objects.get(username=user)
    context = {
        'requested_user': user,
    }

    return render(
        request,
        'user_profile/index.html',
        context
    )

