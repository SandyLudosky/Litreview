
import numpy as np

from django.shortcuts import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Ticket, Review
from . import forms


# Create your views here.
@login_required(login_url='login/')
def posts(request):
    template_name = 'posts/index.html'
    all_tickets = []
    if not request.user.is_authenticated:
        return HttpResponseRedirect('login') # or http response
    else:
        tickets = Ticket.objects.filter(user=request.user)
        for ticket in tickets:
            reviews = ticket.reviews.all()
            all_tickets.append({"ticket": ticket, "reviews": list(reviews)})

        context = {
            'tickets': all_tickets,
        }
        print(all_tickets)
        return render(
            request,
            template_name,
            context
        )


@login_required(login_url='login/')
def create_ticket(request):
    form = forms.TicketForm()
    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            if form.cleaned_data['image']:
                ticket.image = form.cleaned_data['image']
            ticket.save()
            return redirect('posts:home')
    context = {
        'form': form
    }
    return render(
        request,
        'posts/create_ticket.html',
        context
    )


@login_required(login_url='login/')
def create_review(request, ticket_id):
    form = forms.ReviewForm()
    if request.method == 'POST':
        form = forms.ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.ticket = get_object_or_404(Ticket, id=ticket_id)
            review.ticket.has_review = True
            review.ticket.save()
            review.save()
            return redirect('posts:home')
    context = {
        'both': False,
        'form': form,
        'ticket': get_object_or_404(Ticket, id=ticket_id)
    }
    return render(
        request,
        'posts/create_review.html',
        context
    )


def create_ticket_and_review(request):
    ticket_form = forms.TicketForm()
    review_form = forms.ReviewForm()
    if request.method == 'POST':
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        review_form = forms.ReviewForm(request.POST)
        if all([ticket_form.is_valid(), review_form.is_valid()]):
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            if ticket_form.cleaned_data['image']:
                ticket.image = ticket_form.cleaned_data['image']
            ticket.has_review = True
            ticket.save()
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = get_object_or_404(Ticket, id=ticket.id)
            review.save()
            return redirect('posts:home')
    context = {
        'both': True,
        'ticket_form': ticket_form,
        'review_form': review_form,
    }
    return render(
        request,
        'posts/create_review.html',
        context
    )


@login_required(login_url='login/')
def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    edit_form = forms.TicketForm(instance=ticket)
    delete_form = forms.TicketFormDelete()
    if request.method == 'POST':
        if 'edit_ticket' in request.POST:
            edit_form = forms.TicketForm(request.POST, instance=ticket)
            if edit_form.is_valid():
                edit_form.save()
                return redirect('posts:home')
        if 'delete_ticket' in request.POST:
            delete_form = forms.TicketFormDelete(request.POST)
            if delete_form.is_valid():
                ticket.delete()
                return redirect('posts:home')
    context = {
        'edit_form': edit_form,
        'delete_form': delete_form
    }
    return render(
        request,
        'posts/edit_ticket.html',
        context
    )


@login_required(login_url='login/')
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    edit_form = forms.ReviewForm(instance=review)
    delete_form = forms.ReviewFormDelete()
    if request.method == 'POST':
        if 'edit_review' in request.POST:
            edit_form = forms.ReviewForm(request.POST, instance=review)
            if edit_form.is_valid():
                edit_form.save()
                return redirect('posts:home')
        if 'delete_review' in request.POST:
            delete_form = forms.ReviewFormDelete(request.POST)
            if delete_form.is_valid():
                review.delete()
                return redirect('posts:home')
    context = {
        'edit_form': edit_form,
        'delete_form': delete_form
    }
    return render(
        request,
        'posts/edit_review.html',
        context
    )

