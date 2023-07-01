from . import views
from django.urls import path
from .views import follows

urlpatterns = [
       path('follows/', follows, name='follows'),
]