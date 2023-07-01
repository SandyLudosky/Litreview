from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from . import forms
from authentication import models as authentication
from . import models


@login_required
def follow(request):
    form = forms.UserFollowsForm()
    followers = models.UserFollows.objects.filter(followed_user=request.user)
    follows = models.UserFollows.objects.filter(user=request.user)
    error = None
    if request.method == 'POST':
        form = forms.UserFollowsForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            print(username != f'{request.user.username}')
            print(request.user.username)
            if username != f'{request.user.username}':
                try:
                    user = authentication.User.objects.get(id=request.user.id)
                    print(user)
                    followed_user = authentication.User.objects.filter(username=username)[0]
                    print(followed_user)
                    if followed_user is not None:
                        add_follower = models.UserFollows(user=user, followed_user=followed_user)
                        add_follower.save()
                    else:
                        return redirect('follows')
                except Exception:
                    form = forms.UserFollowsForm()
                    error = "Désolé ce compte utilisateur n'existe pas"
            else:
                error = 'Désolé vous ne pouvez pas vous auto-abonné'
    context = {'form': form, 'followers': followers,
               'follows': follows, 'page_name': 'Abonnements', 'error': error}
    return render(request, 'subscriptions/index.html', context=context)


@login_required
def unfollow(request, link_id):
    link = models.UserFollows.objects.get(id=link_id)
    link.delete()
    return redirect('follows')