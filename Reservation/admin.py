from django.contrib import admin
from Reservation.models import UserInfo, Region, Seat, ReservationHistory, UnfinishedReservation


# Register your models here.
@admin.register(UserInfo, Region, Seat, ReservationHistory, UnfinishedReservation)
class DefaultAdmin(admin.ModelAdmin):
    pass
