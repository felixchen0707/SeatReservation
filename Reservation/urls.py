from django.urls import path

from Reservation import views

urlpatterns = [
    path('', views.index),
    path('seatslist/', views.seatsList),
    path('reserve/', views.reserve_seat),
]
