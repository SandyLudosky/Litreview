from . import views
from django.urls import path

urlpatterns = [
   path('profile/<str:user>/', views.user_profile, name="user_profile"),
]