from django.urls import path
from .views import (
    RoomListAPIView,
    BookingReservationAPIView,
    BookingListAPIView,
    BookingCancelAPIView,
)

urlpatterns = [
    path("rooms-available/", RoomListAPIView.as_view(), name="rooms-available"),
    path("rooms-booking/", BookingReservationAPIView.as_view(), name="book-room"),
    path("user-bookings/", BookingListAPIView.as_view(), name="user-booking-list"),
    path(
        "user-bookings/<int:pk>/cancel/",
        BookingCancelAPIView.as_view(),
        name="user-booking-cancel",
    ),
]
