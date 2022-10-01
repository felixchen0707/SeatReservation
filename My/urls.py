from django.urls import path

from My import views

urlpatterns = [
    path('reservation/', views.my_reservation),
    path('cancel/', views.cancel_reservation)
]
