from . import views
from django.urls import path
from .views import follow, unfollow

urlpatterns = [
       path('follows/', follow, name='follows'),
       path('unfollow/<int:link_id>/', unfollow, name='unfollow'),
]