from django.urls import path
from .views import BookingCreateAPIView, BookingReservationAPIView

urlpatterns = [
    path('rooms-available/', BookingCreateAPIView.as_view(), name='rooms-available'),
    path('rooms-booking/', BookingReservationAPIView.as_view(), name='book-room'),

]
