import numpy as np

from django.shortcuts import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


from posts.models import Ticket, Review


# Create your views here.
@login_required(login_url='login/')
def feed(request):
    template_name = 'posts/index.html'
    if not request.user.is_authenticated:
        return HttpResponseRedirect('login') # or http response
    else:
        tickets = []
        reviews = []
        items = np.concatenate((tickets, reviews))
        items_sorted = sorted(items, key=lambda item: item.time_created, reverse=True)

        context = {
            'tickets': tickets,
            'reviews': reviews,
            'items': items_sorted
        }
        return render(
            request,
            template_name,
            context
        )
