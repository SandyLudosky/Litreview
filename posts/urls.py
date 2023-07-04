from . import views
from django.urls import path
from .views import posts, create_ticket, create_review, create_ticket_and_review, edit_ticket, edit_review

app_name = "posts"
urlpatterns = [
    path('', posts, name='home'),
    path('create-ticket/', create_ticket, name='create_ticket'),
    path('create-review/', create_ticket_and_review, name='create_ticket_and_review'),
    path('create-review/<int:ticket_id>/', create_review, name='create_review'),
    path('edit-ticket/<int:ticket_id>/', edit_ticket, name='edit_ticket'),
    path('edit-ticket/<int:ticket_id>/', edit_ticket, name='delete_ticket'),
    path('edit-review/<int:review_id>/', edit_review, name='edit_review'),
    path('delete-review/<int:review_id>/', edit_review, name='delete_review'),
]