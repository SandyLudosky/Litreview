import numpy as np

from django.shortcuts import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from subscriptions.models import UserFollows
from posts.models import Ticket, Review


def get_users(request):
    """We collect all the users to whom the user is subscribed"""
    users = []
    users_follows = UserFollows.objects.filter(user=request.user)
    for user in users_follows:
        users.append(user.followed_user)
    return users


def get_tickets(request, users):
    """we collect all the tickets of the users to whom we are subscribed"""
    tickets = []
    for user in users:
        tickets_by_user = Ticket.objects.filter(user=user)
        for ticket in tickets_by_user:
            tickets.append(ticket)
    tickets = sorted(tickets, key=lambda k: k.time_created, reverse=True)
    return tickets


def get_reviews(request, users):
    """we collect all the reveiws of the users to whom we are subscribed"""
    reviews = []
    for user in users:
        review_by_user = Review.objects.filter(user=user).order_by('-time_created')
        for review in review_by_user:
            reviews.append(review)
    reviews = sorted(reviews, key=lambda k: k.time_created, reverse=True)
    return reviews


def sorted_posts(request, tickets, reviews):
    posts = []
    for ticket in tickets:
        posts.append(ticket)
    for review in reviews:
        posts.append(review)
    posts = sorted(posts, key=lambda k: k.time_created, reverse=True)
    return posts

# Create your views here.
@login_required(login_url='login/')
def feed(request):
    template_name = 'feed/index.html'
    if not request.user.is_authenticated:
        return HttpResponseRedirect('login') # or http response
    else:
        users = get_users(request)
        tickets = get_tickets(request, users)
        reviews = get_reviews(request, users)
        items = np.concatenate((tickets, reviews))
        items_sorted = sorted(items, key=lambda item: item.time_created, reverse=True)
        print(reviews)
        context = {'tickets': tickets, 'reviews': reviews, 'items': items_sorted}
        return render(
            request,
            template_name,
            context
        )
